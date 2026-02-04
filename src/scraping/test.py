from base64 import b64decode
from pathlib import Path
import json

import pandas as pd
import requests
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "config"
URL_LIST_PATH = CONFIG_DIR / "url_list.ods"
API_KEYS_PATH = CONFIG_DIR / "api_keys.yaml"


def load_url_list():
    return pd.read_excel(URL_LIST_PATH, engine="odf")


def show_request_headers():
    response = requests.get("https://httpbin.org/headers")
    print(response.text)


def zyte_fetch(url_to_scrape="https://httpbin.org/anything"):
    with open(API_KEYS_PATH, "r", encoding="utf-8") as f:
        api_keys = yaml.safe_load(f)
    zyte_api_key = api_keys["zyte_api_key"]

    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=(zyte_api_key, ""),
        json={"url": url_to_scrape, "httpResponseBody": True},
    )
    api_response.raise_for_status()

    http_response_body = b64decode(api_response.json()["httpResponseBody"])
    return json.loads(http_response_body)["data"]


if __name__ == "__main__":
    df_url_list = load_url_list()
    print(df_url_list.head())

    show_request_headers()

    sample_body = zyte_fetch()
    print(sample_body)
