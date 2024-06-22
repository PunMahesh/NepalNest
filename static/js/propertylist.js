document.addEventListener("DOMContentLoaded", function () {
  const formSteps = document.querySelectorAll(".form-step");
  const btngrp = document.getElementById("nextprevbtn");
  const startSection = document.getElementById("startSection");
  const startBtn = document.getElementById("startBtn");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const Property_info = document.querySelector("#property_info");
  const formContainer = document.getElementById("frmgrp");
  const submitBtn = document.getElementById("submitBtn"); // Added to fix the issue

  let currentStep = 0;

  function showStep(stepIndex) {
    formSteps.forEach((step, index) => {
      if (index === stepIndex) {
        step.style.display = "block";
      } else {
        step.style.display = "none";
      }
    });

    if (stepIndex === 0) {
      prevBtn.style.display = "none";
    } else {
      prevBtn.style.display = "block";
    }

    if (stepIndex === formSteps.length - 1) {
      nextBtn.style.display = "none";
      submitBtn.style.display = "block"; 
    } else {
      nextBtn.style.display = "block";
      submitBtn.style.display = "none"; 
    }
  }

  startBtn.addEventListener("click", function (event) {
    startSection.style.display = "none";
    formContainer.style.display = "flex";
    btngrp.style.display = "flex";
    btngrp.classList.add("rightAlign");
    showStep(currentStep);
  });

  prevBtn.addEventListener("click", function () {
    if (currentStep > 0) {
      currentStep--;
      showStep(currentStep);
    }
  });

  nextBtn.addEventListener("click", function () {
    // Check if all required fields in the current step are filled
    const currentStepFields = formSteps[currentStep].querySelectorAll("[required]");
    let allFieldsFilled = true;
    currentStepFields.forEach(field => {
      if (!field.value) {
        allFieldsFilled = false;
      }
    });
  
    // Check if there are any radio buttons in the current step
    const hasRadioButtons = formSteps[currentStep].querySelector("input[type='radio']") !== null;
  
    // Check if at least one radio button is checked (if there are radio buttons)
    let radioButtonChecked = true; // Assume true if there are no radio buttons
    if (hasRadioButtons) {
      const radioButtons = formSteps[currentStep].querySelectorAll("input[type='radio']");
      radioButtonChecked = false; // Reset to false for radio button check
      radioButtons.forEach(radioButton => {
        if (radioButton.checked) {
          radioButtonChecked = true;
        }
      });
    }
  
    // Check if the current step contains an image upload field and if the number of uploaded images is at least 5
    const isImageStep = formSteps[currentStep].querySelector("#imageUpload") !== null;
    const uploadedImages = isImageStep ? document.getElementById("imageUpload").files : [];
    const hasEnoughImages = isImageStep ? uploadedImages.length >= 5 : true;
  
    if (allFieldsFilled && (!hasRadioButtons || radioButtonChecked) && (!isImageStep || hasEnoughImages)) {
      if (currentStep < formSteps.length - 1) {
        currentStep++;
        showStep(currentStep);
        btngrp.classList.remove("rightAlign");
      }
    } else if (!allFieldsFilled) {
      // Show alert message for unfilled required fields
      alert("Please fill in all required fields before proceeding.");
    } else if (hasRadioButtons && !radioButtonChecked) {
      // Show alert message for unselected radio buttons
      alert("Please select at least one option before proceeding.");
    } else if (isImageStep && !hasEnoughImages) {
      // Show alert message for insufficient number of uploaded images
      alert("Please upload at least 5 images before proceeding.");
    }
  });
  
  
  
  




  // Event listener for the "Next" button
  nextBtn.addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("title_preview").textContent =
      Property_info.elements.title.value || "N/A";
    document.getElementById("location_preview").textContent =
      Property_info.elements.street_address.value + ", " + Property_info.elements.city.value || "N/A";
    document.getElementById("price_preview").textContent =
      Property_info.elements.price.value || "N/A";
  });

  const inputElement = document.getElementById("imageUpload");
  const previewImage = document.getElementById("pp_photo");

  inputElement.addEventListener('change', function() {
      readURL(this);
  });

  // Set the initial image from the database if available
  const firstImage = document.querySelector('.image-preview img');
  if (firstImage) {
    previewImage.src = firstImage.src;
  }
});

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      const pp_render = document.getElementById("pp_photo");
      pp_render.style.height = "150px";
      pp_render.style.width = "150px";
      pp_render.style.objectFit = "cover";
      pp_render.setAttribute("src", e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}
