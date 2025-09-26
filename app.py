from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def weather_dashboard():
    # Fake data to inject
    plugin_settings = {
        "displayRefreshTime": "true",
        "displayMetrics": "true",
        "displayGraph": "true",
        "displayForecast": "true",
        "forecastDays": "3",
        "moonPhase": "true",
        "textColor": "#000",
    }

    forecast = [
        {
            "day": "Today",
            "high": 80,
            "low": 65,
            "icon": "/static/sun.png",
            "moon_phase_icon": "/static/moon.png",
            "moon_phase_pct": 40,
        },
        {
            "day": "Tue",
            "high": 78,
            "low": 64,
            "icon": "/static/cloud.png",
            "moon_phase_icon": "/static/moon.png",
            "moon_phase_pct": 50,
        },
        {
            "day": "Wed",
            "high": 81,
            "low": 66,
            "icon": "/static/rain.png",
            "moon_phase_icon": "/static/moon.png",
            "moon_phase_pct": 60,
        },
    ]

    hourly_forecast = [
        {
            "time": f"{h}:00",
            "temperature": 65 + h,
            "precipitation": 0.1 * (h % 3),
            "rain": 0.02 * (h % 3),
        }
        for h in range(0, 12)
    ]

    return render_template(
        "dashboard.html",
        units="imperial",
        title="Weather Demo",
        current_date=datetime.now().strftime("%a, %b %d"),
        last_refresh_time=datetime.now().strftime("%H:%M"),
        current_day_icon="/static/sun.png",
        current_temperature=72,
        temperature_unit="°F",
        feels_like=74,
        forecast=forecast,
        data_points=[
            {
                "icon": "/static/wind.png",
                "label": "Wind",
                "measurement": 5,
                "unit": "mph",
            },
            {"icon": "/static/uv.png", "label": "UV", "measurement": 3, "unit": ""},
        ],
        hourly_forecast=hourly_forecast,
        plugin_settings=plugin_settings,
    )


if __name__ == "__main__":
    app.run(debug=True)
