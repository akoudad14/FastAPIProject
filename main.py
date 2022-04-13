
from fastapi import FastAPI
import json
import requests

import utils

TOWN_URL = 'https://geo.api.gouv.fr/communes/{}?fields=nom,codesPostaux,population&format=json&geometry=centre'

app = FastAPI()
cities_score = utils.scrap_cities_score()
cities_price = utils.download_cities_price()


@app.get("/")
def read_root(departement_code: str, area: int, max_rent: int):
    global cities_price
    global cities_score

    cities = list()
    for insee_code, price in cities_price.items():
        average_rent = area * price
        if average_rent <= max_rent:
            url = TOWN_URL.format(insee_code)
            res = requests.get(url)
            if res.status_code == 200:
                city = json.loads(res.content.decode('utf-8'))
                if city['codeDepartement'] == departement_code:
                    city_name = city['nom'].lower()
                    try:
                        score = cities_score[city_name]
                    except KeyError:
                        pass
                    else:
                        cities.append({
                            'name': city_name,
                            'postal_code': city['codesPostaux'][0],
                            'population': city['population'],
                            'average_rent': average_rent,
                            'score': score
                        })
    return cities
