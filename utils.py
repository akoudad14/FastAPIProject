
import requests
from bs4 import BeautifulSoup
import csv
import io

SCORE_URL = 'https://www.bien-dans-ma-ville.fr/classement-ville-global/?page={}'
PRICE_URL = 'https://www.data.gouv.fr/fr/datasets/r/8fac6fb7-cd07-4747-8e0b-b101c476f0da'


def scrap_cities_score():
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
                score = tds[-1].get_text()
                cities_score[city] = score
            i += 1
    return cities_score


def download_cities_price():
    r = requests.get(PRICE_URL)
    r.encoding = 'utf-8'
    csvio = io.StringIO(r.text, newline="")
    cities_price = dict()
    for row in csv.DictReader(csvio, delimiter=';'):
        price = round(float(row['loypredm2'].replace(',', '.')), 2)
        cities_price[row['INSEE']] = price
    return cities_price
