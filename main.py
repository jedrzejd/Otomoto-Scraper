import os
from modules.scrapers.car_scraper import CarScraper


if __name__ == "__main__":
    car_scraper = CarScraper('resources/input/car_models.txt', 'output/data')
    car_scraper.scrap_all_models()
    car_scraper.combine_data()
