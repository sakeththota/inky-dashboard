import os
import requests
from flask import Flask, render_template
from flask_font_awesome import FontAwesome
from datetime import datetime

app = Flask(__name__)
font_awesome = FontAwesome(app)

# Map Open-Meteo weather codes to description + Font Awesome icon
WEATHER_CODES = {
    0: {"desc": "Clear sky", "icon": "fa-sun"},
    1: {"desc": "Mainly clear", "icon": "fa-cloud-sun"},
    2: {"desc": "Partly cloudy", "icon": "fa-cloud-sun"},
    3: {"desc": "Overcast", "icon": "fa-cloud"},
    45: {"desc": "Fog", "icon": "fa-smog"},
    48: {"desc": "Depositing rime fog", "icon": "fa-smog"},
    51: {"desc": "Light drizzle", "icon": "fa-cloud-rain"},
    53: {"desc": "Moderate drizzle", "icon": "fa-cloud-rain"},
    55: {"desc": "Dense drizzle", "icon": "fa-cloud-rain"},
    56: {"desc": "Light freezing drizzle", "icon": "fa-cloud-sleet"},
    57: {"desc": "Dense freezing drizzle", "icon": "fa-cloud-sleet"},
    61: {"desc": "Slight rain", "icon": "fa-cloud-showers-heavy"},
    63: {"desc": "Moderate rain", "icon": "fa-cloud-showers-heavy"},
    65: {"desc": "Heavy rain", "icon": "fa-cloud-showers-heavy"},
    66: {"desc": "Light freezing rain", "icon": "fa-cloud-sleet"},
    67: {"desc": "Heavy freezing rain", "icon": "fa-cloud-sleet"},
    71: {"desc": "Slight snow fall", "icon": "fa-snowflake"},
    73: {"desc": "Moderate snow fall", "icon": "fa-snowflake"},
    75: {"desc": "Heavy snow fall", "icon": "fa-snowflake"},
    77: {"desc": "Snow grains", "icon": "fa-snowflake"},
    80: {"desc": "Slight rain showers", "icon": "fa-cloud-showers-heavy"},
    81: {"desc": "Moderate rain showers", "icon": "fa-cloud-showers-heavy"},
    82: {"desc": "Violent rain showers", "icon": "fa-cloud-showers-heavy"},
    85: {"desc": "Slight snow showers", "icon": "fa-snowflake"},
    86: {"desc": "Heavy snow showers", "icon": "fa-snowflake"},
    95: {"desc": "Thunderstorm", "icon": "fa-bolt"},
    96: {"desc": "Thunderstorm with slight hail", "icon": "fa-bolt"},
    99: {"desc": "Thunderstorm with heavy hail", "icon": "fa-bolt"},
}

@app.route("/")
def weather_dashboard():
    # Fetch weather data from Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 41.8781,
        "longitude": -87.6298,
        "current_weather": "true",
        "hourly": "temperature_2m,precipitation,weathercode,windspeed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum",
        "timezone": "America/Chicago"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract relevant data
    current_weather = data['current_weather']
    daily_forecast = data['daily']
    hourly_forecast = data['hourly']

    # Convert current windspeed from km/h to mph
    windspeed_mph = round(current_weather['windspeed'] * 0.621371, 1)

    # Prepare daily forecast
    forecast = []
    for i, day in enumerate(daily_forecast['time']):
        code = daily_forecast['weathercode'][i]
        forecast.append({
            "day": datetime.strptime(day, "%Y-%m-%d").strftime("%A"),
            "high": round(daily_forecast['temperature_2m_max'][i]),
            "low": round(daily_forecast['temperature_2m_min'][i]),
            "description": WEATHER_CODES.get(code, {"desc": "Unknown", "icon": "fa-sun"})["desc"],
            "icon": WEATHER_CODES.get(code, {"icon": "fa-sun"})["icon"]
        })

    # Prepare hourly forecast
    hourly_data = []
    for i, time_str in enumerate(hourly_forecast['time']):
        code = hourly_forecast['weathercode'][i]
        hourly_data.append({
            "time": datetime.strptime(time_str, "%Y-%m-%dT%H:%M").strftime("%H:%M"),
            "temperature": round(hourly_forecast['temperature_2m'][i]),
            "precipitation": hourly_forecast['precipitation'][i],
            "description": WEATHER_CODES.get(code, {"desc": "Unknown"})["desc"],
            "icon": WEATHER_CODES.get(code, {"icon": "fa-sun"})["icon"]
        })
    with open('static/dist/output.css') as f:
        tailwind_css = f.read()
        return render_template(
            "dashboard.html",
            tailwind_css=tailwind_css,
            units="imperial",
            title="Weather Dashboard",
            current_date=datetime.now().strftime("%a, %b %d"),
            last_refresh_time=datetime.now().strftime("%H:%M"),
            current_day_icon=WEATHER_CODES.get(current_weather['weathercode'], {"icon":"fa-sun"})["icon"],
            current_temperature=round((current_weather['temperature'])*(9/5)+32),
            temperature_unit="°F",
            forecast=forecast,
            data_points=[
                {
                    "icon": "fa-wind",
                    "label": "Wind",
                    "measurement": windspeed_mph,
                    "unit": "mph",
                },
                {"icon": "fa-sun", "label": "UV", "measurement": 3, "unit": ""},
            ],
            hourly_forecast=hourly_data,
            plugin_settings={
                "displayRefreshTime": "true",
                "displayMetrics": "true",
                "displayGraph": "true",
                "displayForecast": "true",
                "forecastDays": "3",
                "moonPhase": "true",
                "textColor": "#000",
            },
        )

if __name__ == "__main__":
    app.run(debug=True)

