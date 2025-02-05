import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

load_dotenv(".env.local")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in '.env.local'")

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


# Define structured response model
class GeneratedWorld(BaseModel):
    terrain: str
    buildings: list
    lighting: str
    npc_behavior: str


# Function to call OpenAI and structure output
def generate_world(prompt: str) -> dict:
    system_prompt = """
    You are an AI assistant for game development.
    Generate a structured JSON world definition based on user input.
    """

    user_prompt = f"Generate a detailed structured JSON for a world based on the prompt: {prompt}"

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.7,
    )

    # Extract and return JSON
    return response["choices"][0]["message"]["content"]


# API Endpoint to Generate World
@app.post("/generate", response_model=GeneratedWorld)
async def generate(request: PromptRequest):
    world_data = generate_world(request.prompt)
    return world_data


# Run server
# uvicorn script_name:app --reload
