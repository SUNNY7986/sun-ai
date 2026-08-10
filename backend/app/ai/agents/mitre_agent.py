class MitreAgent:

    def __init__(self):

        self.mapping = {

            "Brute Force": {
                "technique": "T1110",
                "tactic": "Credential Access"
            },

            "SQL Injection": {
                "technique": "T1190",
                "tactic": "Initial Access"
            },

            "Cross Site Scripting (XSS)": {
                "technique": "T1059",
                "tactic": "Execution"
            },

            "Phishing": {
                "technique": "T1566",
                "tactic": "Initial Access"
            },

            "Malware": {
                "technique": "T1204",
                "tactic": "Execution"
            },

            "DDoS": {
                "technique": "T1498",
                "tactic": "Impact"
            }
        }

    def get_mapping(self, threat):

        return self.mapping.get(
            threat.strip(),
            {
                "technique": "Unknown",
                "tactic": "Unknown"
            }
        )


if __name__ == "__main__":

    agent = MitreAgent()

    result = agent.get_mapping("Brute Force")

    print(result)