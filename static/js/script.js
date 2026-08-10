document.addEventListener("DOMContentLoaded", function () {

    const button = document.getElementById("darkModeToggle");

    // Load saved mode
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
        updateDarkModeButton(true);
    }

    // Button click
    if (button) {
        button.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            const enabled =
                document.body.classList.contains("dark-mode");

            if (enabled) {
                localStorage.setItem("darkMode", "enabled");
            } else {
                localStorage.setItem("darkMode", "disabled");
            }

            updateDarkModeButton(enabled);
        });
    }

});


function updateDarkModeButton(enabled) {

    const icon = document.getElementById("darkModeIcon");
    const text = document.getElementById("darkModeText");

    if (!icon || !text) {
        return;
    }

    if (enabled) {

        icon.className = "fa-solid fa-sun";
        text.textContent = "Light Mode";

    } else {

        icon.className = "fa-solid fa-moon";
        text.textContent = "Dark Mode";

    }
}