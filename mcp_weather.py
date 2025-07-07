from fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
# Replace with your actual OpenWeatherMap API key
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

mcp = FastMCP("CurrentWeatherServer")

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """
    Get the current weather for a given city using OpenWeatherMap API.
    """
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENWEATHER_URL, params=params, timeout=10)
            
            # Better error handling for authorization issues
            if response.status_code == 401:
                return f"Authorization error: Invalid API key. Please check your OpenWeatherMap API key."
            elif response.status_code == 404:
                return f"City '{city}' not found. Please check the spelling."
            
            response.raise_for_status()
            data = response.json()
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data.get("wind", {}).get("speed", "N/A")
            return (f"Hi Sumit!, Current weather in {city}:\n"
                    f"{weather}, temperature: {temp}°C, feels like: {feels_like}°C.\n"
                    f"Humidity: {humidity}%, Wind speed: {wind_speed} m/s")
        except httpx.RequestError as e:
            return f"Network error: Could not retrieve weather data for {city}: {e}"
        except Exception as e:
            return f"Could not retrieve weather data for {city}: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")