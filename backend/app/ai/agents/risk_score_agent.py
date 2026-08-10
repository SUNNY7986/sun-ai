class RiskScoreAgent:

    def calculate_score(self, severity):

        scores = {
            "Low": 25,
            "Medium": 50,
            "High": 75,
            "Critical": 95
        }

        return scores.get(severity.strip(), 0)


if __name__ == "__main__":

    agent = RiskScoreAgent()

    print(agent.calculate_score("High"))