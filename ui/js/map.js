document.getElementById('mapBtn').addEventListener('click', () =>{
    var map = document.getElementById('mapArea');
    if (map.style.height != '400px'){
        map.style.height = '400px';
        map.style.width = '100%';
    }else {
        map.style.height = '0px';
        map.style.width = '0';
    }

});


var map, infoWindow;
function initMap() {
    map = new google.maps.Map(document.getElementById('mapArea'), {
        center: {
            lat: -1.2920659,
            lng: 36.8219462
        },
        zoom: 6
    });
    infoWindow = new google.maps.InfoWindow;

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            infoWindow.open(map);
            map.setCenter(pos);
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
}