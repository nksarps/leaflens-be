import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def list_gemini_models():
    print('Available Gemini Models:')
    for m in genai.list_models():
        # Check if model supports 'generateContent
        if 'generateContent' in m.supported_generation_methods:
            print(f'- {m.name} (Supported for generateContent)')
        else:
            print(f'- {m.name} (Does NOT support generateContent)')
