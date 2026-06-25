from google import genai
from connecter import register_api
import os


register_api()

# ==========================
# FTI API SYSTEM
# ==========================

# Load API keys from environment variable to avoid committing secrets to source control.
# Set FTI_API_KEYS as a comma-separated list of keys (e.g. "key1,key2") or leave empty.
API_KEYS = [k.strip() for k in os.environ.get("FTI_API_KEYS", "").split(",") if k.strip()]

# Remove empty keys
API_KEYS = [key for key in API_KEYS if key]
print("API KEYS FOUND:", len(API_KEYS))
MODEL_NAME = "gemini-2.5-flash-lite"

current_key_index = 0

API_STATUS = {
    "working": True,
    "total_keys": len(API_KEYS),
    "failed_requests": 0,
    "successful_requests": 0,
    "current_key": 0
}

# ==========================
# CLIENT LOADER
# ==========================

def load_client(api_key):

    return genai.Client(
        api_key=api_key
    )

# ==========================
# KEY ROTATION
# ==========================

def get_next_key():

    global current_key_index

    if not API_KEYS:
        raise Exception("sorry model is having some issues, please try again later")

    key = API_KEYS[current_key_index]

    API_STATUS["current_key"] = current_key_index

    current_key_index += 1

    if current_key_index >= len(API_KEYS):
        current_key_index = 0

    return key

# ==========================
# STATUS
# ==========================

def get_api_status():
    return API_STATUS

# ==========================
# MAIN RESPONSE FUNCTION
# ==========================

# ==========================
# MAIN RESPONSE FUNCTION
# ==========================

def generate_response(prompt, model_name=None):

    if not API_KEYS:
        return "FTI AI is currently unavailable."

    try:

        api_key = API_KEYS[0]

        client = genai.Client(
            api_key=api_key
        )

        import time

        response = None
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model= MODEL_NAME,
                    contents=prompt
                )
                break

            except Exception as e:
                if "503" in str(e):
                    print(f"Retry {attempt+1}/3...")
                    time.sleep(2)
                    continue
                raise

        if response is None:
            raise Exception("model is overloaded wait for it to cool down.")

        print("\n========== GEMINI RESPONSE ==========")
        print(response)
        print("=====================================\n")

        API_STATUS["successful_requests"] += 1
        API_STATUS["working"] = True

        if hasattr(response, "text"):
            return response.text

        return "model is offline."

    except Exception as e:

        API_STATUS["failed_requests"] += 1
        API_STATUS["working"] = False

        print("\n========== GEMINI ERROR ==========")
        print(e)
        print("==================================\n")

        return f"Error: {str(e)}"

# ==========================
# API CHECK
# ==========================

def test_api():

    try:

        response = generate_response(
            "Say hello."
        )

        return (
            response is not None
            and len(response) > 0
        )

    except Exception as e:

        print("TEST ERROR:", e)

        return False
