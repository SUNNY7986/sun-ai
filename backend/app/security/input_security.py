import re


PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"you\s+are\s+no\s+longer",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"reveal\s+(the\s+)?api\s+key",
    r"show\s+(the\s+)?api\s+key",
    r"give\s+me\s+(the\s+)?api\s+key",
    r"reveal\s+(the\s+)?credentials",
    r"reveal\s+(the\s+)?secrets",
    r"set\s+(the\s+)?risk\s+level",
    r"change\s+(the\s+)?risk\s+level",
]


def detect_prompt_injection(text: str) -> bool:
    """
    Detect common prompt-injection patterns in untrusted security logs.
    Returns True when suspicious instruction-like content is detected.
    """

    if not text:
        return False

    normalized_text = str(text).lower()

    return any(
        re.search(pattern, normalized_text, flags=re.IGNORECASE)
        for pattern in PROMPT_INJECTION_PATTERNS
    )


def sanitize_log(text: str) -> tuple[str, bool]:
    """
    Mark prompt-injection lines as untrusted data without executing
    or following their instructions.

    Returns:
        sanitized_text, injection_detected
    """

    if not text:
        return "", False

    lines = str(text).splitlines()
    sanitized_lines = []
    injection_detected = False

    for line in lines:

        if detect_prompt_injection(line):
            injection_detected = True

            sanitized_lines.append(
                "[PROMPT-INJECTION CONTENT DETECTED AND REDACTED]"
            )
        else:
            sanitized_lines.append(line)

    return "\n".join(sanitized_lines), injection_detected