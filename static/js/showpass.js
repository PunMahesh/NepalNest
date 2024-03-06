document.addEventListener("DOMContentLoaded", function () {
  var showPassword = document.getElementById("show-icon");
  var passwordField = document.querySelector("#password-input-field");

  showPassword.addEventListener("click", function () {
    this.classList.toggle("view-hide");
    const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
    passwordField.setAttribute("type", type);
  });
});
