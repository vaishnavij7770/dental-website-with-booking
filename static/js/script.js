// ===============================
// Dental Booking System
// script.js
// ===============================

// -------------------------------
// Auto Hide Flash Messages
// -------------------------------

document.addEventListener("DOMContentLoaded", () => {

    const message = document.querySelector(".message");

    if (message) {

        setTimeout(() => {

            message.style.transition = "0.5s";
            message.style.opacity = "0";

            setTimeout(() => {

                message.remove();

            }, 500);

        }, 3000);

    }

});


// -------------------------------
// Mobile Navbar Toggle
// (Optional if menu button added)
// -------------------------------

const menuBtn = document.querySelector(".menu-btn");

if (menuBtn) {

    menuBtn.addEventListener("click", () => {

        document.querySelector("nav ul").classList.toggle("show");

    });

}


// -------------------------------
// Registration Validation
// -------------------------------

const registerForm = document.querySelector("form");

if (registerForm && window.location.pathname === "/register") {

    registerForm.addEventListener("submit", function (e) {

        const mobile = document.querySelector("input[name='mobile']").value;

        const password = document.querySelector("input[name='password']").value;

        if (!/^[0-9]{10}$/.test(mobile)) {

            alert("Mobile number must contain exactly 10 digits.");

            e.preventDefault();

            return;
        }

        if (password.length < 6) {

            alert("Password should be at least 6 characters.");

            e.preventDefault();

            return;
        }

    });

}


// -------------------------------
// Booking Validation
// -------------------------------

const bookingForm = document.querySelector("form");

if (bookingForm && window.location.pathname === "/booking") {

    bookingForm.addEventListener("submit", function (e) {

        const date = document.querySelector("input[name='date']").value;

        const today = new Date().toISOString().split("T")[0];

        if (date < today) {

            alert("Appointment date cannot be in the past.");

            e.preventDefault();

            return;
        }

    });

}


// -------------------------------
// Confirm Cancel Appointment
// -------------------------------

const cancelButtons = document.querySelectorAll(".cancel-btn");

cancelButtons.forEach(button => {

    button.addEventListener("click", function (e) {

        const confirmCancel = confirm(
            "Are you sure you want to cancel this appointment?"
        );

        if (!confirmCancel) {

            e.preventDefault();

        }

    });

});


// -------------------------------
// Smooth Scroll
// -------------------------------

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


// -------------------------------
// Highlight Active Navigation Link
// -------------------------------

const currentPage = window.location.pathname;

document.querySelectorAll("nav a").forEach(link => {

    if (link.getAttribute("href") === currentPage) {

        link.style.color = "#FFD700";
        link.style.fontWeight = "bold";

    }

});


// -------------------------------
// Welcome Message
// -------------------------------

console.log("Dental Booking System Loaded Successfully");