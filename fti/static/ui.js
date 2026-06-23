let currentMood = "normal";

/* =========================
   STORAGE SYSTEM
========================= */

function getChat() {
    return JSON.parse(localStorage.getItem("cognit_chat") || "[]");
}

function saveChat(chat) {
    localStorage.setItem("cognit_chat", JSON.stringify(chat));
}

function getSettings() {
    return JSON.parse(localStorage.getItem("cognit_settings") || "{}");
}

function saveSettings(settings) {
    localStorage.setItem("cognit_settings", JSON.stringify(settings));
}

/* =========================
   CHAT UI RENDER
========================= */

function render(role, text) {
    const chatBox = document.getElementById("chat");
    if (!chatBox) return;

    const div = document.createElement("div");
    div.classList.add("msg");

    if (role === "user") div.classList.add("user");
    else if (role === "system") div.classList.add("system");
    else div.classList.add("bot");

    div.innerText = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* =========================
   LOAD CHAT
========================= */

function loadChat() {
    const chat = getChat();
    const box = document.getElementById("chat");

    if (!box) return;

    box.innerHTML = "";

    chat.forEach(msg => {
        render(msg.role, msg.text);
    });
}

/* =========================
   NEW CHAT
========================= */

function newChat() {
    localStorage.removeItem("cognit_chat");

    const box = document.getElementById("chat");
    if (box) box.innerHTML = "";

    render("system", "New chat started.");
}

/* =========================
   MOOD SYSTEM
========================= */

function setMood(mood) {
    currentMood = mood;

    document.querySelectorAll(".item").forEach(btn => {
        btn.classList.remove("active");
        if (btn.innerText.toLowerCase() === mood) {
            btn.classList.add("active");
        }
    });

    render("system", "Mood changed to " + mood);
}

/* =========================
   CHAT SEND
========================= */

async function send() {
    const input = document.getElementById("input");
    if (!input) return;

    const text = input.value.trim();
    if (!text) return;

    render("user", text);

    let chat = getChat();
    chat.push({ role: "user", text });
    saveChat(chat);

    input.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prompt: text,
                mood: currentMood
            })
        });

        const data = await res.json();

        const reply = data.response || data.error || "No response";

        render("bot", reply);

        chat.push({ role: "bot", text: reply });
        saveChat(chat);

    } catch (err) {
        console.error(err);
        render("system", "Unable to connect to Cognit AI.");
    }
}

/* =========================
   PANEL SYSTEM (FIXED)
========================= */

function hidePanels() {
    document.querySelectorAll(".panel-page").forEach(p => {
        p.classList.remove("active-panel");
    });
}

function openPanel(id) {
    hidePanels();

    const panel = document.getElementById(id);

    if (panel) {
        panel.classList.add("active-panel");
    } else {
        console.log("Panel not found:", id);
    }
}

/* =========================
   ACCOUNT
========================= */

async function loadAccount() {
    try {
        const res = await fetch("/api/account");
        const data = await res.json();

        const box = document.getElementById("accountInfo");
        if (!box) return;

        if (data.logged_in) {
            box.innerHTML = `
                <h3>${data.username}</h3>
                <p>Status: Logged In</p>
                <a href="/logout">Logout</a>
            `;
        } else {
            box.innerHTML = `
                <h3>Guest User</h3>
                <a href="/login/google">Login With Google</a>
            `;
        }
    } catch (e) {
        console.error(e);
    }
}

/* =========================
   HISTORY UI
========================= */

function loadHistory() {
    const list = document.getElementById("historyList");
    if (!list) return;

    const chats = getChat();
    list.innerHTML = "";

    if (chats.length === 0) {
        list.innerHTML = "<p>No chat history found.</p>";
        return;
    }

    chats.forEach((msg, i) => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.innerText = `${i + 1}. ${msg.text.slice(0, 50)}`;
        list.appendChild(div);
    });
}

/* =========================
   SIMPLE ACTION BUTTONS
========================= */

function safeBind(id, fn) {
    const el = document.getElementById(id);
    if (el) el.addEventListener("click", fn);
}

/* =========================
   INIT
========================= */

window.onload = function () {

    loadChat();
    loadAccount();
    loadHistory();

    /* CHAT */
    safeBind("newChatBtn", newChat);

    /* PANELS */
    safeBind("accountBtn", () => openPanel("accountPanel"));
    safeBind("settingsBtn", () => openPanel("settingsPanel"));
    safeBind("teamBtn", () => openPanel("teamPanel"));
    safeBind("libraryBtn", () => openPanel("libraryPanel"));
    safeBind("projectsBtn", () => openPanel("projectsPanel"));
    safeBind("premiumBtn", () => openPanel("premiumPanel"));

    /* MISC */
    safeBind("libraryBtn", () => window.location.href = "/library");

    safeBind("syncBtn", async () => {
        const res = await fetch("/api/account");
        const data = await res.json();

        alert(data.logged_in
            ? "Connected: " + data.username
            : "Please login first"
        );
    });

    safeBind("imagesBtn", () => alert("Image generation coming soon"));
    safeBind("voiceBtn", () => alert("Voice chat coming soon"));

    safeBind("researchBtn", () => setMood("research"));
    safeBind("codingBtn", () => setMood("coding"));

    safeBind("donateBtn", async () => {
        const res = await fetch("/donate");
        const data = await res.json();
        alert("UPI: " + data.upi);
    });

    safeBind("premiumBtn", () => alert("Premium coming soon"));

    /* ENTER KEY */
    document.addEventListener("keydown", (e) => {
        if (e.key === "Enter") send();
    });

    /* PROJECTS */
    safeBind("createProjectBtn", createProject);
};