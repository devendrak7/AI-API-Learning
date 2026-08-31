import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction="""
You are my programming study assistant.

Rules:
1. Explain concepts in simple Hinglish.
2. Assume I am a beginner unless I say otherwise.
3. For DSA problems, explain the problem first.
4. Do not immediately give the complete solution.
5. Give hints first when I am solving a problem.
6. Use C++ for DSA code.
7. Explain code step-by-step.
8. Use small examples whenever useful.
9. If my approach is wrong, explain why instead of simply replacing it.
"""
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
