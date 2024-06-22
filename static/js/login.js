function signup()
{
    document.querySelector(".Signup_Para").style.cssText = "display: none";
    document.querySelector(".login_Para").style.cssText = "display: block";
    document.querySelector(".login-form-container").style.cssText = "display: none;";
    document.querySelector(".signup-form-container").style.cssText = "display: block;";
    document.querySelector(".container").style.cssText = "background: linear-gradient(to bottom, rgb(56, 189, 149),  rgb(28, 139, 106));";
    document.querySelector(".button-1").style.cssText = "display: none";
    document.querySelector(".button-2").style.cssText = "display: block";

};

function login()
{
    document.querySelector(".Signup_Para").style.cssText = "display: block";
    document.querySelector(".login_Para").style.cssText = "display: none";
    document.querySelector(".signup-form-container").style.cssText = "display: none;";
    document.querySelector(".login-form-container").style.cssText = "display: block;";
    document.querySelector(".container").style.cssText = "background: linear-gradient(to bottom, rgb(6, 108, 224),  rgb(14, 48, 122));";
    document.querySelector(".button-2").style.cssText = "display: none";
    document.querySelector(".button-1").style.cssText = "display: block";

}


// Validate User and Password in Login

function validateLoginForm() {
    var email = document.forms["loginForm"]["email1"].value;
    var emailErrorField = document.getElementById("email-error");
    var password = document.forms["loginForm"]["password1"].value;
    var passwordErrorField = document.getElementById("password-error");
  
    // Validate Username
    if (email.trim() === "") {
      emailErrorField.innerText = "Please enter your email.";
      return false;
    } else{
      emailErrorField.innerText = "";
    }

    if (password.trim() === "") {
        passwordErrorField.innerText = "Please enter your password.";
        return false;
      } else{
        passwordErrorField.innerText = "";
      }

      return true;
}
