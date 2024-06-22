// Get the pop-up element
var popup = document.getElementById("filterPopup");

// Get the button that opens the pop-up
var btn = document.getElementById("openPopupBtn");

// Get the <span> element that closes the pop-up
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the pop-up
btn.onclick = function () {
  popup.style.display = "block";
};

// When the user clicks on <span> (x), close the pop-up
function closePopup() {
  popup.style.display = "none";
}

// When the user clicks anywhere outside of the pop-up, close it
window.onclick = function (event) {
  if (event.target == popup) {
    popup.style.display = "none";
  }
};

document.getElementById('clearFiltersBtn').addEventListener('click', function() {
  // Reset the form
  document.getElementById('filterForm').reset();
});

// Get references to the search popup and its overlay
const searchPopup = document.getElementById('searchPopup');
const popupOverlay = document.getElementById('popupOverlay');

// Hide the search popup and its overlay initially
searchPopup.style.display = 'none';
popupOverlay.style.display = 'none';

// Get reference to the button that triggers the search popup
const showFormBtn = document.getElementById('showFormBtn');

// Add event listener to the button
showFormBtn.addEventListener('click', function() {
  // Show the search popup and its overlay
  searchPopup.style.display = 'block';
  popupOverlay.style.display = 'block';
});

// Close the search popup when clicking outside of it or pressing Esc key
document.addEventListener('click', function(e) {
  if (e.target === popupOverlay) {
    searchPopup.style.display = 'none';
    popupOverlay.style.display = 'none';
  }
});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    searchPopup.style.display = 'none';
    popupOverlay.style.display = 'none';
  }
});




// // Get the pop-up element
// var popup = document.getElementById("filterPopup");

// // Get the button that opens the pop-up
// var btn = document.getElementById("openPopupBtn");

// // Get the <span> element that closes the pop-up
// var span = document.getElementsByClassName("close")[0];

// // When the user clicks the button, open the pop-up
// btn.onclick = function () {
//   popup.style.display = "block";
// };

// // When the user clicks on <span> (x), close the pop-up
// function closePopup() {
//   popup.style.display = "none";
// }

// // When the user clicks anywhere outside of the pop-up, close it
// window.onclick = function (event) {
//   if (event.target == popup) {
//     popup.style.display = "none";
//   }
// };

// document.getElementById('clearFiltersBtn').addEventListener('click', function() {
//   // Reset the form
//   document.getElementById('filterForm').reset();
// });
// // Get references to the popup and its overlay
// const searchPopup = document.getElementById('searchPopup');
// const popupOverlay = document.getElementById('popupOverlay');

// // Get reference to the button that triggers the popup
// const showFormBtn = document.getElementById('showFormBtn');

// // Add event listener to the button
// showFormBtn.addEventListener('click', function() {
//   // Show the popup and its overlay
//   searchPopup.style.display = 'block';
//   popupOverlay.style.display = 'block';
// });

// // Close the popup when clicking outside of it or pressing Esc key
// document.addEventListener('click', function(e) {
//   if (e.target === popupOverlay) {
//     searchPopup.style.display = 'none';
//     popupOverlay.style.display = 'none';
//   }
// });

// document.addEventListener('keydown', function(e) {
//   if (e.key === 'Escape') {
//     searchPopup.style.display = 'none';
//     popupOverlay.style.display = 'none';
//   }
// });