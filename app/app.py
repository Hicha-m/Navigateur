# app.py
from flask import Flask, render_template, request, jsonify

from navigateur.fonctions.setup_graphe import setup_g_villes, setup_g_gares

app = Flask(__name__)


g_villes, dicte_villes, connexions_villes = setup_g_villes()
g_gares_tgv, dicte_Gares_tgv, connexions_gares_tgv = setup_g_gares(
    "export_gtfs_voyages"
)
g_gares_intercites, dicte_Gares_intercites, connexions_gares_intercites = setup_g_gares(
    "export-intercites-gtfs-last"
)
g_gares_ter, dicte_Gares_ter, connexions_gares_ter = setup_g_gares(
    "export-ter-gtfs-last"
)


# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/carte")
def carte():
    return render_template("carte.html")


@app.route("/update_marker", methods=["POST"])
def update_marker():
    lat = float(request.form["lat"]) + 1
    lon = float(request.form["lon"]) + 1
    latest_coordinates = {"lat": lat, "lon": lon}
    print(f"New Marker: Latitude={lat}, Longitude={lon}")

    return jsonify(latest_coordinates)


@app.route("/get_localisation", methods=["GET"])
def get_localisation():
    return jsonify(
        [dicte_villes, connexions_villes],
        [dicte_Gares_tgv, connexions_gares_tgv],
        [dicte_Gares_intercites, connexions_gares_intercites],
        [dicte_Gares_ter, connexions_gares_ter],
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    # Exécutez le serveur Flask
    app.run(debug=True)
    # http://127.0.0.1:5000
