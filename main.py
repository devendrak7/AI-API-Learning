import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL_NAME
from rich.console import Console
from rich.markdown import Markdown

def clean_math(text):
    replacements = {
        r"\times": "×",
        r"\cdot": "·",
        r"\le": "≤",
        r"\ge": "≥",
        r"\neq": "≠",
        r"\infty": "∞",
        r"\rightarrow": "→",
        r"\leftarrow": "←",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("$", "")

    return text

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

console = Console()

print("🤖 AI Study Assistant Started!")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Chat ended.")
        break

    try:
        response = chat.send_message(question)

        console.print("\n[bold cyan]Gemini:[/bold cyan]\n")
        cleaned_response = clean_math(response.text)
        console.print(Markdown(cleaned_response))
        console.print()

    except Exception as e:
        print("\nError:", e)
        print()
