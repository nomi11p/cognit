from google import genai
from connecter import register_api
import os


register_api()

# ==========================
# FTI API SYSTEM
# ==========================

API_KEYS = [
  
    
     "AIzaSyAQ9fg5AYkWSp9j4iVivmhHV28o5awQQbc",
    #  "AIzaSyB2esPAWxN-E-PxWUogL9ID-AnJYLTA8H0",
    #  "AIzaSyBzww2X8ZfQ6ZHM3JNyswhhIH-YhKfSybU",
    #  "AIzaSyAbKCMKZMpW8CAiDye5GiCyAUUQ4rqkvFE",
    #  "AIzaSyBlGQNq5X8wM3QXT78F47B3Da5izsGY6Hk",
    #  "AIzaSyBmLsLmLqf3-fK742Smh7rEjLBhT1dPUwA",
    #  "AIzaSyCiCy5LiFFCfOWyc9kzB2cC4CnYTR0zJ28",
    #  "AIzaSyA3rNI6wPMKpGFmi4TbyY9FyTWh_ivP8ig",
    #  "AQ.Ab8RN6Ig0SiUgBK3jv1lzsn-0PjKIgDTe_flnna_aRpZYIdygQ",
    #  "AQ.Ab8RN6LIddH8BO0qMFr-nYTiLuVybUrQDiuTopr8F96HE8VNsg",
    #  "AQ.Ab8RN6I76sThUtzNtl6LZIrPSunwnezqLvhdbCX3GLRSsGJqMg",
    #  "AQ.Ab8RN6JILYcM9dS6r4_hQzmq4it5LSqte-LuzbguBzgMU_8vFg",
    # #  "jj",
    # #  "kk",
    # #  "kk",
    # #  "ll",
    # #  "hjj",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "jj",
    # #  "kk",
    # #  "kk",
    # #  "ll",
    # #  "hjj",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    # #  "dd",
    #  "AQ.Ab8RN6Kri7Oa7A8DRDAX-pd05x-S_D_Wv3l5WIkc6ec8m2ucxg",
    #  "AQ.Ab8RN6Kb6hf-H6PRWPQFEOlQXmJ91af3nNLNUG7fJietWGYPjw",
    #  "AQ.Ab8RN6KVgMh5y9tG201SDyEByUojtCYTci6mzF5o2x5Jqzskuw",
    #  "AQ.Ab8RN6LIddH8BO0qMFr-nYTiLuVybUrQDiuTopr8F96HE8VNsg",
    #  "AQ.Ab8RN6I76sThUtzNtl6LZIrPSunwnezqLvhdbCX3GLRSsGJqMg",
    #  "AIzaSyDDZFXjbuWGh1X6fjklz5juQUk4Lt3yF04",
    #  "AIzaSyBP5naDgJqTssfG7ycCWThYLsABRHPwAQ0",
    #  "AIzaSyBdCLqRbUeKkwvplZcNI2cUDJdfu6vRBK4",
    #  "AIzaSyA8VrrvdNM_iOaQwvgfGo_DUptr_dS-ATY",
    #  "AIzaSyBAJu2mEGJDLCkhHNamOEOSZzsUuPIrFXg",
    #  "AIzaSyAQj6qyzrzry9jYaYpg2cmn7bcS6GBadz4",
    #  "AIzaSyB2esPAWxN-E-PxWUogL9ID-AnJYLTA8H0",
     
    
]

# Remove empty keys
API_KEYS = [key for key in API_KEYS if key]
print("API KEYS FOUND:", len(API_KEYS))
print(API_KEYS)
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

