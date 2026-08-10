from app.ai.llm.llm_service import LLMService


class ThreatClassifier:

    def __init__(self):
        self.llm = LLMService()

    def classify(self, incident: str):

        prompt = f"""
You are a cybersecurity expert.

Classify the following incident into ONE category only.

Categories:
- Brute Force
- SQL Injection
- Cross Site Scripting (XSS)
- Phishing
- Malware
- DDoS
- Unknown

Incident:
{incident}

Return only the category name.
"""

        return self.llm.generate_response(prompt)


if __name__ == "__main__":

    classifier = ThreatClassifier()

    result = classifier.classify(
        "Multiple failed login attempts detected from the same IP."
    )

    print(result)