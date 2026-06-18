const form = document.getElementById("registerForm");
const message = document.getElementById("message");

form.addEventListener("submit", function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const age = document.getElementById("age").value.trim();
    const gender = document.getElementById("gender").value;
    const mobile = document.getElementById("mobile").value.trim();
    const email = document.getElementById("email").value.trim();
    const address = document.getElementById("address").value.trim();
    const password = document.getElementById("password").value.trim();

    if (name === "" || age === "" || gender === "" ||
        mobile === "" || email === "" || address === "" ||
        password === "") {

        message.style.color = "red";
        message.innerText = "Please fill all fields";
        return;
    }
});