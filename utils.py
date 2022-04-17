
from bs4 import BeautifulSoup
import csv
import io
import requests

SCORE_URL = 'https://www.bien-dans-ma-ville.fr/classement-ville-global/?page={}'
SCORE_FILE = 'score.csv'
PRICE_URL = 'https://www.data.gouv.fr/fr/datasets/r/8fac6fb7-cd07-4747-8e0b-b101c476f0da'
PRICE_FILE = 'price.csv'


def scrap_cities_score():
    i = 1
    cities_score = list()
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
                cities_score.append({'city': city, 'score': score})
            i += 1
    fieldnames = ['city', 'score']
    with open(SCORE_FILE, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cities_score)
    return cities_score


def download_cities_price():
    r = requests.get(PRICE_URL)
    r.encoding = 'utf-8'
    csvio = io.StringIO(r.text, newline="")
    cities_price = list()
    for row in csv.DictReader(csvio, delimiter=';'):
        price = round(float(row['loypredm2'].replace(',', '.')), 2)
        cities_price.append({'insee': row['INSEE'], 'price': price})
    fieldnames = ['insee', 'price']
    with open(PRICE_FILE, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cities_price)
    return cities_price


if __name__ == '__main__':
    scrap_cities_score()
    download_cities_price()
