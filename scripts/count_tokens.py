import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(dotenv_path='backend/.env')

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in backend/.env")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    text = "We deliver to Nigeria,  but the provided text doesn't specify delivery to Abuja.  Shipping within Ghana and Nigeria takes 1–3 business days.  Customer support is available 24/7 via WhatsApp, Telegram, email (support@urbanstep.com), and phone (+233 550 123 456)."
    token_count = model.count_tokens(text)
    
    print(f"The exact token count for the phrase ''{text}'' is: {token_count.total_tokens}")
