function validateForm() {
  var username = document.forms["registrationForm"]["username"].value;
  var usernameErrorField = document.getElementById("username-error");
  var fullname = document.forms["registrationForm"]["full_name"].value;
  var NameerrorField = document.getElementById("fullname-error");
  var contact = document.forms["registrationForm"]["contact"].value;
  var contactErrorField = document.getElementById("contact-error");
  var email = document.forms["registrationForm"]["email"].value;
  var emailErrorField = document.getElementById("email-error");
  var password = document.forms["registrationForm"]["password1"].value;
  var passwordErrorField = document.getElementById("password-error");
  var confirmPassword = document.forms["registrationForm"]["password2"].value;
  var confirmPasswordErrorField = document.getElementById("confirm-password-error");

  // Validate Username
  if (username.trim() === "") {
    usernameErrorField.innerText = "Please enter your username.";
    return false;
  } else if (username.length < 5) {
    usernameErrorField.innerText = "Username must be at least 5 characters long.";
    return false;
  } else {
    usernameErrorField.innerText = "";
  }

  // Validate Email
  if (email.trim() === "") {
    emailErrorField.innerText = "Please enter your email address.";
    return false;
  } else if (!email.includes("@")) {
    emailErrorField.innerText = "Please enter a valid email address.";
    return false;
  } else {
    emailErrorField.innerText = "";
  }

  // Validate Full Name
  if (fullname.trim() === "") {
    NameerrorField.innerText = "Please enter your full name.";
    return false;
  } else if (fullname.trim().split(" ").length < 2) {
    NameerrorField.innerText =
      "Please enter your full name (first name and last name).";
    return false;
  } else if (fullname.length < 5) {
    NameerrorField.innerText = "Full name must be at least 5 characters long.";
    return false;
  } else {
    NameerrorField.innerText = "";
  }

  // Validate Contact
  if (contact.trim() === "") {
    contactErrorField.innerText = "Please enter your contact number.";
    return false;
  } else if (contact.length < 10 || isNaN(contact) || contact.startsWith("98")) {
    contactErrorField.innerText = "Please enter a valid contact number.";
    return false;
  } else {
    contactErrorField.innerText = "";
  }

  // Password validation
  if (password.trim === "") {
    passwordErrorField.innerText = "Please enter password.";
    return false;
  } else if (password.length < 8) {
    passwordErrorField.innerText ="Password must be at least 8 characters long.";
    return false;
  } else {
    passwordErrorField.innerText = "";
  }

  // Validate Confirm Password

  if (confirmPassword.trim() === "") {
    confirmPasswordErrorField.innerText = "Please enter password to confirm.";
    return false;
  } else{
    confirmPasswordErrorField.innerText = "";
  }

  // Confirm password validation
  if (password !== confirmPassword) {
    confirmPasswordErrorField.innerText = "Passwords do not match.";
    return false;
  } else {
    confirmPasswordErrorField.innerText = "";
  }

  return true;
}
