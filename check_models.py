import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key[:20]}...") if api_key else print("NO API KEY!")

client = genai.Client(api_key=api_key)
print("\n🔍 Testing models:\n")

for model in ["gemini-pro", "models/gemini-pro", "gemini-1.5-flash", "models/gemini-1.5-flash"]:
    try:
        response = client.models.generate_content(model=model, contents="Say OK")
        print(f"✅ {model} - WORKS!")
        break
    except Exception as e:
        print(f"❌ {model} - FAILED")