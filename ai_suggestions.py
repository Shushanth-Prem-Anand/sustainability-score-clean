# ai_suggestions.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_suggestions(product_data):
    system_prompt = (
        "You are a sustainability expert. Given product attributes such as materials used, transport method, "
        "packaging, global warming potential (GWP), cost, and circularity, give 2-3 actionable suggestions to make the product more environmentally sustainable. "
        "Avoid repeating general phrases. Base suggestions on concrete facts like material impact, transport emissions, etc."
    )

    product_desc = f"""
Product: {product_data.get("product_name", "Unknown")}
Materials: {', '.join(product_data.get("materials", []))}
Weight (g): {product_data.get("weight_grams", 0)}
Transport: {product_data.get("transport", "unknown")}
Packaging: {product_data.get("packaging", "unknown")}
GWP: {product_data.get("gwp", "unknown")}
Cost: {product_data.get("cost", "unknown")}
Circularity: {product_data.get("circularity", "unknown")}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": product_desc}
            ],
            temperature=0.7,
            max_tokens=150
        )
        output = response['choices'][0]['message']['content']
        suggestions = [line.strip("- ").strip() for line in output.strip().split("\n") if line.strip()]
        return suggestions
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return ["Unable to generate suggestions at this time."]
