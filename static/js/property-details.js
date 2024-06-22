function calculateDays() {
    var checkInDate = document.getElementById("arrival").value;
    var checkOutDate = document.getElementById("departure").value;

    // Check if both check-in and check-out dates are provided
    if (checkInDate && checkOutDate) {
        checkInDate = new Date(checkInDate);
        checkOutDate = new Date(checkOutDate);

        var numDays = Math.floor((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));

        // Ensure numDays is a valid number
        if (!isNaN(numDays) && numDays >= 0) {
            document.getElementById("num_days").textContent = numDays;

            var roomPrice = parseInt(document.getElementById("room_price").textContent);
            var beforeServicePrice = numDays * roomPrice;

            document.getElementById("before_service_price").textContent = beforeServicePrice;

            var serviceFee = beforeServicePrice * 0.1;
            document.getElementById("service_fee").textContent = serviceFee.toFixed(2);

            var afterServicePrice = beforeServicePrice + serviceFee;
            document.getElementById("after_service_price").textContent = afterServicePrice.toFixed(2);

            document.getElementById("total_price").value = afterServicePrice;
            document.getElementById("num_of_days").value = numDays;
            document.getElementById("before_service_fee").value = beforeServicePrice;
            document.getElementById("service_price").value = serviceFee;
        } else {
            // Display an error message or handle the case where numDays is not valid
            console.log("Invalid number of days");
        }
    } else {
        // Display an error message or handle the case where either check-in or check-out date is missing
        console.log("Please provide both check-in and check-out dates");
    }
}
