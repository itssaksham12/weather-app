from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        # Current weather
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"]
            }

            # 5-day forecast
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url)
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()["list"]
                # Pick one forecast per day (every 8 entries = 24 hrs)
                forecast = [forecast_data[i] for i in range(0, len(forecast_data), 8)][:5]
        else:
            error = "City not found. Please try again."

    return render_template("index.html", weather=weather, forecast=forecast, error=error)

if __name__ == "__main__":
    app.run(debug=True)