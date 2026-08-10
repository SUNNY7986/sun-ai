import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_response(self, prompt: str):

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert cybersecurity analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content


if __name__ == "__main__":

    llm = LLMService()

    response = llm.generate_response(
        "Explain what a brute force attack is."
    )

    print(response)