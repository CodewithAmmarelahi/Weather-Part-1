import requests
import time
import os
from datetime import datetime

# ============================================================
# DEVELOPER AMMAR - PESHAWAR WEATHER MONITOR
# Weather source: WeatherAPI.com
# ============================================================

API_KEY = "ba9def58a1fd4985aa5142938261209"

LOCATION = "Peshawar, Pakistan"

UPDATE_INTERVAL = 60

CURRENT_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json"


# ============================================================
# Clear terminal
# ============================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ============================================================
# Get weather
# ============================================================

def get_weather():

    params = {
        "key": API_KEY,
        "q": LOCATION,
        "days": 7,
        "aqi": "yes",
        "alerts": "yes"
    }

    try:

        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if "current" not in data:
            print("❌ Current weather data missing.")
            return None

        if "forecast" not in data:
            print("❌ Forecast data missing.")
            return None

        return data

    except requests.exceptions.Timeout:

        print("❌ Weather server timed out.")

    except requests.exceptions.ConnectionError:

        print("❌ Internet connection error.")

    except requests.exceptions.HTTPError as error:

        try:
            error_data = response.json()

            if "error" in error_data:
                print(
                    "❌ WeatherAPI error:",
                    error_data["error"]["message"]
                )
            else:
                print("❌ HTTP error:", error)

        except Exception:
            print("❌ HTTP error:", error)

    except requests.exceptions.RequestException as error:

        print("❌ Request error:", error)

    except ValueError:

        print("❌ Invalid API response.")

    return None


# ============================================================
# Display current weather
# ============================================================

def display_current(data):

    current = data["current"]
    location = data["location"]

    print("=" * 65)
    print("              🌦️ PESHAWAR WEATHER MONITOR")
    print("=" * 65)

    # Temperature
    print(
        f"🌡️ Temperature       : "
        f"{current['temp_c']:.1f} °C"
    )

    # Feels like
    print(
        f"🥵 Feels Like        : "
        f"{current['feelslike_c']:.1f} °C"
    )

    # REAL humidity from WeatherAPI
    print(
        f"💧 Humidity          : "
        f"{current['humidity']}%"
    )

    # Wind
    print(
        f"💨 Wind Speed        : "
        f"{current['wind_kph']:.1f} km/h"
    )

    print(
        f"🧭 Wind Direction    : "
        f"{current['wind_dir']} "
        f"({current['wind_degree']}°)"
    )

    # Gust
    print(
        f"💨 Wind Gust         : "
        f"{current['gust_kph']:.1f} km/h"
    )

    # Pressure
    print(
        f"🧭 Pressure          : "
        f"{current['pressure_mb']:.1f} mb"
    )

    # Rain
    print(
        f"🌧️ Precipitation     : "
        f"{current['precip_mm']:.1f} mm"
    )

    # Cloud
    print(
        f"☁️ Cloud Cover       : "
        f"{current['cloud']}%"
    )

    # UV
    print(
        f"☀️ UV Index          : "
        f"{current['uv']:.1f}"
    )

    # Condition
    print(
        f"☁️ Condition         : "
        f"{current['condition']['text']}"
    )

    print("-" * 65)

    # API observation time
    print(
        f"🕒 Last Updated      : "
        f"{current['last_updated']}"
    )

    print(
        f"📍 Location          : "
        f"{location['name']}, "
        f"{location['region']}, "
        f"{location['country']}"
    )

    print(
        f"🌐 Coordinates       : "
        f"{location['lat']}, "
        f"{location['lon']}"
    )

    print(
        f"🕐 Timezone          : "
        f"{location['tz_id']}"
    )

    print(
        "📡 Source            : "
        "WeatherAPI.com"
    )

    print("=" * 65)


# ============================================================
# Today's forecast
# ============================================================

