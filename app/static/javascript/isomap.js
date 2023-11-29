import { map,make_circle } from '/static/javascript/carte.js';


const MARCHE_VITESSE_M_S = 1.1
const MARCHE_VITESSE_M_MIN = MARCHE_VITESSE_M_S * 60


map.on("click", function (e) {
    var lat = e.latlng.lat;
    var lon = e.latlng.lng;
    console.log("Clicked at:", lat, lon);
    let temps_min = document.getElementById("bouton_number_duree").value
    let distance_m = temps_min * MARCHE_VITESSE_M_MIN
    let couleur = '#f03'
    make_circle(distance_m, lat, lon,couleur)


// Send the coordinates to the server
fetch("/update_marker", {
    method: "POST",
    headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `lat=${lat}&lon=${lon}`,
})
    .then((response) => response.json())
    .then((data) => updateMapWithLatestCoordinates(data));
});


function updateMapWithLatestCoordinates(data) {
    var lat = data.lat;
    var lon = data.lon;

    // Add a marker to the map
    var marker = L.marker([lat, lon]).addTo(map);

    console.log("Latest Coordinates:", lat, lon);
}


