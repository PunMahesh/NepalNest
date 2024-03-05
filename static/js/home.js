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

// // room container
// ScrollReveal().reveal(".room__card", {
//   ...scrollRevealOption,
//   interval: 500,
// });

// // feature container
// ScrollReveal().reveal(".feature__card", {
//   ...scrollRevealOption,
//   interval: 500,
// });

// // news container
// ScrollReveal().reveal(".news__card", {
//   ...scrollRevealOption,
//   interval: 500,
// });



// Get all input fields
var inputFields = document.querySelectorAll('.input-field input');

// Add event listeners to each input field
inputFields.forEach(function(input) {
    input.addEventListener('input', function() {
        // If input field is not empty, hide its label
        if (input.value.trim() !== '') {
            input.parentNode.querySelector('label').style.display = 'none';
        } else {
            // If input field is empty, show its label
            input.parentNode.querySelector('label').style.display = 'block';
        }
    });
});
