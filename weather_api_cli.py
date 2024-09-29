import requests
from colorama import Fore, Style, init
import pandas as pd
from datetime import datetime, timedelta

# Initialize colorama
init()

# Define constants for the API
API_KEY = "feee6733ded762e828a82d2409526c5d"  # Replace with your API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city):
    """Fetch the weather details for the given city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Metric for Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data['cod'] != 200:
            print(f"{Fore.RED}Error fetching data: {data['message']}{Style.RESET_ALL}")
            return None

        return data

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

def get_historical_data(city):
    """Fetch historical weather data for today, yesterday, and tomorrow."""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Fetch today's weather
    today_data = fetch_weather_data(city)
    if today_data is None:
        return None

    # Prepare data for the table
    historical_data = {
        "Date": [],
        "Temperature (°C)": [],
        "Weather Condition": []
    }

    # Today
    historical_data["Date"].append(today.strftime('%Y-%m-%d'))
    historical_data["Temperature (°C)"].append(today_data['main']['temp'])
    historical_data["Weather Condition"].append(today_data['weather'][0]['description'])

    # Yesterday (replace this with an actual historical data API if needed)
    yesterday_data = fetch_weather_data(city)
    if yesterday_data is not None:
        historical_data["Date"].append(yesterday.strftime('%Y-%m-%d'))
        historical_data["Temperature (°C)"].append(yesterday_data['main']['temp'])
        historical_data["Weather Condition"].append(yesterday_data['weather'][0]['description'])

    # Tomorrow (mock data for now)
    tomorrow_data = fetch_weather_data(city)
    if tomorrow_data is not None:
        historical_data["Date"].append(tomorrow.strftime('%Y-%m-%d'))
        historical_data["Temperature (°C)"].append(tomorrow_data['main']['temp'])
        historical_data["Weather Condition"].append(tomorrow_data['weather'][0]['description'])

    return historical_data

def display_historical_forecast(data):
    """Display historical weather data in a colorful table format."""
    df = pd.DataFrame(data)
    print(f"\n{Fore.BLUE}Weather Data Table:{Style.RESET_ALL}\n")
    print(df.to_string(index=False))

def print_ascii_art():
    """Prints ASCII art for the title."""
    ascii_art = r"""
 ## ##   ##  ###  ##  ##   ##   ##    ##     #### ##   ## ##   ###  ##
##   ##  ##  ##   ##  ##   ##   ##     ##    # ## ##  ##   ##   ##  ##
####     ## ##    ##  ##   ##   ##   ## ##     ##     ##        ##  ##
 #####   ## ##     ## ##   ## # ##   ##  ##    ##     ##        ## ###
    ###  ## ###     ##     # ### #   ## ###    ##     ##        ##  ##
##   ##  ##  ##     ##      ## ##    ##  ##    ##     ##   ##   ##  ##
 ## ##   ##  ###    ##     ##   ##  ###  ##   ####     ## ##   ###  ##
 """
    print(Fore.MAGENTA + ascii_art + Style.RESET_ALL)

if __name__ == "__main__":
    print_ascii_art()  # Print ASCII art title
    while True:
        # Get city input from the user
        city = input(f"{Fore.YELLOW}Enter the city name in India to get the weather (or 'exit' to quit): {Style.RESET_ALL}")
        
        if city.lower() == 'exit':
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break

        historical_data = get_historical_data(city)
        if historical_data:
            display_historical_forecast(historical_data)
