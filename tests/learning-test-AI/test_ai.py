import pytest
import requests
import time
    
def test_ollama_response():
    # End point
    url = "http://localhost:11434/api/generate"
    # Sample payload for the Ollama API
    payload = {
        "model": "tinyllama",
        "prompt": "Why is the sky blue?",
        "stream": False
    }

    start_time = time.time()

    response = requests.post(url, json=payload)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Response time: {duration:.2f} seconds")
    
    # Assert the HTTP status is 200
    assert response.status_code == 200, f"Failed! Status code is {response.status_code}"
    
    data = response.json()
    # Assert the response contains a "response" key and (bonus) it is not empty.
    assert "response" in data, "Failed! Key 'response' not found in JSON"
    assert len(data["response"]) > 0, "Failed! Response is empty"

    # Assert the response time is under 5 seconds.
    assert duration <= 20, f"Took {duration:.2f}s (Limit is 20s)"

