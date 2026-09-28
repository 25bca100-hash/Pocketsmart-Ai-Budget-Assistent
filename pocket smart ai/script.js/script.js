document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // Form validation
    // -----------------------------

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const budget = form.querySelector('input[name="budget"]');

            if (budget) {
                const value = Number(budget.value);

                if (value <= 0 || isNaN(value)) {
                    event.preventDefault();

                    alert("Please enter a valid budget greater than 0.");

                    budget.focus();
                }
            }

        });

    });


    // -----------------------------
    // Guest validation for Party Planner
    // -----------------------------

    const guestInput = document.querySelector(
        'input[name="guests"]'
    );

    if (guestInput) {

        guestInput.addEventListener("input", function () {

            if (Number(this.value) < 1) {
                this.setCustomValidity(
                    "Number of guests must be at least 1."
                );
            } else {
                this.setCustomValidity("");
            }

        });

    }


    // -----------------------------
    // Automatically hide result
    // -----------------------------

    const result = document.querySelector(".result");

    if (result) {

        setTimeout(function () {

            result.style.transition = "opacity 0.5s";
            result.style.opacity = "1";

        }, 100);

    }


    // -----------------------------
    // Button loading effect
    // -----------------------------

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector(
                'button[type="submit"]'
            );

            if (button) {

                setTimeout(function () {

                    button.disabled = true;
                    button.textContent = "Creating Plan...";

                }, 10);

            }

        });

    });


    // -----------------------------
    // Confirmation before logout
    // -----------------------------

    const logoutLinks = document.querySelectorAll(
        'a[href*="logout"]'
    );

    logoutLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const confirmLogout = confirm(
                "Are you sure you want to logout?"
            );

            if (!confirmLogout) {
                event.preventDefault();
            }

        });

    });

});
