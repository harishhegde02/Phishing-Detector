import os
import time
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import json
import random

# Load environment variables
load_dotenv('.env.local')
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env.local")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

PROMPT_TEMPLATE = """
Generate {count} unique examples of {category} email subjects/snippets.
Each example must include the text and boolean flags (0 or 1) for the following labels:
- urgency
- authority
- fear
- impersonation

Format the output as a JSON list of objects. Each object should have keys: "text", "urgency", "authority", "fear", "impersonation".
Ensure the "text" is realistic and varied.

Example JSON format:
[
  {{"text": "Example email text here", "urgency": 1, "authority": 0, "fear": 0, "impersonation": 0}},
  ...
]
"""

CATEGORIES = [
    "phishing (financial/payment urgency)",
    "phishing (account security/blocked)",
    "phishing (CEO/executive impersonation)",
    "phishing (HR/payroll/benefits)",
    "phishing (IT support/password reset)",
    "phishing (delivery/package pending)",
    "phishing (contest winner/reward)",
    "benign (casual conversation)",
    "benign (work meeting/schedule)",
    "benign (newsletter/marketing)",
    "benign (transaction receipt)",
    "benign (project update/collaboration)"
]

def generate_batch(count=5, category="phishing"):
    prompt = PROMPT_TEMPLATE.format(count=count, category=category)
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Cleanup markdown json blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        return data
    except Exception as e:
        print(f"Error generating batch for {category}: {e}")
        return []

def main():
    print("Starting AI data generation with separate batch files...")
    
    output_dir = 'data/raw'
    os.makedirs(output_dir, exist_ok=True)
    
    for i, category in enumerate(CATEGORIES):
        print(f"Generating for: {category}")
        # Generate 1 batch per category
        batch_data = generate_batch(count=10, category=category) # Increased to 10
        
        if batch_data:
            df_batch = pd.DataFrame(batch_data)
            # Save to unique file
            filename = f"ai_gen_{i}_{int(time.time())}.csv"
            output_path = os.path.join(output_dir, filename)
            df_batch.to_csv(output_path, index=False)
            print(f"  Saved {len(df_batch)} to {filename}")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
