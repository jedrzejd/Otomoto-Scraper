import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict
from typing import List

import httpx
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils.logger import console_logger
from utils.logger import file_logger


class AdvertisementFetcher:
    """
        Fetches advertisements
        Args:
             features_file_path: path to file with features
    """
    MAX_THREADS = 8

    def __init__(self, features_file_path='resources/input/feats.txt'):
        self.features_file_path = os.path.join(os.getcwd(), features_file_path)
        self.all_features = self._read_features()
        self._cars = []

    def _read_features(self) -> List[str]:
        with open(self.features_file_path, 'r', encoding='utf-8') as featsFile:
            features = featsFile.readlines()
        return [x.strip() for x in features]

    def _make_line(self, main_features) -> Dict[str, str]:
        temp = {feat: main_features.get(feat, None)
                for feat in self.all_features}
        return temp

    def _download_url(self, path) -> Dict[str, str]:
        try:
            file_logger.info(f'Fetching {path}')
            headers = [
                {
                    'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/117.0.0.0 Safari/537.36',
                    'Accept':
                        'text/html,application/xhtml+xml,application'
                        '/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                        'q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language':
                        'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Referer':
                        'https://www.google.com/',
                },
                {
                    'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; '
                        'rv:109.0) Gecko/20100101 Firefox/109.0',
                    'Accept-Language': 'pl-PL,pl;q=0.9,en-US,en;q=0.7',
                    'Accept': 'text/html,application/xhtml+xml,application/'
                              'xml;q=0.9,image/avif,image/webp,'
                              'image/apng,*/*;q=0.8',
                    'Referer':
                        'https://www.google.com/',
                },
                {
                    'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15;'
                        ' rv:109.0) Gecko/20100101 Firefox/117.0',
                    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
                    'Accept': 'text/html,application/xhtml+xml,'
                              'application/xml;q=0.9,image/avif,'
                              'image/webp,*/*;q=0.8',
                    'Referer':
                        'https://www.google.com/',
                }
            ]
            header = random.choice(headers)
            res = httpx.get(path, headers=header)
            res = requests.get(path)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='lxml')
            for style_tag in soup.find_all('style'):
                style_tag.decompose()

            features = self._get_main_features(path, soup)

            extendend_features = self._get_extended_features(path, soup)
            features.update(extendend_features)

            price_feat = self._get_price(path, soup)
            features.update(price_feat)

            currency_feat = self._get_currency(path, soup)
            features.update(currency_feat)

            price_details_feat = self._get_price_details(path, soup)
            features.update(price_details_feat)

            features = self._make_line(features)

        except Exception as e:
            file_logger.error(f'Error {e} while fetching {path}')
            return None

        time.sleep(0.25)

        return features

    def _get_main_features(self, path, soup) -> Dict[str, str]:
        features = dict()
        try:
            main_params = soup.find(
                'div', attrs={'data-testid': 'advert-details-list'})
            for param in main_params.find_all(
                    'div',
                    attrs={'data-testid': 'advert-details-item'}
            ):
                try:
                    el = [x.text for x in param]
                    features.update({el[0]: el[1]})
                except Exception:
                    pass
        except Exception:
            try:
                main_params = soup.find_all(class_='offer-params__item')
                features = {
                    param.find(
                        'span',
                        class_='offer-params__label'
                    ).text.strip():
                        param.find(
                            'div',
                            class_='offer-params__value'
                    ).text.strip()
                    for param in main_params
                }
            except Exception as e:
                console_logger.error(
                    f'Error {e} while fetching main features from {path}')
                file_logger.error(
                    f'Error {e} while fetching main features from {path}')
                pass
        return features

    def _get_extended_features(self, path, soup) -> Dict[str, str]:
        features = dict()
        try:
            extendend_params = soup.find_all(
                'div',
                attrs={'data-testid': 'accordion-collapse-inner-content'}
            )
            for param in extendend_params:
                for x in param.find_all('p'):
                    try:
                        features[x.text.strip()] = 1
                    except Exception:
                        pass
        except Exception:
            try:
                extendend_params = soup.find_all(
                    'li', class_='parameter-feature-item')
                for param in extendend_params:
                    features[param.text.strip()] = 1
            except Exception as e:
                console_logger.error(
                    f'Error {e} while fetching extended features from {path}')
                file_logger.error(
                    f'Error {e} while fetching extended features from {path}')
                pass
        return features

    def _get_price(self, path, soup) -> Dict[str, str]:
        features = dict()
        try:
            price = ''.join(soup.select(
                'h3[class^="offer-price__number"]')[0].text.strip().split())
            features['Cena'] = price
        except Exception:
            try:
                price = ''.join(
                    soup.find('span',
                              class_='offer-price__number').text.
                    strip().split()[:-1]
                )
                features['Cena'] = price
            except Exception:
                features['Cena'] = None
                console_logger.info(f'Price not found in {path}')
                file_logger.info(f'Price not found in {path}')
        return features

    def _get_currency(self, path, soup) -> Dict[str, str]:
        features = dict()
        try:
            currency = ''.join(soup.select(
                'p[class^="offer-price__currency"]')[0].text.strip().split())
            features['Waluta'] = currency
        except Exception:
            try:
                currency = soup.find(
                    'span', class_='offer-price__currency').text.strip()
                features['Waluta'] = currency
            except Exception:
                features['Waluta'] = None
                console_logger.info(f'Currency not found in {path}')
                file_logger.info(f'Currency not found in {path}')
        return features

    def _get_price_details(self, path, soup) -> Dict[str, str]:
        features = dict()
        try:
            price_details = soup.find(
                'p',
                attrs={'data-testid': 'price-with-evaluation-labels'}
            ).text.strip()
            features['Szczegóły ceny'] = price_details
        except Exception:
            try:
                price_details = soup.find(
                    'span', class_='offer-price__details').text.strip()
                features['Szczegóły ceny'] = price_details
            except Exception:
                features['Szczegóły ceny'] = None
                file_logger.info(f'Price details not found in {path}')
        return features

    def fetch_ads(self, links):
        """ Fetches ads
            Args:
                 links: links
        """
        with ThreadPoolExecutor(
                max_workers=min(
                    self.MAX_THREADS,
                    len(links)
                )
        ) as executor:
            features = [
                executor.submit(self._download_url, link)
                for link in links
            ]
            for feature in features:
                result = feature.result()
                if result is not None and result['Cena'] is not None:
                    self._cars.append(result)

    def save_ads(self, model):
        """
            Saves ads
            Args:
                 model: model
        """
        file_logger.info(f'Saving {model} ads')
        file_logger.info(f'Found {len(self._cars)} ads')
        console_logger.info(f'Found {len(self._cars)} ads')
        pd.DataFrame(self._cars).to_csv(
            f'output/data/{model}.csv', index=False)
        file_logger.info(f'Saved {model} ads')

    def setup_fetcher(self):
        self._cars = []