def display_today(data):

    today = data["forecast"]["forecastday"][0]

    day = today["day"]
    astro = today["astro"]

    print()
    print("📅 TODAY")
    print("-" * 65)

    print(
        f"🌡️ Maximum           : "
        f"{day['maxtemp_c']:.1f} °C"
    )

    print(
        f"🌡️ Minimum           : "
        f"{day['mintemp_c']:.1f} °C"
    )

    print(
        f"🌡️ Average           : "
        f"{day['avgtemp_c']:.1f} °C"
    )

    print(
        f"🥵 Max Feels Like    : "
        f"{day['avgtemp_c']:.1f} °C"
    )

    print(
        f"💨 Max Wind          : "
        f"{day['maxwind_kph']:.1f} km/h"
    )

    print(
        f"🌧️ Total Rain        : "
        f"{day['totalprecip_mm']:.1f} mm"
    )

    print(
        f"🌧️ Rain Chance       : "
        f"{day['daily_chance_of_rain']}%"
    )

    print(
        f"☀️ UV Index          : "
        f"{day['uv']:.1f}"
    )

    print(
        f"☁️ Condition         : "
        f"{day['condition']['text']}"
    )

    print(
        f"🌅 Sunrise           : "
        f"{astro['sunrise']}"
    )

    print(
        f"🌇 Sunset            : "
        f"{astro['sunset']}"
    )


# ============================================================
# 7 Day Forecast
# ============================================================

def display_7_day(data):

    forecast_days = data[
        "forecast"
    ]["forecastday"]

    print()
    print("📆 7-DAY FORECAST")
    print("-" * 65)

    for day_data in forecast_days:

        day = day_data["day"]

        date = datetime.strptime(
            day_data["date"],
            "%Y-%m-%d"
        )

        day_name = date.strftime("%A")

        print(
            f"{day_name:<10} "
            f"{date.strftime('%d %b')} | "
            f"🌡️ "
            f"{day['mintemp_c']:.0f}°"
            f"–"
            f"{day['maxtemp_c']:.0f}°C | "
            f"🌧️ "
            f"{day['daily_chance_of_rain']}% | "
            f"💨 "
            f"{day['maxwind_kph']:.0f} km/h | "
            f"{day['condition']['text']}"
        )


# ============================================================
# Next 6 hours
# ============================================================

def display_next_hours(data):

    today = data[
        "forecast"
    ]["forecastday"][0]

    hours = today["hour"]

    current_time = data[
        "current"
    ]["last_updated"]

    try:

        current_dt = datetime.strptime(
            current_time,
            "%Y-%m-%d %H:%M"
        )

    except ValueError:

        current_dt = datetime.now()

    print()
    print("⏱️ NEXT 6 HOURS")
    print("-" * 65)

    shown = 0

    for hour in hours:

        hour_dt = datetime.strptime(
            hour["time"],
            "%Y-%m-%d %H:%M"
        )

        if hour_dt >= current_dt:

            print(
                f"{hour_dt.strftime('%I:%M %p')} | "
                f"🌡️ {hour['temp_c']:.1f}°C | "
                f"💧 {hour['humidity']}% | "
                f"🌧️ {hour['chance_of_rain']}% | "
                f"💨 {hour['wind_kph']:.1f} km/h | "
                f"{hour['condition']['text']}"
            )

            shown += 1

            if shown >= 6:
                break


# ============================================================
# Main display
# ============================================================

def display_weather(data):

    clear_screen()

    display_current(data)

    display_today(data)

    display_next_hours(data)

    display_7_day(data)

    print()
    print("=" * 65)
    print("🔄 Auto-update        : Every 60 seconds")
    print("⌨️ Press CTRL+C to stop")
    print("=" * 65)


# ============================================================
# Main
# ============================================================

def main():

    if API_KEY == "YOUR_API_KEY_HERE":

        print()
        print("❌ YOU HAVE NOT ADDED YOUR WEATHERAPI KEY!")
        print()
        print("Open the code and change:")
        print()
        print('API_KEY = "YOUR_API_KEY_HERE"')
        print()
        print("to your real API key.")
        return

    print("🌦️ Starting Peshawar Weather Monitor...")
    print("📡 Connecting to WeatherAPI.com...")
    print()

    while True:

        start_time = time.monotonic()

        data = get_weather()

        if data is not None:

            display_weather(data)

        else:

            print()
            print("⚠️ Weather update failed.")
            print("🔄 Retrying in 60 seconds...")

        elapsed = (
            time.monotonic()
            - start_time
        )

        wait_time = max(
            0,
            UPDATE_INTERVAL - elapsed
        )

        try:

            time.sleep(wait_time)

        except KeyboardInterrupt:

            print()
            print("👋 Weather monitor stopped.")
            break


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("👋 Goodbye!")