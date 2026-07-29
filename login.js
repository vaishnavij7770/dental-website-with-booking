const form = document.getElementById("loginForm");
const message = document.getElementById("message");

form.addEventListener("submit", function(e){

    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    // Required validation
    if(email === "" || password === ""){
        message.style.color = "red";
        message.innerText = "Please fill all fields";
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

    // Example successful login
    message.style.color = "green";
    message.innerText = "Login Successful";

    // Backend API Example
    const loginData = {
        email,
        password
    };

    console.log(loginData);

    /*
    fetch("http://localhost:5000/login",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(loginData)
    })
    */

    // Redirect Example
    // window.location.href = "dashboard.html";

});