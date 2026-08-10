import joblib


class SeverityPredictor:

    def __init__(self):
        self.model = joblib.load("models/severity_model.pkl")

    def predict(self, incident: str):
        prediction = self.model.predict([incident])
        return prediction[0]


if __name__ == "__main__":

    predictor = SeverityPredictor()

    result = predictor.predict(
        "Multiple failed login attempts from one IP address."
    )

    print("Predicted Severity:", result)