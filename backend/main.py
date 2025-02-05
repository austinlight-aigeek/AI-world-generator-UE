import json
import os
import re
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(".env.local")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in '.env.local'")

# Load predefined configuration
CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    CONFIG_DATA = json.load(file)  # Configuration data

# Initialize OpenAI client
openai = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Restrict CORS to frontend URL only
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"prompt": "Generate a futuristic cyberpunk city"}
            ]
        }
    )


def clean_json_response(response_text: str) -> str:
    """
    Removes backticks and unnecessary formatting from a GPT response to get clean JSON.
    """
    cleaned_text = re.sub(r"```(?:json)?", "", response_text).strip()
    return cleaned_text


def check_prompt_validity(prompt: str) -> bool:
    validation_prompt = f"""
        Does the following prompt request to generate a city?\n
        Prompt: '{prompt}'\n
        Answer with 'yes' or 'no' only.
    """

    # Step 1: Validate if the user prompt is related to generating a city description
    validation_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI that determines if a prompt is about city generation."},
                  {"role": "user", "content": validation_prompt}],
        max_tokens=10
    )

    is_valid = validation_response.choices[0].message.content.strip().lower()
    return is_valid == "yes"


def determine_city_size(prompt: str) -> str:
    """
        Uses LLM to classify the city type as 'small', 'normal', or 'large'.
    """

    size_prompt = f"""
        Analyze the following city generation prompt and determine the city size:
        
        Prompt: "{prompt}"
        
        Choose one of the following:
        - "small" (few buildings, quiet town)
        - "normal" (moderate buildings, balanced city)
        - "large" (many buildings, dense metropolis)
        
        Provide only the answer (small, normal, or large) with no additional text.
        If specific information of the city size if not found, answer should be "normal"
    """

    size_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You classify city descriptions into size categories."},
                  {"role": "user", "content": size_prompt}],
        max_tokens=10
    )

    city_size = size_response.choices[0].message.content.strip().lower()

    if city_size not in ["small", "normal", "large"]:
        return "normal"  # Default to normal if LLM fails

    return city_size


def analyze_prompt_and_generate(prompt: str) -> dict:
    """
        Analyzes the user prompt and selects the most relevant terrain, buildings, lighting, and NPC behavior.
    """

    # Step 1. Check if the prompt requires to generate a city
    is_valid = check_prompt_validity(prompt)

    if not is_valid:
        return {"error": "Your prompt does not seem related to generating a city. Please provide a relevant prompt."}

    # Step 2: Classify city size (small, normal, large)
    city_size = determine_city_size(prompt)

    # Step 3: Determine number of buildings based on city size
    if city_size == "small":
        num_buildings = random.randint(1, 3)
    elif city_size == "large":
        num_buildings = random.randint(8, 12)
    else:  # Normal city
        num_buildings = random.randint(4, 7)

    # Step 4: Ask LLM to classify the user prompt into predefined categories
    classification_prompt = f"""
        Analyze the following city generation prompt and categorize it based on the available options:
        
        Prompt: "{prompt}"
        
        Choose the most relevant category for each field from the given options:
        
        Terrain: {CONFIG_DATA["terrain"]}
        Lighting: {CONFIG_DATA["lighting"]}
        NPC Behavior: {CONFIG_DATA["npc_behavior"]}
        
        Answer in JSON format:
        {{
            "terrain": "<one of the terrain types>",
            "lighting": "<one of the lighting types>",
            "npc_behavior": "<one of the NPC behaviors>"
        }}
    """

    llm_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You classify city descriptions into predefined categories."},
                  {"role": "user", "content": classification_prompt}],
        max_tokens=50
    )

    # Extract structured data from response
    cleaned_response = clean_json_response(llm_response.choices[0].message.content.strip())

    try:
        city_data = json.loads(cleaned_response)
    except json.JSONDecodeError:
        city_data = {"error": "Failed to classify prompt into predefined categories."}
        return city_data

    # Step 5: Pick the most relevant buildings based on the prompt
    building_prompt = f"""
        Based on the city description "{prompt}", select the most relevant {num_buildings} buildings from this list:
        
        Buildings: {CONFIG_DATA["buildings"]}
        
        Answer in JSON format as an array:
        ["<building1>", "<building2>", "<building3>", ...]
    """

    building_response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You extract the most relevant buildings from a list based on a city description."},
                  {"role": "user", "content": building_prompt}],
        max_tokens=100
    )

    cleaned_buildings = clean_json_response(building_response.choices[0].message.content.strip())

    try:
        selected_buildings = json.loads(cleaned_buildings)
    except json.JSONDecodeError:
        selected_buildings = random.sample(CONFIG_DATA["buildings"], num_buildings)  # Fallback to random

    # Step 5: Construct final JSON output
    city_data["buildings"] = selected_buildings

    return city_data


@app.post("/generate")
async def generate(request: PromptRequest):
    """
    FastAPI route to generate structured city data.
    Ensures the prompt is not empty or only whitespace.
    """
    clean_prompt = request.prompt.strip()  # Remove leading/trailing whitespace

    if not clean_prompt:  # Reject if prompt is empty after stripping
        return JSONResponse(
            status_code=422,
            content={"error": "Prompt cannot be empty or only whitespace."}
        )

    return analyze_prompt_and_generate(clean_prompt)
