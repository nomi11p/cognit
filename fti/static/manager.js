/* =========================
   COGNIT MANAGER JS
========================= */

console.log("Manager JS Loaded");

/* =========================
   LOAD DASHBOARD
========================= */

async function loadDashboard() {

    try {

        const response =
            await fetch("/manager-data");

        const data =
            await response.json();

        const users =
            document.getElementById("users");

        const premium =
            document.getElementById("premium");

        const requests =
            document.getElementById("requests");

        const errors =
            document.getElementById("errors");

        const modelStatus =
            document.getElementById("modelStatus");

        const logs =
            document.getElementById("logs");

        if (users)
            users.innerText = data.users || 0;

        if (premium)
            premium.innerText = data.premium || 0;

        if (requests)
            requests.innerText = data.requests || 0;

        if (errors)
            errors.innerText = data.errors || 0;

        if (modelStatus)
            modelStatus.innerText =
                data.model_status || "Unknown";

        if (logs) {

            let html = "";

            if (
                data.logs &&
                data.logs.length > 0
            ) {

                data.logs.forEach(log => {

                    html += `
                    <div class="log-item">
                        ${log}
                    </div>
                    `;

                });

            } else {

                html =
                    "<div>No Logs Found</div>";

            }

            logs.innerHTML = html;

        }

    }

    catch (err) {

        console.error(
            "Dashboard Error:",
            err
        );

    }

}

/* =========================
   NAVIGATION
========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const libraryBtn =
            document.getElementById(
                "libraryBtn"
            );

        if (libraryBtn) {

            libraryBtn.addEventListener(
                "click",
                () => {

                    window.location.href =
                        "/library";

                }
            );

        }

        loadDashboard();

        setInterval(
            loadDashboard,
            5000
        );

    }
);