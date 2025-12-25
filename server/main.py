from fastapi import FastAPI
import os
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = AsyncInferenceClient(
    api_key=os.getenv("HF_TOKEN"),
)
model = "meta-llama/Llama-3.1-8B-Instruct"


@app.get("/")
async def root():
    return {"message": "Welcome to Kinoji, an interesting place keep your cinema fantasies alive."}


@app.get ("/insights")
async def getInsights():
    result = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Hello, how are you doing? I'll be using you for a data science project I'm working now, are you ready?"
            }
        ]
    )
    return result.choices[0].message.content