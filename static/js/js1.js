let loginDiv = document.getElementById("login-title");
let signupDiv = document.getElementById("signup-title")
let loginForm = document.getElementById("login-form")
let signupForm = document.getElementById("register-form")


loginDiv.addEventListener("click", () => {
    signupForm.style.display = "none";
    loginForm.style.display = "block";
    loginDiv.getElementsByTagName("p")[0].style.borderBottom = "1px solid gray"
    signupDiv.getElementsByTagName("p")[0].style.borderBottom = "none"

})

signupDiv.addEventListener("click", () => {
   
    loginForm.style.display = "none";
    signupForm.style.display = "block";
    signupDiv.getElementsByTagName("p")[0].style.borderBottom = "1px solid gray"
    loginDiv.getElementsByTagName("p")[0].style.borderBottom = "none"

})