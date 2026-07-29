// ==========================
// MOBILE NAVBAR (Optional)
// ==========================

const menuBtn = document.querySelector(".menu-btn");
const navLinks = document.querySelector(".nav-links");

if (menuBtn && navLinks) {

    menuBtn.addEventListener("click", () => {

        navLinks.classList.toggle("active");

    });

}


// ==========================
// AUTO HIDE FLASH MESSAGE
// ==========================

const alerts = document.querySelectorAll(".alert");

alerts.forEach((alert) => {

    setTimeout(() => {

        alert.style.opacity = "0";

        setTimeout(() => {

            alert.remove();

        }, 500);

    }, 3000);

});


// ==========================
// CONFIRM DELETE DOCTOR
// ==========================

const deleteButtons = document.querySelectorAll(".delete");

deleteButtons.forEach((button) => {

    button.addEventListener("click", function (e) {

        if (!confirm("Are you sure you want to delete this doctor?")) {

            e.preventDefault();

        }

    });

});


// ==========================
// CONFIRM CANCEL APPOINTMENT
// ==========================

const cancelButtons = document.querySelectorAll(".cancel-btn");

cancelButtons.forEach((button) => {

    button.addEventListener("click", function (e) {

        if (!confirm("Cancel this appointment?")) {

            e.preventDefault();

        }

    });

});


// ==========================
// CONFIRM APPROVE
// ==========================

const approveButtons = document.querySelectorAll(".approve");

approveButtons.forEach((button) => {

    button.addEventListener("click", function (e) {

        if (!confirm("Approve this appointment?")) {

            e.preventDefault();

        }

    });

});


// ==========================
// CONFIRM REJECT
// ==========================

const rejectButtons = document.querySelectorAll(".reject");

rejectButtons.forEach((button) => {

    button.addEventListener("click", function (e) {

        if (!confirm("Reject this appointment?")) {

            e.preventDefault();

        }

    });

});


// ==========================
// PASSWORD MATCH
// ==========================

const registerForm = document.querySelector("#registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function (e) {

        const password = document.getElementById("password");

        const confirmPassword = document.getElementById("confirm_password");

        if (password && confirmPassword) {

            if (password.value !== confirmPassword.value) {

                e.preventDefault();

                alert("Passwords do not match.");

            }

        }

    });

}


// ==========================
// TODAY DATE
// ==========================

const dateInput = document.getElementById("appointment_date");

if (dateInput) {

    const today = new Date().toISOString().split("T")[0];

    dateInput.min = today;

}


// ==========================
// SMOOTH SCROLL
// ==========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});


// ==========================
// BUTTON HOVER EFFECT
// ==========================

const buttons = document.querySelectorAll(".btn");

buttons.forEach((button) => {

    button.addEventListener("mouseenter", () => {

        button.style.transform = "scale(1.05)";

    });

    button.addEventListener("mouseleave", () => {

        button.style.transform = "scale(1)";

    });

});


// ==========================
// PAGE LOADED
// ==========================

window.addEventListener("load", () => {

    console.log("Dental Booking System Loaded Successfully.");

});