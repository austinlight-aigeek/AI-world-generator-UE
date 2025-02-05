import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, analyze_prompt_and_generate, determine_city_size, check_prompt_validity

client = TestClient(app)

# Mock CONFIG_DATA to avoid dependency on external JSON file
MOCK_CONFIG_DATA = {
    "terrain": ["desert", "urban", "mountain", "forest", "coastal", "tundra", "volcanic", "swamp"],
    "buildings": ["apartment", "house", "villa", "skyscraper", "market", "shopping mall", "restaurant", "hotel", 
                  "factory", "warehouse", "power plant", "stadium", "castle", "museum", "church", "temple", 
                  "space station", "tower"],
    "lighting": ["day", "night", "sunset", "stormy", "cyberpunk neon", "eclipse", "foggy", "post-apocalyptic dim"],
    "npc_behavior": ["crowded", "empty", "active market", "quiet town", "chaotic", "military patrol", "zombie outbreak", "festive"]
}


@pytest.mark.parametrize("prompt, expected_size", [
    ("Generate a small medieval village", "small"),
    ("Generate a huge futuristic cyberpunk city", "large"),
    ("Generate a normal-sized modern city", "normal"),
    ("Generate a fantasy city with magic towers", "normal"),  # No size mentioned, should default to normal
    ("Create a vast metropolis with skyscrapers and highways", "large"),
])
@patch("main.openai.chat.completions.create")
def test_determine_city_size(mock_openai, prompt, expected_size):
    """
    Tests city size determination logic based on prompt.
    """
    mock_openai.return_value.choices = [type('', (), {"message": type('', (), {"content": expected_size})()})()]
    assert determine_city_size(prompt) == expected_size


@pytest.mark.parametrize("prompt, expected_validity", [
    ("Generate a cyberpunk city", True),
    ("Tell me a joke", False),
    ("Create a fantasy kingdom", True),  # Assume it's valid
    ("What is the weather today?", False),
])
@patch("main.openai.chat.completions.create")
def test_check_prompt_validity(mock_openai, prompt, expected_validity):
    """
    Tests if the prompt is correctly classified as valid (related to city generation) or not.
    """
    mock_openai.return_value.choices = [type('', (), {"message": type('', (), {"content": "yes" if expected_validity else "no"})()})()]
    assert check_prompt_validity(prompt) == expected_validity


@patch("main.openai.chat.completions.create")
def test_analyze_prompt_and_generate_invalid(mock_openai):
    """
    Tests that an invalid prompt returns an error message.
    """
    mock_openai.side_effect = lambda *args, **kwargs: type('', (), {
        "choices": [type('', (), {
            "message": type('', (), {
                "content": "no"
            })()
        })()]
    })()

    prompt = "Tell me about dinosaurs"
    response = analyze_prompt_and_generate(prompt)

    assert "error" in response
    assert response["error"] == "Your prompt does not seem related to generating a city. Please provide a relevant prompt."


@patch("main.analyze_prompt_and_generate", return_value={
    "terrain": "forest",
    "lighting": "sunset",
    "npc_behavior": "quiet town",
    "buildings": ["house", "church", "market"]
})
def test_generate_api(mock_generate):
    """
    Tests the /generate endpoint.
    """
    response = client.post("/generate", json={"prompt": "Generate a small medieval village"})
    
    assert response.status_code == 200
    data = response.json()
    assert "terrain" in data
    assert "lighting" in data
    assert "npc_behavior" in data
    assert "buildings" in data
    assert isinstance(data["buildings"], list)
    assert len(data["buildings"]) > 0


@patch("main.analyze_prompt_and_generate", return_value={"error": "Invalid request"})
def test_generate_api_invalid_prompt(mock_generate):
    """
    Tests the /generate endpoint with an invalid prompt.
    """
    response = client.post("/generate", json={"prompt": "Tell me a joke"})
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid request"


@pytest.mark.parametrize("prompt", [
    "",
    "   ",  # Whitespace-only input
    None
])
def test_generate_api_empty_prompt(prompt):
    """
    Tests /generate endpoint with empty input.
    """
    response = client.post("/generate", json={"prompt": prompt})
    
    assert response.status_code == 422  # FastAPI should return a validation error

