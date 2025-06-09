from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        
        if not city:
            error = "Please enter a city name."
            return render_template("index.html", weather=weather, forecast=forecast, error=error)
        
        if not API_KEY:
            error = "API key not configured. Please check your .env file."
            return render_template("index.html", weather=weather, forecast=forecast, error=error)

        print(f"Searching weather for: {city}")
        print(f"API Key exists: {'Yes' if API_KEY else 'No'}")
        
        # Current weather
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(weather_url, timeout=10)
            print(f"Weather API Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": round(data["main"]["temp"]),
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                    "feels_like": round(data["main"]["feels_like"]),
                    "humidity": data["main"]["humidity"]
                }

                # 5-day forecast
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                forecast_response = requests.get(forecast_url, timeout=10)
                
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()["list"]
                    # Get one forecast per day (every 8th entry ≈ 24 hours)
                    forecast = []
                    for i in range(0, min(len(forecast_data), 40), 8):
                        forecast_item = forecast_data[i]
                        forecast.append({
                            "date": forecast_item["dt_txt"].split(" ")[0],
                            "temp": round(forecast_item["main"]["temp"]),
                            "description": forecast_item["weather"][0]["description"].title(),
                            "icon": forecast_item["weather"][0]["icon"]
                        })
                    forecast = forecast[:5]  # Limit to 5 days
                    
            elif response.status_code == 401:
                error = "Invalid API key. Please check your OpenWeatherMap API key."
            elif response.status_code == 404:
                error = f"City '{city}' not found. Please check the spelling and try again."
            else:
                error = f"Unable to fetch weather data. Error code: {response.status_code}"
                
        except requests.exceptions.Timeout:
            error = "Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            error = f"Network error: {str(e)}"
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template("index.html", weather=weather, forecast=forecast, error=error)

if __name__ == "__main__":
    app.run(debug=True)