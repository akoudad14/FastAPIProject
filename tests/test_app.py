
from unittest import TestCase
from unittest.mock import Mock
from unittest import mock

import app


class TestApp(TestCase):

    @mock.patch('app.json')
    @mock.patch('app.requests')
    def test_no_city(
            self,
            requests_mock: Mock,
            json_mock: Mock):
        json_mock.loads.return_value = []
        department_code = Mock()

        cities = app.get_cities_info(department_code)

        self.assertEqual(cities, [])
        town_url = app.TOWN_URL.format(department_code)
        requests_mock.get.assert_called_once_with(town_url)
        content_mock = requests_mock.get.return_value.content
        json_mock.loads.assert_called_once_with(content_mock.decode('utf-8'))

    @mock.patch('app.json')
    @mock.patch('app.requests')
    def test_get_cities(
            self,
            requests_mock: Mock,
            json_mock: Mock):
        json_mock.loads.return_value = [{'nom': 'Nom',
                                         'codesPostaux': ['code'],
                                         'population': 'population',
                                         'code': 'code'}]
        department_code = Mock()

        cities = app.get_cities_info(department_code)

        self.assertEqual(cities, [{'name': 'nom',
                                   'postal_code': 'code',
                                   'population': 'population',
                                   'insee_code': 'code'}])

    def test_filter_no_city(self):
        cities_filtered = app.filter_cities_by_rent([], Mock(), Mock())

        self.assertEqual(cities_filtered, [])

    def test_filter_cities_keep_nothing(self):
        city_rent = 10
        app.cities_rent = {'code': city_rent}

        cities = [{'insee_code': 'code'}]
        area = 50
        max_rent = 400
        cities_filtered = app.filter_cities_by_rent(cities, area, max_rent)

        self.assertEqual(cities_filtered, [])

    def test_filter_cities_keep_cities(self):
        city_rent = 10
        app.cities_rent = {'code': city_rent}
        city_score = 3.8
        app.cities_score = {'name': city_score}

        cities = [{'insee_code': 'code', 'name': 'name'}]
        area = 50
        max_rent = 500
        cities_filtered = app.filter_cities_by_rent(cities, area, max_rent)

        self.assertEqual(cities_filtered, [{'insee_code': 'code',
                                            'average_rent': city_rent,
                                            'score': city_score,
                                            'name': 'name'}])




