# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import webbrowser
from recuperation import fetch_data_from_database

app = Flask(__name__)
socketio = SocketIO(app)


# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")


# Écoute des mises à jour de la base de données
@socketio.on("update_map")
def handle_update(data):
    print("Received message:", data)
    # Mettez à jour la carte avec les données de la base de données
    updated_data = fetch_data_from_database()
    socketio.emit("map_updated", updated_data)


if __name__ == "__main__":
    browser = webbrowser.get()
    browser.open("http://127.0.0.1:5000")
    # Exécutez le serveur Flask-SocketIO
    socketio.run(app, debug=True)
