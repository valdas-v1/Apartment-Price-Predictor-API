# Aruodas.lt Apartment Price Predictor API
A Flask API able to predict the price of an apartment from provided attributes.
The model was trained on apartment data from Aruodas.lt with the help of the [scrape_aruodas](https://github.com/valdas-v1/scrape_aruodas) package.

Aruodas.lt Apartment Price Predictor API currently supports:
  - POST requests
  - Single or multiple apartment predictions with a single request
  - Storing the data in a remote Heroku database
  - Invalid input handling
### Upcomming Features!

  - Visual user interface

### Tech
Aruodas.lt Apartment Price Predictor API uses a number of open source projects to work properly:

* [Python](https://www.python.org/) - The programming language for of this project
* [Scrape_Aruodas](https://github.com/valdas-v1/scrape_aruodas) - Scrape_Aruodas is a web scraper designed to scrape Aruodas.lt apartment listings
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Flask is a lightweight WSGI web application framework
* [Scikit-learn](https://scikit-learn.org/stable/) - Scikit-learn is a free software machine learning library for the Python programming language
* [Pickle](https://docs.python.org/3/library/pickle.html) - Python object serialization
* [JSON](https://docs.python.org/3/library/json.html) - JSON encoder and decoder
* [NumPy](https://numpy.org/) - The fundamental package for scientific computing with Python

## Installation
* Aruodas.lt Apartment Price Predictor API requires at least Python version 3.7

#### Installation as a standalone python project:

1) Clone the repository to a local directory

2) Create a virtual environment
    ```sh
    $ python -m venv venv
    ```
3) Activate the virtual environment
    ```sh
    $ venv\Scripts\activate.bat
    ```

4) Install required libraries
    ```sh
    $ pip install git+https://github.com/valdas-v1/scrape_aruodas
    $ pip install -r requirements.txt
    ```

## Running the API
Run the API as any other Python file
```sh
$ python app.py
```

## Using the API
To use the API, make a POST request with the sample JSON structure of 
```JSON
{
    "inputs": [
        {
            "Area": 100,
            "Build year": 1985,
            "Building type": "Brick",
            "Equipment": "Fully equipped",
            "Floor": 1,
            "Heating system": "Central thermostat",
            "No. of floors": 9,
            "Number of rooms": 3,
            "Renovation year": 2010,
            "city": "Vilnius",
            "region": "Šnipiškės",
            "street": "Rinktinės g."
        }
    ]
}
```


Body of expected response
```JSON
{"predicted_prices": [225679.79271469155]}
```

License
----

[MIT](LICENSE)