  
  window.initMap = initMap;
  
  // Initialize and add the map
function initMap() {
    let markers = []

    fetch('all_been')
      .then(response => response.json())
      .then(trips => {
      // Print trips
      console.log(trips);
      for (let i = 0; i < trips.length; i++) {
        markers.push(trips[i])
      }

    const world = { lat: 20, lng: 0 };
    // The map, centered at center
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 2,
        center: world,
    });
  
    for (let i = 0; i < markers.length; i++) {
        codeAddress(markers[i], map)
    }
    });
}

  function codeAddress(trip, map) {
    var contentString = `<h5>${trip.fields.location}</h5>` +
    `<p><input type='hidden' name='search' value='${trip.fields.location}'></p>
    <button class="mapButton" type="submit">View All Trips For <strong class="tag_name">${trip.fields.location}</strong></button>`;
    var geocoder;
    geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': trip.fields.location}, function(results, status) {
      if (status == 'OK') {
        const infowindow = new google.maps.InfoWindow({
          content: contentString,
          ariaLabel: "Uluru",
        });
        var marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location,
            title: trip.fields.location
        });
        marker.addListener("click", () => {
          infowindow.open({
            anchor: marker,
            map: map,
          });
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }