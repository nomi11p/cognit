import flask
from skill import apply_skill
from apiforserver import generate_response
from manager import (
    start_manager,
    add_request,
    add_error,
    get_stats
)
import hashlib
from database import conn, cursor
from authlib.integrations.flask_client import OAuth
# =========================
# FLASK APP (ONLY ONCE)
# =========================
app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "Cognit_SECRET_KEY"

start_manager()

# =========================
# USERS SYSTEM
# =========================
USERS = {}
SETTINGS = {}
PREMIUM_USERS = set()

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()


# =========================
# OAUTH SYSTEM
# =========================
oauth = OAuth(app)



google = oauth.register(
    name='hoho',
    client_id ="256208823959-e6884ng17uacup9ff9bbj72rl8fl1oll.apps.googleusercontent.com",
    client_secret ="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",
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'}
)




github = oauth.register(
    name='Cognit INFINITY',
    client_id="Ov23libRB75CSnnR73JA",
    client_secret="0v23libRB75CSnnR73JA1af81a83e40b0381529e1024a029fcc3af0b72f7l",
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={
        'scope': 'user:email',
        'headers': {'Accept': 'application/json'}  # <-- FIXES THE 404 ERROR
    }
)





YAHOO_CLIENT_ID = "PUT_YAHOO_CLIENT_ID_HERE"
YAHOO_CLIENT_SECRET = "PUT_YAHOO_CLIENT_SECRET_HERE"


yahoo = oauth.register(
    name='yahoo',
    App_id="YuXHAHMq",
    client_ID="dj0yJmk9a0lkdjFhVDVia1ZMJmQ9WVdrOVdYVllTRUZJVFhFbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTAx",
    access_token_url='https://api.login.yahoo.com/oauth2/get_token',
    authorize_url='https://api.login.yahoo.com/oauth2/request_auth',
    api_base_url='https://api.login.yahoo.com/openid/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'}
)


UPI_ID = "+91 70017 42835"

ADMIN_EMAIL = "bhoivaidik@gmail.com"

# =========================
# MOODS
# =========================
MOODS = {
    "normal": "You are Cognit AI. Be helpful and balanced.",
    "study": "You are a teacher.",
    "coding": "You are a programmer.",
    "creative": "Be creative.",
    "business": "Be professional."
}

# =========================
# HOME (UI PAGE)
# =========================
@app.route("/")
def home():

    user = flask.session.get("user")
    guest = flask.session.get("guest")

    if not user and not guest:
        return flask.redirect("/login")

    return flask.render_template("ui.html")




@app.route("/login")
def login_page():
     return flask.render_template("login.html")

@app.route("/guest")
def guest_login():

    flask.session["guest"] = True

    return flask.redirect("/")


