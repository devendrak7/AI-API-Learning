import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL_NAME

load_dotenv()

def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model=MODEL_NAME,
    config=types.GenerateContentConfig(
        system_instruction=load_prompt("prompts/dsa.txt")
    )
)

print("🤖 AI Study Assistant Started!")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Chat ended.")
        break

    try:
        response = chat.send_message(question)

        print("\nGemini:")
        print(response.text)
        print()

    except Exception as e:
        print("\nError:", e)
        print()
