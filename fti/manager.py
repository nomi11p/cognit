import time
import threading
import smtplib
from email.message import EmailMessage
from datetime import datetime
import json
import os

from connecter import register_manager

register_manager()

from apiforserver import get_api_status
from apiforserver import test_api


# =========================
# CONFIG (FIXED)
# =========================

OWNER_EMAIL = os.getenv("OWNER_EMAIL", "bhoivaidik@gmail.com")
EMAIL = os.getenv("SYSTEM_EMAIL", "ftiinfinity23@gmail.com")
PASSWORD = os.getenv("FTI_EMAIL_PASSWORD")  # FIXED (important)

ACTIVE_MODEL = "FTI-Small"
START_TIME = datetime.now()

# =========================
# SYSTEM STATS
# =========================

STATS = {
    "requests": 0,
    "errors": 0,
    "api_switches": 0
}

SYSTEM_STATUS = {
    "server": True,
    "model": True,
    "api": True,
    "manager": True
}

FEATURES = {
    "server": True,
    "manager": True,
    "model_system": True,
    "monitoring": True,
    "logging": True,
}


# =========================
# CORE FUNCTIONS
# =========================

def get_active_model():
    return ACTIVE_MODEL


def add_request():
    STATS["requests"] += 1


def add_error():
    STATS["errors"] += 1


def get_uptime():
    return int((datetime.now() - START_TIME).total_seconds())


def get_status():
    return {
        "time": str(datetime.now()),
        "uptime_seconds": get_uptime(),
        "active_model": ACTIVE_MODEL,
        "system_status": SYSTEM_STATUS,
        "features": FEATURES,
        "stats": STATS
    }

def get_stats():
    return {
        "requests": STATS["requests"],
        "errors": STATS["errors"]
    }

# =========================
# LOGGING
# =========================

def write_log():
    try:
        with open("fti_logs.txt", "a", encoding="utf-8") as file:
            file.write(json.dumps(get_status(), indent=2))
            file.write("\n\n")
    except Exception as e:
        print("LOG ERROR:", e)


# =========================
# EMAIL ALERT SYSTEM (FIXED)
# =========================

def send_alert(subject, message):
    try:
        if not EMAIL or not PASSWORD:
            print("EMAIL ALERT DISABLED (missing environment variables)")
            return

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = OWNER_EMAIL
        msg.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print("EMAIL ALERT SENT ✔")

    except smtplib.SMTPAuthenticationError:
        print("EMAIL ERROR: Authentication failed (use Gmail App Password)")
        SYSTEM_STATUS["api"] = False

    except Exception as e:
        print("EMAIL ERROR:", e)


# =========================
# HEALTH CHECK
# =========================

def health_check():
    if not SYSTEM_STATUS["server"]:
        send_alert("Server Offline", "FTI server is not responding.")

    if not SYSTEM_STATUS["api"]:
        send_alert("API Error", "FTI API system failure.")

    return get_status()


def generate_report():
    report = health_check()

    print("\n========== FTI REPORT ==========")
    print(json.dumps(report, indent=2))
    print("================================\n")

    write_log()


def monitor():
    while True:
        generate_report()
        time.sleep(600)  # 10 minutes


# =========================
# START MANAGER
# =========================

def start_manager():
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    print("FTI MANAGER STARTED ✔")


# =========================
# SYSTEM CONTROL
# =========================

def api_online():
    SYSTEM_STATUS["api"] = True


def api_offline():
    SYSTEM_STATUS["api"] = False


def server_online():
    SYSTEM_STATUS["server"] = True


def server_offline():
    SYSTEM_STATUS["server"] = False


def get_features():
    return FEATURES
# =========================
# TEST RUN
# =========================

if __name__ == "__main__":
    send_alert("FTI TEST", "Manager email system working ✔")
    start_manager()

    while True:
        time.sleep(1)