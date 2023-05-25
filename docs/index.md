# Otomoto Scraper

This program gets more than 95% advertisements from [otomoto.pl](https://otomoto.pl) with 227 features - [show features](https://github.com/jedrzejd/Otomoto-Scraper/blob/main/resources/input/feats.txt)

---
## Table Of Contents

1. [General info](#General-info)
2. [Code](code_docs.md)
3. [Installation](installation.md)
4. [Usage](#Usage)
5. [Technologies](#Technologies)

## General info
Program saves datasets to ```data/``` directory.

Each the car brand has a separate file ```car_name.xlsx``` with data and have ```car.xlsx``` with all cars.

Results should be 10 hours later.

Instalation instructions are in [installation.md](installation.md)

## Usage

Instructions on how to use OtoMoto Scraper.

### Linux usage

```bash
python3 scrap_cars.py
```

### Windows Usage

```bash
py scrap_cars.py
```

## Technologies
- Python 3.7
- beautifulsoup4
- requests