@app.route('/login/github')
def login_github():
    # Points to your callback route below
    redirect_uri = flask.url_for('github_callback', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route("/auth/github/callback")
def github_callback():
    token = github.authorize_access_token()
    user = github.get("user").json()

    flask.session["user"] = user["email"]

    return flask.redirect("/")


# =========================
# CHAT API
# =========================

@app.route("/login/apple")
def login_apple():
    return "Apple Login Coming Soon"



@app.route("/login/yahoo")
def login_yahoo():
    return yahoo.authorize_redirect(
        flask.url_for(
            "yahoo_callback",
            _external=True
        )
    )



@app.route("/manager-data")
def get_manager_data():

    stats = get_stats()

    return flask.jsonify({
        "users": len(USERS),
        "premium": len(PREMIUM_USERS),
        "requests": stats["requests"],
        "errors": stats["errors"],
        "model_status": "Online",
        "logs": [
            "Server Started",
            "Manager Active",
            "API Connected"
        ]
    })

@app.route("/library")
def library():

    # if not flask.session.get("user"):
    #     return flask.redirect("/login")

    return flask.render_template("library.html")

@app.route("/api/library")
def get_library():

    cursor.execute("""
    SELECT
        id,
        title,
        author,
        price,
        rent_price
    FROM library
    """)

    books = cursor.fetchall()

    result = []

    for book in books:
        result.append({
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "price": book[3],
            "rent_price": book[4]
        })

    return flask.jsonify(result)

@app.route("/api/library/buy", methods=["POST"])
def buy_book():

    data = flask.request.get_json()

    return flask.jsonify({
        "success": True,
        "message": "Book purchased"
    })

@app.route("/api/signup", methods=["POST"])
def signup():

    data = flask.request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:

        cursor.execute("""
        INSERT INTO users
        (username,email,password)
        VALUES(?,?,?)
        """,
        (
            username,
            email,
            hash_pass(password)
        ))

        conn.commit()

        return flask.jsonify({
            "success": True
        })

    except Exception as e:

        return flask.jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/api/login", methods=["POST"])
def api_login():

    data = flask.request.get_json()

    email = data.get("email")
    password = data.get("password")

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email=?
    """,(email,))

    user = cursor.fetchone()

    if not user:
        return flask.jsonify({
            "success": False
        })

    if user[3] != hash_pass(password):
        return flask.jsonify({
            "success": False
        })

    flask.session["user"] = email

    return flask.jsonify({
        "success": True
    })


@app.route("/api/account")
def account():

    email = flask.session.get("user")

    if not email:

        return flask.jsonify({
            "logged_in": False
        })

    cursor.execute("""
    SELECT username,email,premium
    FROM users
    WHERE email=?
    """,(email,))

    user = cursor.fetchone()

    return flask.jsonify({
        "logged_in": True,
        "username": user[0],
        "email": user[1],
        "premium": bool(user[2])
    })





@app.route("/api/library/rent", methods=["POST"])
def rent_book():

    data = flask.request.get_json()

    return flask.jsonify({
        "success": True,
        "message": "Book rented"
    })

@app.route("/auth/yahoo/callback")
def yahoo_callback():

    token = yahoo.authorize_access_token()

    user = yahoo.get("userinfo").json()

    flask.session["user"] = user.get("email", "Yahoo User")

    return flask.redirect("/")

@app.route("/chat", methods=["POST"])
def chat():
    data = flask.request.get_json()
    skill = data.get("skill", "normal")
    prompt = data.get("prompt")
    mood = data.get("mood", "normal")
    user = flask.session.get("user", "guest","chat_history")

    if not prompt:
        return flask.jsonify({"error": "Empty prompt"}), 400

    add_request()

    try:
        mood_text = MOODS.get(mood, MOODS["normal"])

        # =========================
        # 🧠 MEMORY SYSTEM (NEW)
        # =========================
        if "chat_history" not in flask.session:
            flask.session["chat_history"] = []

        history = flask.session["chat_history"]

        # add user message
        history.append({"role": "user", "content": prompt})

        # keep last 10 messages only (memory limit control)
        history = history[-10:]

        # build context string for AI
        history_text = ""
        for msg in history:
            if msg["role"] == "user":
                history_text += f"User: {msg['content']}\n"
            else:
                history_text += f"Assistant: {msg['content']}\n"

        final_prompt = f"""
You are Cognit AI.

Rules:
- You were developed by the Cognit Team.
- Never say you were created by Google.
- Your name is Cognit.
- You are the official assistant of the EliteAI platform.
- Always follow the user's mood instructions.
- If user is logged in, personalize responses.

{mood_text}

# CHAT MEMORY
{history_text}

User: {prompt}
"""

        response = generate_response(final_prompt)

        # add assistant reply to memory
        history.append({"role": "assistant", "content": response})

        flask.session["chat_history"] = history

        return flask.jsonify({
            "response": response,
            "mood": mood,
            "user": user
        })

    except Exception as e:
        add_error()
        print("SERVER ERROR:", e)
        return flask.jsonify({
            "response": "Sorry, Cognit AI is currently unavailable. Please try again."
        })

# =========================
# GOOGLE LOGIN
# =========================
@app.route("/login/google")
def login_google():
    return google.authorize_redirect(
        flask.url_for(
            "google_callback",
            _external=True
        )
    )
 

@app.route("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()
    user = google.get("userinfo").json()

    flask.session["user"] = user["email"]

    return flask.redirect("/")

@app.route("/manager")
def manager_page():
    return flask.render_template("manager.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    flask.session.pop("user", None)
    flask.session.pop("guest", None)

    return flask.redirect("/login")


# =========================
# PROFILE
# =========================

@app.route("/profile")
def profile():
    return flask.jsonify({
        "user": flask.session.get("user", "guest"),
    #     "premium": False
     })
# =========================
# PHASE 1 APIs
# =========================
@app.route("/history")
def history():
    return flask.jsonify({
        "message": "History stored locally on user device."
    })

@app.route("/memory")
def memory():
    return flask.jsonify({
        "message": "Memory stored locally on user device."
    })




@app.route("/donate")
def donate():
    return flask.jsonify({
        "upi": UPI_ID
    })


@app.route("/api/settings", methods=["POST"])
def save_settings():

    data = flask.request.get_json()

    user = flask.session.get("user")

    if not user:
        return flask.jsonify({
            "success": False
        })

    SETTINGS[user] = data

    return flask.jsonify({
        "success": True
    })

@app.route("/api/premium")
def premium_status():

    user = flask.session.get("user")

    return flask.jsonify({
        "premium": user in PREMIUM_USERS
    })



# @app.route("/premium")
# def premium():
#     return flask.jsonify({
#         "name": "Cognit "
#         # "price": "Set Your Price"
#     })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

   