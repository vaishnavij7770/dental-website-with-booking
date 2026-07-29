const cancelButtons = document.querySelectorAll(".cancel-btn");
const rescheduleButtons = document.querySelectorAll(".reschedule-btn");
const message = document.getElementById("message");

// Cancel Appointment

cancelButtons.forEach(button => {

    button.addEventListener("click", function(){

        message.style.color = "red";
        message.innerText = "Appointment Cancelled";

        // Backend API Example

        /*
        fetch("http://localhost:5000/cancel-appointment",{
            method:"POST"
        })
        */

    });

});

// Reschedule Appointment

rescheduleButtons.forEach(button => {

    button.addEventListener("click", function(){

        message.style.color = "green";
        message.innerText = "Redirecting to Reschedule Page";

        // Example Redirect

        // window.location.href = "booking.html";

    });

});