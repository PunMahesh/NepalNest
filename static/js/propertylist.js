document.addEventListener("DOMContentLoaded", function () {
  const formSteps = document.querySelectorAll(".form-step");
  const startSection = document.getElementById("startSection");
  const startBtn = document.getElementById("startBtn");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const Property_info = document.querySelector("#property_info");
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
    event.preventDefault(); // Prevent form submission
    startSection.style.display = "none";
    showStep(currentStep);
  });

  prevBtn.addEventListener("click", function () {
    if (currentStep > 0) {
      currentStep--;
      showStep(currentStep);
    }
  });

  nextBtn.addEventListener("click", function () {
    if (currentStep < formSteps.length - 1) {
      currentStep++;
      showStep(currentStep);
    }
  });

  // Add event listener to the "Next" button
  nextBtn.addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("title_preview").textContent = Property_info.elements.title.value || "N/A";
    document.getElementById("description_preview").textContent = Property_info.elements.description.value || "N/A";
    document.getElementById("price_preview").textContent = Property_info.elements.price.value || "N/A";
    document.getElementById("images_preview").textContent = Property_info.elements.images.value || "N/A";
    const pp_photo = Property_info.elements.PropertyPhot;
  readURL(pp_photo);
});

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      const pp_render = getElemById("pp_photo");
      pp_render.style.height = "150px";
      pp_render.style.width = "150px";
      pp_render.style.objectFit = "cover";
      pp_render.setAttribute('src', e.target.result);
    };

    reader.readAsDataURL(input.files[0]);
  }
}

});
