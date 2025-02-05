import re
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env.local")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in '.env.local'")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Restrict CORS to frontend URL only
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


class PromptRequest(BaseModel):
    prompt: str


def clean_json_response(response_text: str) -> str:
    """
    Removes backticks and unnecessary formatting from a GPT response to get clean JSON.
    """
    # Remove triple backticks and newlines around JSON
    cleaned_text = re.sub(r"```(?:json)?", "", response_text).strip()
    return cleaned_text


# Function to call OpenAI and structure output
def generate_world(user_prompt: str) -> dict:

    validation_prompt = (
        f"Does the following prompt request to generate a city?\n"
        f"Prompt: '{user_prompt}'\n"
        f"Answer with 'yes' or 'no' only."
    )

    # Step 1: Validate if the user prompt is related to generating a city description
    validation_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that determines if a prompt is about city generation."},
                  {"role": "user", "content": validation_prompt}],
        max_tokens=10
    )

    is_valid_prompt = validation_response.choices[0].message.content.strip().lower()

    if is_valid_prompt != 'yes':
        return {"error": "Your prompt does not seem related to generating a city. Please provide a relevant prompt."}

    # Step 2: Generate a city description based on the valid prompt
    city_prompt = (
        f"Generate a city description based on the following prompt: {user_prompt}.\n"
        f"Ensure the output follows this JSON schema:\n"
        f"{{\n"
        f'"terrain": "<terrain_type>",\n'
        f'"buildings": ["<building1>", "<building2>", "<building3>"],\n'
        f'"lighting": "<lighting_type>",\n'
        f'"NPC": "<npc_activity>"\n'
        f"}}\n"
        f"Provide only the JSON output, no extra text."
    )

    city_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You generate creative yet reasonable city descriptions in JSON format."},
                  {"role": "user", "content": city_prompt}],
        temperature=1.0,
    )

    city_description = city_response.choices[0].message.content.strip()
    cleaned_city_description = clean_json_response(city_description)
    
    try:
        city_data = json.loads(cleaned_city_description)
    except json.JSONDecodeError:
        city_data = {"error": "Failed to generate valid JSON output."}

    return city_data


# API Endpoint to Generate World
@app.post("/generate")
async def generate(request: PromptRequest):
    """
    FastAPI route to handle city generation based on user input.
    """
    return generate_world(request.prompt)
