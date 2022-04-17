
from bs4 import BeautifulSoup
import csv
import io
import requests

SCORE_URL = 'https://www.bien-dans-ma-ville.fr/classement-ville-global/?page={}'
PRICE_URL = 'https://www.data.gouv.fr/fr/datasets/r/8fac6fb7-cd07-4747-8e0b-b101c476f0da'


def scrap_cities_score() -> dict:
    """Retrieve cities score based on www.bien-dans-ma-ville.fr .

    Returns:
        A dict containing for each city (the key), the score (the value).
    """
    i = 1
    cities_score = dict()
    finished = False
    while not finished:
        url = SCORE_URL.format(i)
        res = requests.get(url)
        if res.history and res.history[0].status_code == 301:
            finished = True
        else:
            soup = BeautifulSoup(res.content, 'html.parser')
            section = soup.find('section', id="classement")
            tbody = section.find('tbody')
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                city = ' '.join(tds[1].get_text().split()[:-1]).lower()
                score = float(tds[-1].get_text())
                cities_score[city] = score
            i += 1
    return cities_score


def download_cities_rent() -> dict:
    """Retrieve the average rent of a city, identified by INSEE,
    based on www.data.gouv.fr .

    Returns:
        A dict containing for each insee code (the key), the rent (the value).
    """
    r = requests.get(PRICE_URL)
    r.encoding = 'utf-8'
    csvio = io.StringIO(r.text, newline="")
    cities_rent = dict()
    for row in csv.DictReader(csvio, delimiter=';'):
        rent = round(float(row['loypredm2'].replace(',', '.')), 2)
        cities_rent[row['INSEE']] = rent
    return cities_rent
