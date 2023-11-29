const MARCHE_VITESSE_M_S = 1.1
const MARCHE_VITESSE_M_MIN = MARCHE_VITESSE_M_S * 60

var map = L.map("map").setView([46.6031, 1.8883], 6);
console.log("La carte a été créée avec succès.");
// Ajoutez une couche de carte (par exemple, OpenStreetMap)
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
attribution: "© OpenStreetMap contributors",
}).addTo(map);


// Gestionnaire d'événements pour le bouton
document.getElementById("bouton_gares").addEventListener("click", function (e) {
    let affichage = document.getElementById("bouton_gares_tgv").style.display === "none" ? "block": "none";
    document.getElementById("bouton_gares_tgv").style.display = affichage;
    document.getElementById("bouton_gares_ter").style.display = affichage;
    document.getElementById("bouton_gares_intercites").style.display = affichage;
});
document.getElementById("bouton_gares_tgv").addEventListener("click", function (e) {
    get_localisation(e.target.innerText);
});
document.getElementById("bouton_gares_ter").addEventListener("click", function (e) {
    get_localisation(e.target.innerText);
});
document.getElementById("bouton_gares_intercites").addEventListener("click", function (e) {
    get_localisation(e.target.innerText);
});

document.getElementById("bouton_villes").addEventListener("click", function (e) {
    get_localisation(e.target.innerText);
});
document.getElementById("bouton_clear").addEventListener("click", function (e) {
    map.eachLayer(function (layer) {
    if (layer instanceof L.Marker || layer instanceof L.Polyline || layer instanceof L.Circle) {
        map.removeLayer(layer);
    }
    });
});

function get_localisation(bouton) {
    // Appel de la fonction pour mettre à jour la carte avec les dernières coordonnées
    let checkbox = document.querySelector(
        "#bouton_checkbox_connexion"
    ).checked;

    console.log(bouton);

    let map_button = {
        villes: 0,
        gares_tgv: 1,
        gares_intercites: 2,
        gares_ter: 3,
    };

    fetch("/get_localisation", {
        method: "GET",
    })
        .then((response) => response.json())
        .then((data) => {
        console.log(data);
        update_markers(data[map_button[bouton]][0]);
        if (checkbox)
            update_connexions(
            data[map_button[bouton]][0],
            data[map_button[bouton]][1]
            );
        });
}

function update_markers(localisations) {
    // Ajouter des marqueurs pour chaque ville
    for (const key in localisations) {
        let nom = key;
        let coordonees = localisations[key];
        let latitude = coordonees[0];
        let longitude = coordonees[1];

        // Choisir la couleur du marqueur en fonction de la ville
        let markerColor = "blue"; // Vous pouvez personnaliser cela selon vos besoins
        let markerIcon = new L.Icon({
        iconUrl:
            "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-" +
            markerColor +
            ".png",
        shadowUrl:
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
        });

        L.marker([latitude, longitude], {
        icon: markerIcon,
        })
        .addTo(map)
            .bindPopup(nom);
        
        let temps_min = document.getElementById("bouton_number_duree").value
        let distance_m = temps_min * MARCHE_VITESSE_M_MIN

        make_circle(distance_m,latitude,longitude)

    }
}

function update_connexions(localisations, connexions) {
    // Ajouter des connexions entre les villes
    connexions.forEach(([nom1, nom2, temps]) => {
        const [latitude1, longitude1] = localisations[nom1];
        const [latitude2, longitude2] = localisations[nom2];

        let polyline = L.polyline(
        [
            [latitude1, longitude1],
            [latitude2, longitude2],
        ],
        { color: "blue", weight: 2 }
        ).addTo(map);
        // Ajouter un popup avec le temps sur la polyline
        polyline.bindPopup("Temps de trajet : " + temps + " minutes");

        let distance_m = temps * MARCHE_VITESSE_M_MIN
        let couleur = '#21f'

        make_circle(distance_m,latitude1,longitude1,couleur)
        make_circle(distance_m,latitude2,longitude2,couleur)

    });
}


function make_circle(distance,lat,lon,couleur) {



    var marker = L.marker([lat, lon]).addTo(map);
    var circle = L.circle([lat, lon], {
        color: "red",
        fillColor: couleur,
        fillOpacity: 0.2,
        radius: distance  // Specify the radius in meters
    }).addTo(map);
    
}


export { map,make_circle }

