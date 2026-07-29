const form = document.getElementById("registerForm");
const message = document.getElementById("message");

form.addEventListener("submit", function(e){

    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value.trim();
    const gender = document.getElementById("gender").value;
    const mobile = document.getElementById("mobile").value.trim();
    const email = document.getElementById("email").value.trim();
    const address = document.getElementById("address").value.trim();
    const password = document.getElementById("password").value.trim();

    // Required field validation
    if(name === "" || age === "" || gender === "" ||
       mobile === "" || email === "" ||
       address === "" || password === ""){

        message.style.color = "red";
        message.innerText = "Please fill all fields";
        return;
    }

    // Mobile validation
    const mobilePattern = /^[0-9]{10}$/;

    if(!mobilePattern.test(mobile)){
        message.style.color = "red";
        message.innerText = "Enter valid 10-digit mobile number";
        return;
    }

    // Email validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if(!emailPattern.test(email)){
        message.style.color = "red";
        message.innerText = "Enter valid email";
        return;
    }

    // Password validation
    if(password.length < 6){
        message.style.color = "red";
        message.innerText = "Password must be at least 6 characters";
        return;
    }

    // Success message
    message.style.color = "green";
    message.innerText = "Registration Successful";

    // Example API data
    const userData = {
        name,
        age,
        gender,
        mobile,
        email,
        address,
        password
    };

    console.log(userData);

    // Backend API Example
    /*
    fetch("http://localhost:5000/register",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(userData)
    })
    */
});