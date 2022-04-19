
from unittest import TestCase
from unittest.mock import Mock
from unittest import mock

import utils


class TestUtils(TestCase):

    @mock.patch('utils.scrap_city_score_from_one_page', return_value={})
    def test_scrapping_finished(
            self,
            scrap_mock: Mock):
        cities_score = utils.scrap_cities_score()

        scrap_mock.assert_called_once_with(1)
        self.assertEqual(cities_score, {})

    @mock.patch('utils.BeautifulSoup')
    @mock.patch('utils.requests')
    def test_scrapping_succeed(
            self,
            requests_mock: Mock,
            beautiful_mock: Mock):
        page = Mock()
        soup_mock = beautiful_mock.return_value
        section_mock = soup_mock.find.return_value
        tbody_mock = section_mock.find.return_value

        city_mock = Mock()
        city_mock.get_text.return_value = "City (11)"
        score_mock = Mock()
        score_mock.get_text.return_value = "3.6"
        tr_mock = Mock()
        tr_mock.find_all.return_value = [Mock(), city_mock, score_mock]
        tbody_mock.find_all.return_value = [tr_mock]

        cities_score = utils.scrap_city_score_from_one_page(page)

        requests_mock.get.assert_called_once_with(utils.SCORE_URL.format(page))
        res_mock = requests_mock.get.return_value
        beautiful_mock.assert_called_once_with(res_mock.content, 'html.parser')
        soup_mock.find.assert_called_once_with('section', id="classement")
        section_mock.find.assert_called_once_with('tbody')
        tbody_mock.find_all.assert_called_once_with('tr')
        tr_mock.find_all.assert_called_once_with('td')
        self.assertEqual(cities_score, {'city': 3.6})

    @mock.patch('utils.requests')
    def test_scrapping_failed(
            self,
            requests_mock: Mock):
        history_mock = Mock()
        history_mock.status_code = 301
        requests_mock.get().history = [history_mock]
        page = Mock()

        cities_score = utils.scrap_city_score_from_one_page(page)

        self.assertEqual(cities_score, {})

    @mock.patch('utils.DictReader', return_value=[{'loypredm2': '8,456789',
                                                   'INSEE': 'INSEE_CODE'}])
    @mock.patch('utils.StringIO')
    @mock.patch('utils.requests')
    def test_download_succeed(
            self,
            requests_mock: Mock,
            string_io_mock: Mock,
            reader_mock: Mock):
        res_mock = requests_mock.get.return_value
        res_mock.status_code = 200
        text_mock = Mock()
        res_mock.text = text_mock

        cities_rent = utils.download_cities_rent()

        string_io_mock.assert_called_once_with(text_mock, newline="")
        reader_mock.assert_called_once_with(string_io_mock.return_value,
                                            delimiter=";")
        self.assertEqual(cities_rent, {'INSEE_CODE': 8.46})

    @mock.patch('utils.requests')
    def test_download_failed(
            self,
            requests_mock: Mock):
        cities_rent = utils.download_cities_rent()

        self.assertEqual(cities_rent, {})
