const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", (e) => {
  navLinks.classList.toggle("open");

  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

navLinks.addEventListener("click", (e) => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

const scrollRevealOption = {
  distance: "50px",
  origin: "bottom",
  duration: 1000,
};

// header container
ScrollReveal().reveal(".header__container .section__subheader", {
  ...scrollRevealOption,
});

ScrollReveal().reveal(".header__container h1", {
  ...scrollRevealOption,
  delay: 500,
});

ScrollReveal().reveal(".header__container .btn", {
  ...scrollRevealOption,
  delay: 1000,
});

// room container
ScrollReveal().reveal(".room__card", {
  ...scrollRevealOption,
  interval: 500,
});

// feature container
ScrollReveal().reveal(".feature__card", {
  ...scrollRevealOption,
  interval: 500,
});

// news container
ScrollReveal().reveal(".news__card", {
  ...scrollRevealOption,
  interval: 500,
});








// for sign up and login form

const showPopupBtn = document.querySelector(".log-in");
const formPopup = document.querySelector(".form-popup");
const hidePopupBtn = document.querySelector(".form-popup .close-btn");
const loginSignupLink = document.querySelectorAll(".form-box .bottom-link a")

//Show form popup
showPopupBtn.addEventListener("click", () =>{
    document.body.classList.toggle("show-popup");
});

//Hide form popup
hidePopupBtn.addEventListener("click", () => {
    document.body.classList.remove("show-popup");
    formPopup.classList.remove("show-signup");
});

loginSignupLink.forEach(link =>{
    link.addEventListener("click", (e) =>{
        e.preventDefault();
        formPopup.classList[link.id === "signup-link" ? 'add' : 'remove']("show-signup");
    });
});

//Sign Up Form
const signUpBtn = document.querySelector(".sign-up");

//Show form popup
signUpBtn.addEventListener("click", () => {
    document.body.classList.toggle("show-popup");
    formPopup.classList.add("show-signup");
});

//Hide form popup
hidePopupBtn.addEventListener("click", () => {
    document.body.classList.remove("show-popup");
    formPopup.classList.remove("show-signup");
});






//json response

// JavaScript code to handle form submission and display error messages
document.querySelector('#login-form').addEventListener('submit', function(event) {
  event.preventDefault();
  
  // Fetch data from form fields
  const formData = new FormData(event.target);
  
  // Send form data to the server using AJAX
  fetch('/login/', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          // Update pop-up content with error message
          const errorRender = document.querySelector('.error-render');
          errorRender.textContent = data.error;
          errorRender.style.display = 'block'; // Make the error message visible
      } else {
          // Proceed with login process
          // For example, close the pop-up or redirect to another page
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
});
