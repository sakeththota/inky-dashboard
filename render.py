# render.py
import os
import asyncio
from flask import Flask, render_template
from flask_font_awesome import FontAwesome
from utils.weather import fetch_weather
from pyppeteer import launch
from PIL import Image
from inky.auto import auto

# Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
font_awesome = FontAwesome(app)
app.config['SERVER_NAME']='localhost:5000'

# Inky Impression 7.3" resolution
width, height = 800, 480

async def render_dashboard_to_png(output_path="dashboard.png"):
    weather_data = fetch_weather()

    with open('static/dist/output.css') as f:
        tailwind_css = f.read()
        with app.app_context():
            html = render_template("dashboard.html", **weather_data, tailwind_css=tailwind_css)

    browser = await launch(headless=True, args=['--no-sandbox', '--disable-web-security', '--allow-file-access-from-files'])
    page = await browser.newPage()

    await page.setViewport({'width': width, 'height': height})
    await page.setContent(html)
    await page.evaluate('''() => new Promise(resolve => setTimeout(resolve, 1000))''')

    await page.screenshot({'path': output_path, 'clip': {'x': 0, 'y': 0, 'width': width, 'height': height}})
    await browser.close()
    return output_path

def show_on_inky(image_path="dashboard.png"):
    inky_display = auto()
    inky_display.set_border(inky_display.WHITE)

    img = Image.open(image_path).resize(inky_display.resolution)
    inky_display.set_image(img)
    inky_display.show()

if __name__ == "__main__":
    try:
        png_path = asyncio.run(render_dashboard_to_png())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(render_dashboard_to_png())
    # show_on_inky(png_path)

