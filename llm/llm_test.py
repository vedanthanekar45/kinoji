import os
from huggingface_hub import InferenceClient
import json
from dotenv import load_dotenv

load_dotenv

# Your Token (Keep this safe!)
HF_TOKEN = os.getenv('HUGGING_FACE_TOKEN')

# Initialize the client (connects to HF servers)
client = InferenceClient(token=HF_TOKEN)

def generate_chart_config(movie_data):
    # 1. The Prompt: Be extremely specific about what you want
    system_prompt = """
    You are a data visualization expert. 
    You receive movie data and output a JSON configuration for Chart.js.
    Do NOT output any markdown, explanations, or text. ONLY the raw JSON object.
    """
    
    user_prompt = f"""
    Create a bar chart comparing the box office revenue of these movies:
    {json.dumps(movie_data)}
    
    Use millions of USD for the Y-axis. Color the bars blue.
    """

    # 2. Call the API (Llama-3-8B-Instruct)
    response = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
        temperature=0.1  # Low temperature = more consistent/strict code
    )

    # 3. Extract the answer
    return response.choices[0].message.content

# --- TEST IT ---
sample_data = [
    {"title": "Movie A", "revenue": 150000000},
    {"title": "Movie B", "revenue": 85000000},
    {"title": "Movie C", "revenue": 200000000}
]

json_output = generate_chart_config(sample_data)
print(json_output)