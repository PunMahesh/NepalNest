function calculateDays() {
    var checkInDate = new Date(document.getElementById("arrival").value);
    var checkOutDate = new Date(document.getElementById("departure").value);
    var numDays = Math.floor((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));

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

}