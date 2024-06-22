document.addEventListener('DOMContentLoaded', function() {
    var typingTimer;                // Timer identifier
    var doneTypingInterval = 1000;  // Time in milliseconds (1 second)

    // Function to initialize Google Maps
    function initMap() {
        var map = new google.maps.Map(document.getElementById('map-canvas'), {
            center: { lat: 27.7172, lng: 85.3240 }, // Default center (Kathmandu)
            zoom: 12 // Default zoom level
        });
    
        // Retrieve latitude and longitude from hidden input fields
        var latitude = parseFloat(document.getElementById('latitude').value);
        var longitude = parseFloat(document.getElementById('longitude').value);
    
        // Check if latitude and longitude are valid numbers
        if (!isNaN(latitude) && !isNaN(longitude)) {              
            // Create a LatLng object for the retrieved location
            var location = { lat: latitude, lng: longitude };
    
            // Set the map center to the retrieved location
            map.setCenter(location);
    
            // Add a marker for the retrieved location
            var marker = new google.maps.Marker({
                map: map,
                position: location,
                draggable: true // You can set draggable to false if you don't want the marker to be draggable
            });
    
            // Add event listener for marker dragend event
            google.maps.event.addListener(marker, 'dragend', function() {
                // Get new marker position
                var newPosition = marker.getPosition();
    
                // Update hidden fields with latitude and longitude
                document.getElementById('latitude').value = newPosition.lat();
                document.getElementById('longitude').value = newPosition.lng();
            });
        }
    }

    // Function to update the map based on the address entered by the user
    function updateMap(address) {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({ 'address': address }, function(results, status) {
            if (status === 'OK') {
                var map = new google.maps.Map(document.getElementById('map-canvas'), {
                    center: results[0].geometry.location,
                    zoom: 12 // Adjust the zoom level as needed
                });

                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    draggable: true
                });

                // Update hidden fields with latitude and longitude
                document.getElementById('latitude').value = results[0].geometry.location.lat();
                document.getElementById('longitude').value = results[0].geometry.location.lng();

                // Update marker position and hidden fields when marker is dragged
                google.maps.event.addListener(marker, 'dragend', function() {
                    document.getElementById('latitude').value = marker.getPosition().lat();
                    document.getElementById('longitude').value = marker.getPosition().lng();

                    // Reverse geocode the new marker position to obtain address components
                    var geocoder = new google.maps.Geocoder();
                    geocoder.geocode({ 'location': marker.getPosition() }, function(results, status) {
                        if (status === 'OK') {
                            // Update input field with new street address
                            updateAddressFields(results);
                        } else {
                            alert('Geocode was not successful for the following reason: ' + status);
                        }
                    });
                });

                // Extract city, province, and postal code from geocoding results
                var address_components = results[0].address_components;
                var city = '';
                var province = '';
                var postal_code = '';
                for (var i = 0; i < address_components.length; i++) {
                    var component = address_components[i];
                    if (component.types.includes('locality')) {
                        city = component.long_name;
                    } else if (component.types.includes('administrative_area_level_1')) {
                        province = component.long_name;
                    } else if (component.types.includes('postal_code')) {
                        postal_code = component.long_name;
                    }
                }

                // Update input fields with city, province, and postal code
                document.getElementById('city_id').value = city;
                document.getElementById('province_id').value = province;
                document.getElementById('postal_code_id').value = postal_code;

                // Update street address field if it's empty
                if (document.getElementById('street_address_id').value.trim() === '') {
                    updateAddressFields(results);
                }
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }

    // Function to update the input fields with address components
    function updateAddressFields(results) {
        // Find address components from geocoding results
        var address_components = results[0].address_components;

        // Initialize variables for address components
        var street_address = '';

        // Loop through address components to find relevant information
        for (var i = 0; i < address_components.length; i++) {
            var component = address_components[i];
            if (component.types.includes('street_number') || component.types.includes('route')) {
                street_address += component.long_name + ' ';
            }
        }

        // If street address is empty, construct it from other components
        if (street_address.trim() === '') {
            var city = '';
            var province = '';
            var postal_code = '';

            // Loop through address components to find city, province, and postal code
            for (var i = 0; i < address_components.length; i++) {
                var component = address_components[i];
                if (component.types.includes('locality')) {
                    city = component.long_name;
                } else if (component.types.includes('administrative_area_level_1')) {
                    province = component.long_name;
                } else if (component.types.includes('postal_code')) {
                    postal_code = component.long_name;
                }
            }

            // Assemble street address from city, province, and postal code
            street_address = city + ', ' + province + ', ' + postal_code;
        }

        // Update input field with new street address
        document.getElementById('street_address_id').value = street_address.trim();
    }

    // Add event listener to the address input field for manual address entry
    document.getElementById('street_address_id').addEventListener('input', function() {
        clearTimeout(typingTimer);
        var address = document.getElementById('street_address_id').value;
        if (address) {
            typingTimer = setTimeout(function() {
                updateMap(address);
            }, doneTypingInterval);
        }
    });

    // Call initMap function to initialize the map
    initMap();
});
