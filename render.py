import os
from flask import Flask, render_template
from flask_font_awesome import FontAwesome
from utils.weather import fetch_weather
import imgkit
from PIL import Image
from inky.auto import auto

app = Flask(__name__, template_folder="templates", static_folder="static")
font_awesome = FontAwesome(app)

def render_dashboard_to_png(output_path="dashboard.png"):
    # Get weather data
    weather_data = fetch_weather()

    # Render HTML with Jinja
    with app.app_context():
        css_path = f"file://{os.path.abspath('static/dist/output.css')}"
        html = render_template("dashboard.html", **weather_data, css_path=css_path)

    options = {
        "enable-local-file-access": None
    }

    # Convert HTML → PNG
    imgkit.from_string(html, output_path, options=options)

    return output_path

def show_on_inky(image_path="dashboard.png"):
    inky_display = auto()
    inky_display.set_border(inky_display.WHITE)

    # Load image
    img = Image.open(image_path).resize(inky_display.resolution)
    inky_display.set_image(img)
    inky_display.show()

if __name__ == "__main__":
    png = render_dashboard_to_png()
    show_on_inky(png)
