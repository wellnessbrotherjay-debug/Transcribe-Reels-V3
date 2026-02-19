import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("/Users/jaydengle/Transcribe-Reels/.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
