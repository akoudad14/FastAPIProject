
from fastapi import FastAPI
import json
import requests

import utils

TOWN_URL = 'https://geo.api.gouv.fr/departements/{}/communes?fields=nom,code,codesPostaux,population&format=json&geometry=centre'

app = FastAPI()
cities_score = utils.scrap_cities_score()
cities_price = utils.download_cities_price()


@app.get("/")
def cities_root(departement_code: int, area: int, max_rent: int):
    cities = get_cities(departement_code, area, max_rent)
    return cities


def get_cities(departement_code: int, area: int, max_rent: int) -> list:
    global cities_price
    global cities_score

    cities = get_cities_info(departement_code)
    cities = filter_cities_by_price(cities, area, max_rent)
    return cities


def get_cities_info(department_code: int) -> list:
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


def filter_cities_by_price(cities: list, area: int, max_rent: int) -> list:
    global cities_price
    global cities_score

    cities_filtered = list()
    for city in cities:
        price = cities_price[city['insee_code']]
        if area * price <= max_rent:
            city['average_rent'] = price
            try:
                city['score'] = cities_score[city['name']]
            except KeyError:
                print(city['name'])
            else:
                cities_filtered.append(city)
    return cities_filtered
