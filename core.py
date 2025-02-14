import requests
import json
from config import API_KEY


BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='


def get_unit():
    while True:
        unit = input('Weather in Celsius or Fahrenheit: ').lower()
        if unit in ['c', 'celsius', 'metric']:
            return '&units=metric'
        elif unit in ['f', 'fahrenheit', 'imperial']:
            return '&units=imperial'


def get_weather(city, unit):
    url = f'{BASE_URL}{city}&appid={API_KEY}{unit}'

    try:
        # requests.get() sends an HTTP request, it will return an HTTP response
        response = requests.get(url)
        # raise an error if we don't get a 2xxx response status
        response.raise_for_status()
        # transform the response into json format, so that I can interpret the results. results will be of type 'dict'
        data = response.json()
        # use the json library to transform the dict to a string with an indentation of 4 aka. format the string
        formatted_data = json.dumps(data, indent=4)
        # print(formatted_data)

        # extract the temperature and round it
        country = data['sys']['country']
        description = data['weather'][0]['description']
        weather = round(data['main']['temp'])
        icon = data['weather'][0]['icon']

        return country, weather, description, icon

    except requests.exceptions.HTTPError as e1:
        print(f'HTTP Error: {e1}')
    except Exception as e2:
        print(f'Error - {e2}')


def get_city_name():
    while True:
        city = input('Hit me with a city name. I\'ll do the heavy lifting, you take the credit: ')
        if city:
            return city


def main():
    city_name = get_city_name()
    unit = get_unit()
    # test cases
    (_, temp, _, _) = get_weather(city_name, unit)
    # if there is an actual temp, and we did not get None from the get_weather() function: display
    if temp:
        print(f'The weather in {city_name} is:', temp)


if __name__ == '__main__':
    main()