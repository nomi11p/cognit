
/* =========================
   COGNIT LOGIN JS
========================= */

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {

        loginForm.addEventListener("submit", async (e) => {

            e.preventDefault();

            const email =
                document.getElementById("email").value;

            const password =
                document.getElementById("password").value;

            try {

                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email,
                        password
                    })
                });

                const data = await response.json();

                if (data.success) {

                    alert("Login Successful");

                    window.location.href = "/";

                } else {

                    alert(
                        data.message ||
                        "Invalid Email or Password"
                    );

                }

            } catch (err) {

                console.error(err);

                alert("Server Error");

            }

        });

    }

});


/* =========================
   GOOGLE LOGIN
========================= */

function loginGoogle() {

    window.location.href = "/login/google";

}


/* =========================
   Github LOGIN
========================= */

function loginGithub() {

    window.location.href = "/login/github";

}


/* =========================
   YAHOO LOGIN
========================= */

function loginYahoo() {

    window.location.href = "/login/yahoo";

}

function loginApple() {

    window.location.href = "/login/apple";

}

/* =========================
   GUEST MODE
========================= */

function continueGuest() {
    window.location.href = "/guest";
}


/* =========================
   PRIVATE MODE
========================= */

function privateMode() {

    sessionStorage.setItem(
        "cognit_private",
        "true"
    );

    alert(
        "Private Mode Enabled.\nNo chat data will be saved."
    );

    window.location.href = "/";

}


/* =========================
   SHOW PASSWORD
========================= */

function togglePassword() {

    const password =
        document.getElementById("password");

    if (!password) return;

    password.type =
        password.type === "password"
        ? "text"
        : "password";

}


/* =========================
   SIGN UP PAGE
========================= */

function goSignup() {

    window.location.href = "/signup";

}


/* =========================
   FORGOT PASSWORD
========================= */

function forgotPassword() {

    alert(
        "Password recovery system coming soon."
    );

}

