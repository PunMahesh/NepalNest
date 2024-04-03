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




// // Display block for search so that No Results is Found does not appear
// document.addEventListener("DOMContentLoaded", function() {
//   var searchInput = document.getElementById("search_input");
//   var searchButton = document.getElementById("search_button");
//   var searchResults = document.getElementById("search_results");

//   searchButton.addEventListener("click", function() {
//     // Toggle display of search results based on the input value
//     if (searchInput.value.trim() !== "") {
//       searchResults.style.display = "block";
//     } else {
//       searchResults.style.display = "none";
//     }
//   });
// });
