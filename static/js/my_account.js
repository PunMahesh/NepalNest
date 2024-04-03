function validateAddress(address) {
  // Trim the address to remove leading/trailing whitespace
  address = address.trim();

  // Check if the address is empty
  if (address === "") {
    return false; // Address is empty
  }

  // Check if the address exceeds maximum length (adjust as needed)
  if (address.length > 100) {
    return false; // Address is too long
  }

  // Check for a basic format (alphanumeric characters, commas, periods, dashes, spaces)
  var basicFormatRegex = /^[a-zA-Z0-9\s.,-]+$/;
  if (!basicFormatRegex.test(address)) {
    return false; // Address contains invalid characters
  }

  return true;
}

function validateprofileForm() {
  // Get form inputs
  var email = document.forms["profileForm"]["email"].value;
  var fullname = document.forms["profileForm"]["full_name"].value;
  var contact = document.forms["profileForm"]["contact"].value;
  var address = document.forms["profileForm"]["address"].value;

  // Define regular expressions for validation
  var emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  var contactRegex = /^98\d{8}$/; // Contact starts with 98 and followed by 8 digits
  var fullnameRegex = /^[a-zA-Z]+(\s[a-zA-Z]+)+$/; // At least two names with a space in between

  // Reset previous errors
  document.getElementById("email-error").innerHTML = "";
  document.getElementById("fullname-error").innerHTML = "";
  document.getElementById("contact-error").innerHTML = "";
  document.getElementById("address-error").innerHTML = "";

  // Validate email
  if (!emailRegex.test(email)) {
    document.getElementById("email-error").innerHTML =
      "Please enter a valid email address";
    return false;
  }

  // Validate fullname
  if (!fullnameRegex.test(fullname)) {
    document.getElementById("fullname-error").innerHTML =
      "Please enter your full name with at least two names separated by space";
    return false;
  }

  // Validate contact
  if (!contactRegex.test(contact)) {
    document.getElementById("contact-error").innerHTML =
      "Please enter a valid 10-digit contact number starting with 98";
    return false;
  }

  // Validate address
  if (!validateAddress(address)) {
    document.getElementById("address-error").innerHTML =
      "Please enter a valid address (alphanumeric characters, commas, periods, dashes, spaces)";
    return false;
  }

  // If all validations pass, return true to submit the form
  return true;
}




function validatePasswordForm() {
    var password = document.forms["passwordForm"]["new_password1"].value;
    var passwordErrorField = document.getElementById("password-error");
    var confirmPassword = document.forms["passwordForm"]["new_password2"].value;
    var confirmPasswordErrorField = document.getElementById("confirm-password-error");
  
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
  