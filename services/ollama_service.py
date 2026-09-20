import subprocess
import time

import requests


OLLAMA_URL = "http://localhost:11434"


def is_ollama_running() -> bool:
    try:
        response = requests.get(
            OLLAMA_URL,
            timeout=2
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def start_ollama():

    if is_ollama_running():
        print("Ollama is already running.")
        return

    print("Starting Ollama...")

    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(2)

    if not is_ollama_running():
        raise RuntimeError(
            "Unable to start Ollama."
        )

    print("Ollama started successfully.")