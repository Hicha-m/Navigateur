from flask import Flask, render_template, request, send_from_directory
import folium

app = Flask(__name__)

# Initial marker location
current_location = [37.7749, -122.4194]


def generate_map(location):
    my_map = folium.Map(location=location, zoom_start=12)
    folium.Marker(location=location, popup="Hello, I am a marker!").add_to(my_map)
    return my_map


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/my_map")
def my_map():
    generate_map(current_location).save("app/templates/my_map.html")
    return send_from_directory("templates", "my_map.html")


@app.route("/update_location", methods=["POST"])
def update_location():
    global current_location
    if request.method == "POST":
        new_latitude = float(request.form["latitude"])
        new_longitude = float(request.form["longitude"])
        current_location = [new_latitude, new_longitude]
    return ""


if __name__ == "__main__":
    generate_map(current_location).save("app/templates/my_map.html")
    app.run(debug=True)
