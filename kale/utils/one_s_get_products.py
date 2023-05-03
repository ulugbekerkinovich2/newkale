import requests

from django.conf import settings

username = settings.ONE_S_USERNAME
password = settings.ONE_S_PASSWORD


def get_products():
    url = "http://94.158.52.249/Base/hs/info/stocks/"
    try:
        response = requests.get(url, auth=(username, password))
        # response.raise_for_status()  # raise an exception for any HTTP error status code
        json_data = response.json()
        return json_data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.JSONDecodeError as err:
        print(f"JSON decoding error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def get_latest_update_datetime():
    url = "http://94.158.52.249/Base/hs/info/stocksChangeDate/"
    try:
        response = requests.get(url, auth=(username, password))
        # response.raise_for_status()  # raise an exception for any HTTP error status code
        json_data = response.json()
        return json_data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.JSONDecodeError as err:
        print(f"JSON decoding error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
