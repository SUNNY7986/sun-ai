from app.ai.ml.predict import SeverityPredictor


class SeverityAgent:

    def __init__(self):
        self.predictor = SeverityPredictor()

    def predict_severity(self, incident: str):
        return self.predictor.predict(incident)


if __name__ == "__main__":

    agent = SeverityAgent()

    result = agent.predict_severity(
        "Multiple failed login attempts from the same IP within 2 minutes."
    )

    print(result)