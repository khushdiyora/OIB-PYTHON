import requests

# OpenWeatherMap API key
API_KEY = 'c852eead5c82e25c17fdca6746618647'

def get_weather(location):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        if data['cod'] != 200:
            print('Error:', data.get('message', 'Location not found'))
            return

        weather_data = {
            'Location': data['name'],
            'Temperature': data['main']['temp'],
            'Description': data['weather'][0]['description'],
            'Icon URL': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            'Wind Speed': data['wind']['speed'],
        }

        print(f"Weather in {weather_data['Location']}:")
        print(f"Temperature: {weather_data['Temperature']}°C")
        print(f"Description: {weather_data['Description']}")
        print(f"Wind Speed: {weather_data['Wind Speed']} m/s")
        print(f"Icon: {weather_data['Icon URL']}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    location = input("Enter the location: ")
    get_weather(location)
