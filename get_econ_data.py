import os
import requests
from datetime import date
from dotenv import load_dotenv
import streamlit as st
from typing import Optional


# Load local .env only if it exists (i.e., you're not in Streamlit Cloud)
load_dotenv()

def get_key(key_name: str) -> Optional[str]:
    """Function to get a key from an environment variable.
    First checks for key in st.secrets (key location in production
    environment). If that fails, fetches from local .env file. Can
    use app in local or production without changing code."""
    try:
        return st.secrets[key_name]
    except st.errors.StreamlitSecretNotFoundError:
        return os.getenv(key_name)



key = get_key("FRED_API_KEY")


# To get start and end observation dates, create today date object; create
# end_date object by changing today.day to 01; create start_date object by
# subtracting 2 from end_date.year (we subtract 2 from year to capture
# enough data  so that we have the last available 12 month numbers); convert
# start and end dates to strings to use a parameters in the endpoint url;


def get_current_inflation_rate():
    today = date.today()
    end_date = today
    start_date = date.fromisoformat(f"{end_date.year - 2}-{str(end_date.month).zfill(2)}-01")  # use zfill to pad single digit months with leading 0 for proper date object format
    end_date = str(end_date)
    start_date = str(start_date)
    # print(end_date)
    # print(start_date)

    # FRED Inflation Endpoint
    url = (
        f"https://api.stlouisfed.org/fred/series/observations?series_id"
        f"=CPIAUCSL&api_key={key}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    )

    response = requests.get(url)
    data = response.json()
    # pprint(data)
    # set end_value to the last available value by using [-1] slice on the results;
    # set start_value by selecting 12 values back [-13] slice on results
    start_value = float(data["observations"][-13]["value"])
    end_value = float(data["observations"][-1]["value"])
    rate = ((end_value - start_value) / start_value) * 100
    return f"{rate:.1f}", data["observations"][-1]["date"]


def get_current_unemployment_rate():
    today = date.today()
    end_date = today
    start_date = date.fromisoformat(f"{end_date.year - 1}-{str(end_date.month).zfill(2)}-01")
    end_date = str(end_date)
    start_date = str(start_date)
    # print(end_date)
    # print(start_date)

    # FRED Unemployment Endpoint
    url = (
        f"https://api.stlouisfed.org/fred/series/observations?series_id"
        f"=UNRATE&api_key={key}&file_type=json&observation_start"
        f"={start_date}&observation_end={end_date}"
    )

    response = requests.get(url)
    data = response.json()
    # pprint(data)
    # set end_value to the last available value by using [-1] slice on the results;
    # set start_value by selecting 12 values back [-13] slice on results
    # start_value = float(data['observations'][-13]['value'])
    # end_value = float(data['observations'][-1]['value'])
    # rate = ((end_value - start_value) / start_value) * 100
    # return f"{rate:.1f}", data["observations"][-1]["date"]
    return data["observations"][-1]["value"], data["observations"][-1]["date"]


def get_current_gas_price():
    today = date.today()
    end_date = today
    start_date = date.fromisoformat(f"{end_date.year - 1}-{str(end_date.month).zfill(2)}-01")
    end_date = str(end_date)
    start_date = str(start_date)
    # print(end_date)
    # print(start_date)

    # FRED Gas Price Endpoint
    url = (
        f"https://api.stlouisfed.org/fred/series/observations?series_id"
        f"=GASREGW&api_key={key}&file_type=json&observation_start"
        f"={start_date}&observation_end={end_date}"
    )

    response = requests.get(url)
    data = response.json()
    # pprint(data)
    # set end_value to the last available value by using [-1] slice on the results;
    # set start_value by selecting 12 values back [-13] slice on results
    # start_value = float(data['observations'][-13]['value'])
    # end_value = float(data['observations'][-1]['value'])
    # rate = ((end_value - start_value) / start_value) * 100
    # return f"{rate:.1f}", data["observations"][-1]["date"]
    return data["observations"][-1]["value"], data["observations"][-1]["date"]


def get_current_cost_of_eggs():
    today = date.today()
    end_date = today
    start_date = date.fromisoformat(f"{end_date.year - 1}-{str(end_date.month).zfill(2)}-01")
    end_date = str(end_date)
    start_date = str(start_date)

    # FRED Egg Price Endpoint
    url = (
        f"https://api.stlouisfed.org/fred/series/observations?series_id"
        f"=APU0000708111&api_key={key}&file_type=json&observation_start"
        f"={start_date}&observation_end={end_date}"
    )

    response = requests.get(url)
    data = response.json()

    return data["observations"][-1]["value"], data["observations"][-1]["date"]


def get_current_thirty_year_conventional_mortgage_rate():
    today = date.today()
    end_date = today
    start_date = date.fromisoformat(f"{end_date.year - 1}-{str(end_date.month).zfill(2)}-01")
    end_date = str(end_date)
    start_date = str(start_date)

    # FRED Thirty Year Conventional Mortgage Endpoint
    url = (
        f"https://api.stlouisfed.org/fred/series/observations?series_id"
        f"=MORTGAGE30US&api_key={key}&file_type=json&observation_start"
        f"={start_date}&observation_end={end_date}"
    )

    response = requests.get(url)
    data = response.json()

    return data["observations"][-1]["value"], data["observations"][-1]["date"]


if __name__ == "__main__":
    print(get_current_thirty_year_conventional_mortgage_rate())
