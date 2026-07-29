const form = document.getElementById("bookingForm");
const message = document.getElementById("message");

form.addEventListener("submit", function(e){

    e.preventDefault();

    const doctor = document.getElementById("doctor").value;
    const treatment = document.getElementById("treatment").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;

    // Validation

    if(doctor === "" || treatment === "" ||
       date === "" || time === ""){

        message.style.color = "red";
        message.innerText = "Please fill all fields";
        return;
    }

    // Success Message

    message.style.color = "green";
    message.innerText = "Appointment Booked Successfully";

    // Booking Data

    const bookingData = {
        doctor,
        treatment,
        date,
        time
    };

    console.log(bookingData);

    // Backend API Example

    /*
    fetch("http://localhost:5000/book-appointment",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(bookingData)
    })
    */

});