document.addEventListener("DOMContentLoaded", (event) => {
  updatePopupDates()
});
function updatePopupDates() {
  var newCheckInDate = document.getElementById("newCheckInDate").value;
  var newCheckOutDate = document.getElementById("newCheckOutDate").value;
  var price = document.getElementById("hidden_price").value;

  // Parse the selected dates
  var checkInDate = new Date(newCheckInDate);
  var checkOutDate = new Date(newCheckOutDate);

  // Check if both dates are valid
  if (!isNaN(checkInDate.getTime()) && !isNaN(checkOutDate.getTime())) {
    // Calculate the number of days between the check-in and check-out dates
    var numberOfDays = Math.floor(
      (checkOutDate - checkInDate) / (1000 * 60 * 60 * 24)
    );

    // Update the displayed dates and number of days in the popup content
    document.getElementById("popupCheckInDate").textContent = formatDate(checkInDate);
    document.getElementById("popupCheckOutDate").textContent = formatDate(checkOutDate);
    document.getElementById("popupNumOfDays").textContent = numberOfDays;

     // Calculate before service cost
     var beforeServiceCost = numberOfDays * price;
     document.getElementById("before_service_price").textContent = beforeServiceCost.toFixed(2);
      
     // Calculate service fee (10%)
     var serviceFee = 0.1 * beforeServiceCost;
     document.getElementById("service_fee").textContent = serviceFee.toFixed(2);
 
     // Calculate total cost
     var totalCost = beforeServiceCost + serviceFee;
     document.getElementById("after_service_price").textContent = totalCost.toFixed(2);
 
  }
}

// Function to format date as "M d"
function formatDate(date) {
  var month = date.toLocaleString("default", { month: "short" });
  var day = date.getDate();
  return month + " " + day;
}

// Open the popup
function openPopup() {
  // Create the overlay element
  var overlay = document.createElement("div");
  overlay.className = "overlay";

  // Add the overlay to the body
  document.body.appendChild(overlay);

  // Show the popup
  document.getElementById("editDatesPopup").style.display = "block";
}

// Close the popup
function closePopup() {
  // Hide the popup
  document.getElementById("editDatesPopup").style.display = "none";

  // Remove the overlay
  var overlay = document.querySelector(".overlay");
  document.body.removeChild(overlay);
}

// Update dates and close popup
function updateDates() {
  // Perform any validation if needed

  // Update dates in the main page paragraph
  document.getElementById("checkInDate").textContent =
    document.getElementById("popupCheckInDate").textContent;
  document.getElementById("checkOutDate").textContent =
    document.getElementById("popupCheckOutDate").textContent;

  // Close the popup
  closePopup();
}
