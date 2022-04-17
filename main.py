
from fastapi import FastAPI
import json
import requests

import utils

TOWN_URL = 'https://geo.api.gouv.fr/departements/{}/communes?fields=nom,code,codesPostaux,population&format=json&geometry=centre'

app = FastAPI()
cities_score = utils.scrap_cities_score()
cities_rent = utils.download_cities_rent()


@app.get("/")
def cities_root(department_code: int, area: int, max_rent: int) -> list:
    """API entry point, allowing to retrieve a list of cities filtered
    by department, area and the average rent.

    Args:
        department_code: The department code (eg. 64).
        area: The minimum area (eg. 50).
        max_rent: The maximum rent (eg. 800).

    Returns:
        A list containing the names of relevant cities, complete with average
        rents, ratings, postcodes and population.
    """
    cities = get_cities(department_code, area, max_rent)
    return cities


def get_cities(department_code: int, area: int, max_rent: int) -> list:
    """Retrieve a list of cities filtered
    by department, area and the average rent.

    Args:
        department_code: The department code.
        area: The minimum area.
        max_rent: The maximum rent.

    Returns:
        A list containing the names of relevant cities, complete with average
        rents, ratings, postcodes and population.
    """
    cities = get_cities_info(department_code)
    cities = filter_cities_by_rent(cities, area, max_rent)
    return cities


def get_cities_info(department_code: int) -> list:
    """Retrieve information (name, postal code, population, INSEE code)
    of all cities in a department.

    Args:
        department_code: The department code.

    Returns:
        A list containing for each city, its name, its postal code,
        its population and its INSEE code.
    """
    url = TOWN_URL.format(department_code)
    res = requests.get(url)
    cities_info = json.loads(res.content.decode('utf-8'))
    cities = list()
    for city_info in cities_info:
        city = {'name': city_info['nom'].lower(),
                'postal_code': city_info['codesPostaux'][0],
                'population': city_info['population'],
                'insee_code': city_info['code']}
        cities.append(city)
    return cities


def filter_cities_by_rent(cities: list, area: int, max_rent: int) -> list:
    """Filter a list of cities based on their average rent.

    Args:
        cities: List of cities.
        area: The minimum area.
        max_rent: The maximum rent.

    Returns:
        A list of cities with an average rent lower than the maximum rent.
    """
    global cities_rent
    global cities_score

    cities_filtered = list()
    for city in cities:
        rent = cities_rent[city['insee_code']]
        if area * rent <= max_rent:
            city['average_rent'] = rent
            try:
                city['score'] = cities_score[city['name']]
            except KeyError:
                pass
            else:
                cities_filtered.append(city)
    return cities_filtered
