/* =========================
   COGNIT LIBRARY JS
========================= */

document.addEventListener("DOMContentLoaded", () => {

    const content =
        document.getElementById("libraryContent");

    /* =====================
       EBOOKS
    ===================== */

    document
    .getElementById("ebooksBtn")
    ?.addEventListener("click", () => {

        content.innerHTML = `

        <h2>📘 E-Books</h2>

        <div class="book-grid">

            <div class="book-card">
                <div class="book-cover"></div>
                <div class="book-title">
                    AI Basics
                </div>
                <div class="book-author">
                    Cognit Team
                </div>
            </div>

            <div class="book-card">
                <div class="book-cover"></div>
                <div class="book-title">
                    Python Starter
                </div>
                <div class="book-author">
                    Cognit Team
                </div>
            </div>

        </div>
        `;

    });

    /* =====================
       NOTES
    ===================== */

    document
    .getElementById("notesBtn")
    ?.addEventListener("click", () => {

        content.innerHTML = `

        <h2>📄 Notes</h2>

        <ul>
            <li>Science Notes</li>
            <li>Math Notes</li>
            <li>Programming Notes</li>
            <li>AI Notes</li>
        </ul>

        `;

    });

    /* =====================
       SAVED CHATS
    ===================== */

    document
    .getElementById("savedChatsBtn")
    ?.addEventListener("click", () => {

        content.innerHTML = `

        <h2>💾 Saved Chats</h2>

        <p>
            Saved conversations will appear here.
        </p>

        `;

    });

    /* =====================
       DOWNLOADS
    ===================== */

    document
    .getElementById("downloadsBtn")
    ?.addEventListener("click", () => {

        content.innerHTML = `

        <h2>⬇ Downloads</h2>

        <p>
            Downloaded books and files will appear here.
        </p>

        `;

    });

    /* =====================
       SEARCH
    ===================== */

    document
    .getElementById("searchBtn")
    ?.addEventListener("click", () => {

        const query =
            document
            .getElementById("searchInput")
            .value
            .trim();

        if (!query) {

            alert(
                "Please enter something to search."
            );

            return;
        }

        content.innerHTML = `

        <h2>
            🔍 Search Results
        </h2>

        <p>
            Searching for:
            <strong>${query}</strong>
        </p>

        <br>

        <p>
            Search system will be connected to the database later.
        </p>

        `;

    });

});

/* =========================
   FUTURE FUNCTIONS
========================= */

function openBook(bookId){

    alert(
        "Open Book: " + bookId +
        "\nComing Soon"
    );

}

function downloadBook(bookId){

    alert(
        "Download Book: " + bookId +
        "\nComing Soon"
    );

}

function rentBook(bookId){

    alert(
        "Rent Book: " + bookId +
        "\nComing Soon"
    );

}

function buyBook(bookId){

    alert(
        "Buy Book: " + bookId +
        "\nComing Soon"
    );

}