from datetime import datetime
from pyngrok import ngrok
from github import Github, Auth

# ==========================
# FTI CONNECTER V2
# ==========================

VERSION = "2.0"

CONNECTIONS = {
    "server": False,
    "manager": False,
    "api": False,
    "ngrok": False,
    "github": False
}

PUBLIC_URL = None
GITHUB_CLIENT = None
GITHUB_USER = None


# ==========================
# REGISTRATION
# ==========================

def register_server():
    CONNECTIONS["server"] = True


def register_manager():
    CONNECTIONS["manager"] = True


def register_api():
    CONNECTIONS["api"] = True


# ==========================
# NGROK
# ==========================

def start_ngrok(port=5000):
    global PUBLIC_URL

    try:
        tunnel = ngrok.connect(port)

        PUBLIC_URL = tunnel.public_url

        CONNECTIONS["ngrok"] = True

        return PUBLIC_URL

    except Exception as e:
        CONNECTIONS["ngrok"] = False
        return f"NGROK ERROR: {e}"


def get_public_url():
    return PUBLIC_URL


# ==========================
# GITHUB
# ==========================

def connect_github(token):
    global GITHUB_CLIENT
    global GITHUB_USER

    try:
        auth = Auth.Token(token)

        GITHUB_CLIENT = Github(auth=auth)

        user = GITHUB_CLIENT.get_user()

        GITHUB_USER = user.login

        CONNECTIONS["github"] = True

        return GITHUB_USER

    except Exception as e:
        CONNECTIONS["github"] = False
        return f"GITHUB ERROR: {e}"


def github_connected():
    return CONNECTIONS["github"]


# ==========================
# STATUS
# ==========================

def system_ready():

    return (
        CONNECTIONS["server"]
        and CONNECTIONS["manager"]
        and CONNECTIONS["api"]
    )


def get_status():

    return {
        "version": VERSION,
        "time": str(datetime.now()),
        "connections": CONNECTIONS,
        "public_url": PUBLIC_URL,
        "github_user": GITHUB_USER,
        "ready": system_ready()
    }


# ==========================
# START
# ==========================

def start_connecter():
    print("FTI CONNECTER STARTED")
    print(get_status())

if __name__ == "__main__":
    register_server()
register_manager()
register_api()

GITHUB_TOKEN = "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"

print("\nCONNECTING TO GITHUB...")
print(connect_github(GITHUB_TOKEN))
print("\nSTARTING NGROK...")
print(start_ngrok(5000))

print("\nFTI STATUS:")
print(get_status())