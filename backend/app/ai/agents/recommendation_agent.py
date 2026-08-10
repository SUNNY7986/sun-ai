class RecommendationAgent:

    def __init__(self):

        self.recommendations = {

            "Brute Force": [
                "Block the suspicious IP address.",
                "Enable Multi-Factor Authentication (MFA).",
                "Lock accounts after repeated failed login attempts.",
                "Review authentication logs."
            ],

            "SQL Injection": [
                "Use parameterized SQL queries.",
                "Validate all user inputs.",
                "Deploy a Web Application Firewall (WAF).",
                "Review database access logs."
            ],

            "Cross Site Scripting (XSS)": [
                "Sanitize user input.",
                "Enable Content Security Policy (CSP).",
                "Escape HTML output.",
                "Validate all form inputs."
            ],

            "Phishing": [
                "Educate users about phishing emails.",
                "Enable email filtering.",
                "Require MFA.",
                "Verify suspicious links."
            ],

            "Malware": [
                "Isolate the infected device.",
                "Run endpoint antivirus scans.",
                "Update security patches.",
                "Review network traffic."
            ],

            "DDoS": [
                "Enable DDoS protection.",
                "Rate-limit incoming requests.",
                "Use CDN mitigation.",
                "Monitor network traffic."
            ]
        }

    def recommend(self, threat):

        return self.recommendations.get(
            threat.strip(),
            ["Further investigation is recommended."]
        )


if __name__ == "__main__":

    agent = RecommendationAgent()

    recommendations = agent.recommend("Brute Force")

    for recommendation in recommendations:
        print("-", recommendation)