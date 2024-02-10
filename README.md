# Otomoto-Scraper

This program gets more than 95% advertisements from [otomoto.pl](https://otomoto.pl) with 227 features - [show features](feats.txt)

Link to the documentation: https://jedrzejd.github.io/Otomoto-Scraper/

---

## Table of content
* [General info](#General-info)
* [Installation](#Installation)
* [Usage](#Usage)
* [Technologies](#technologies)

## General info

Program saves datasets to ```output/data/``` directory.

Each the car brand has a separate file ```car_name.csv``` with data and have ```car.csv``` with all cars.

Results should be 12 hours later.



## Installation on Linux/Macos

* Download and install `Python 3.10.0`

    ```
    https://www.python.org/downloads/release/python-3100/
    ```
* Download this repository and unzip


* Create python virtual environment

```bash
python3 -m venv venv
```

* Active python virtual environment

```bash
. venv/bin/activate
```

* Install require packages

```bash
pip install -r Requirements.txt
```

### Usage

```bash
python3 scrap_cars.py
```

## Installation on Windows

* Download and install `Python 3.10.0`

    ```
    https://www.python.org/downloads/release/python-3100/
    ```
* Download this repository and unzip


* Create python virtual environment

```bash
py -m venv venv
```

* Active python virtual environment

```bash
venv\Scripts\activate
```

* Install require packages

```bash
pip install -r Requirements.txt
```

### Usage

```bash
py scrap_cars.py
```

## Technologies
- Python 3.10.0
- beautifulsoup4
- requests
