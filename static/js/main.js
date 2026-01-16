// -----------------------------
// MAIN JS – Global Scripts
// -----------------------------

// Show alert messages (used later)
function showMessage(message) {
    alert(message);
}

// -----------------------------
// FORM VALIDATION (BASIC)
// -----------------------------
document.addEventListener("DOMContentLoaded", function () {

    // Login form validation
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            const username = document.getElementById("username").value;
            const role = document.getElementById("role").value;

            if (username.trim() === "" || role === "") {
                e.preventDefault();
                alert("Please enter username and select role");
            }
        });
    }

    // Assessment submission confirmation
    const assessmentForm = document.getElementById("assessmentForm");
    if (assessmentForm) {
        assessmentForm.addEventListener("submit", function () {
            alert("Assessment submitted successfully!");
        });
    }

});

// -----------------------------
// DASHBOARD HELPERS
// -----------------------------
function startAssessment() {
    window.location.href = "/assessment";
}

function viewRoadmap() {
    window.location.href = "/roadmap";
}

function viewAnalytics() {
    window.location.href = "/analytics";
}
