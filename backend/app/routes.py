from datetime import datetime, timedelta
import json
import os

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    UploadFile,
    File,
)
from fastapi.responses import FileResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import func

from app.models import (
    LoginRequest,
    RegisterRequest,
    LogRequest,
)

from app.database import SessionLocal

from app.db_models import (
    User,
    Analysis,
)

from app.ai_service import analyze_security_log
from app.pdf_service import generate_pdf


# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = os.getenv(
    "SUN_AI_SECRET_KEY",
    "sun_ai_secret_key_change_me",
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


router = APIRouter()


# ==========================================================
# Helper Functions
# ==========================================================

def create_access_token(data: dict):
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_token(
    token: str = Depends(oauth2_scheme),
):
    """
    Validate JWT token and return username.
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


def safe_json_loads(value, default=None):
    """
    Safely convert JSON database strings back to Python objects.
    """

    if default is None:
        default = []

    if value is None:
        return default

    if isinstance(value, (list, dict)):
        return value

    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default


# ==========================================================
# Login
# ==========================================================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.username == form_data.username
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        if not pwd_context.verify(
            form_data.password,
            user.password,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        access_token = create_access_token({
            "sub": user.username,
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "message": "Login successful",
        }

    finally:
        db.close()


# ==========================================================
# Profile
# ==========================================================

@router.get("/profile")
def profile(
    username: str = Depends(verify_token),
):

    return {
        "message": "Welcome to SUN AI",
        "username": username,
    }


# ==========================================================
# Register
# ==========================================================

@router.post("/register")
def register(
    user: RegisterRequest,
):

    db = SessionLocal()

    try:

        existing_username = (
            db.query(User)
            .filter(
                User.username == user.username
            )
            .first()
        )

        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )

        existing_email = (
            db.query(User)
            .filter(
                User.email == user.email
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        hashed_password = pwd_context.hash(
            user.password
        )

        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Registration successful",
            "username": new_user.username,
            "email": new_user.email,
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        db.close()


# ==========================================================
# Manual Log Analysis
# ==========================================================

@router.post("/analyze")
def analyze_log(
    request: LogRequest,
):

    if not request.log_text or not request.log_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Security log cannot be empty.",
        )

    db = SessionLocal()

    try:

        result = analyze_security_log(
            request.log_text
        )

        analysis = Analysis(
            filename="Manual Input",

            risk_level=result["risk_level"],

            attack_type=result["attack_type"],

            severity_score=result["severity_score"],

            confidence=result["confidence"],

            reasoning=result["reasoning"],

            affected_assets=json.dumps(
                result["affected_assets"]
            ),

            iocs=json.dumps(
                result["iocs"]
            ),

            summary=result["summary"],

            recommendations=json.dumps(
                result["recommendations"]
            ),

            next_steps=json.dumps(
                result["next_steps"]
            ),
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "status": "success",
            "id": analysis.id,
            "analysis": result,
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        db.close()


# ==========================================================
# Upload Security Log
# ==========================================================

@router.post("/upload-log")
async def upload_log(
    file: UploadFile = File(...),
):
    MAX_LOG_SIZE = 2 * 1024 * 1024  # 2 MB
    ALLOWED_EXTENSIONS = {".log", ".txt"}

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    # Get a safe filename
    safe_filename = os.path.basename(file.filename)

    # Check file extension
    extension = os.path.splitext(safe_filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a .log or .txt file.",
        )

    db = SessionLocal()

    try:
        # Read only slightly more than the maximum allowed size
        content = await file.read(MAX_LOG_SIZE + 1)

        # Prevent oversized uploads
        if len(content) > MAX_LOG_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum allowed size is 2 MB.",
            )

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        try:
            log_text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid text file. Please upload a UTF-8 text log.",
            )

        if not log_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Uploaded log is empty.",
            )

        result = analyze_security_log(
            log_text
        )

        analysis = Analysis(
            filename=safe_filename,

            risk_level=result["risk_level"],

            attack_type=result["attack_type"],

            severity_score=result["severity_score"],

            confidence=result["confidence"],

            reasoning=result["reasoning"],

            affected_assets=json.dumps(
                result["affected_assets"]
            ),

            iocs=json.dumps(
                result["iocs"]
            ),

            summary=result["summary"],

            recommendations=json.dumps(
                result["recommendations"]
            ),

            next_steps=json.dumps(
                result["next_steps"]
            ),
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "status": "success",
            "id": analysis.id,
            "filename": safe_filename,
            "analysis": result,
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        db.close()

# ==========================================================
# Analysis History
# ==========================================================

@router.get("/history")
def get_history():

    db = SessionLocal()

    try:

        analyses = (
            db.query(Analysis)
            .order_by(
                Analysis.id.desc()
            )
            .all()
        )

        history = []

        for analysis in analyses:

            history.append({
                "id": analysis.id,

                "filename": analysis.filename,

                "risk_level": analysis.risk_level,

                "attack_type": analysis.attack_type,

                "severity_score": analysis.severity_score,

                "confidence": analysis.confidence,

                "reasoning": analysis.reasoning,

                "affected_assets": safe_json_loads(
                    analysis.affected_assets
                ),

                "iocs": safe_json_loads(
                    analysis.iocs
                ),

                "summary": analysis.summary,

                "recommendations": safe_json_loads(
                    analysis.recommendations
                ),

                "next_steps": safe_json_loads(
                    analysis.next_steps
                ),
            })

        return history

    finally:
        db.close()


# ==========================================================
# Dashboard
# ==========================================================

@router.get("/dashboard")
def dashboard():

    db = SessionLocal()

    try:

        total = (
            db.query(Analysis)
            .count()
        )

        critical = (
            db.query(Analysis)
            .filter(
                func.lower(
                    Analysis.risk_level
                ) == "critical"
            )
            .count()
        )

        high = (
            db.query(Analysis)
            .filter(
                func.lower(
                    Analysis.risk_level
                ) == "high"
            )
            .count()
        )

        medium = (
            db.query(Analysis)
            .filter(
                func.lower(
                    Analysis.risk_level
                ) == "medium"
            )
            .count()
        )

        low = (
            db.query(Analysis)
            .filter(
                func.lower(
                    Analysis.risk_level
                ) == "low"
            )
            .count()
        )

        latest = (
            db.query(Analysis)
            .order_by(
                Analysis.id.desc()
            )
            .first()
        )

        # Find most common attack type
        attack_counts = (
            db.query(
                Analysis.attack_type,
                func.count(
                    Analysis.attack_type
                ).label("count"),
            )
            .filter(
                Analysis.attack_type.isnot(None)
            )
            .group_by(
                Analysis.attack_type
            )
            .order_by(
                func.count(
                    Analysis.attack_type
                ).desc()
            )
            .first()
        )

        most_common_attack = (
            attack_counts[0]
            if attack_counts
            else None
        )

        return {
            "total_analyses": total,

            "critical_risk": critical,

            "high_risk": high,

            "medium_risk": medium,

            "low_risk": low,

            "latest_analysis": (
                latest.id
                if latest
                else None
            ),

            "most_common_attack": most_common_attack,
        }

    finally:
        db.close()


# ==========================================================
# Delete Analysis
# ==========================================================

@router.delete("/analysis/{analysis_id}")
def delete_analysis(
    analysis_id: int,
):

    db = SessionLocal()

    try:

        analysis = (
            db.query(Analysis)
            .filter(
                Analysis.id == analysis_id
            )
            .first()
        )

        if analysis is None:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found",
            )

        db.delete(analysis)
        db.commit()

        return {
            "message": "Analysis deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        db.close()


# ==========================================================
# Download PDF Report
# ==========================================================

@router.get("/download-report/{analysis_id}")
def download_report(
    analysis_id: int,
):

    db = SessionLocal()

    try:

        analysis = (
            db.query(Analysis)
            .filter(
                Analysis.id == analysis_id
            )
            .first()
        )

        if analysis is None:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found",
            )

        reports_dir = "reports"

        os.makedirs(
            reports_dir,
            exist_ok=True,
        )

        pdf_path = os.path.join(
            reports_dir,
            f"SUN_AI_Report_{analysis.id}.pdf",
        )

        generate_pdf(
            analysis,
            pdf_path,
        )

        return FileResponse(
            path=pdf_path,
            filename=(
                f"SUN_AI_Report_{analysis.id}.pdf"
            ),
            media_type="application/pdf",
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:
        db.close()