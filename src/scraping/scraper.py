from pathlib import Path
import os
import random
import time

import pandas as pd
import requests
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "config"
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
URL_LIST_PATH = CONFIG_DIR / "url_list.ods"
API_KEYS_PATH = CONFIG_DIR / "api_keys.yaml"
CA_CERT_PATH = CONFIG_DIR / "zyte-ca.crt"


class Car:
    def __init__(self, brand, model, segment, body_type, brand_id, model_id, first_url, flag_load,
                 pages, destination_folder, main_url):
        self.brand = brand
        self.model = model
        self.segment = segment
        self.body_type = body_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.first_url = first_url
        self.flag_load = flag_load
        self.pages = pages
        self.destination_folder = destination_folder
        self.main_url = main_url


def scrape_data(base_url, max_pages, output_folder=DATA_RAW_DIR):
    """
    Scrape HTML content from multiple pages with increasing page numbers
    and save each page's content in separate files.

    Parameters:
    - base_url (str): The base URL without the page number.
    - max_pages (int): The maximum number of pages to download.
    - output_folder (str): Folder to save raw HTML content.

    Returns:
    - None
    """
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    for page_number in range(1, max_pages + 1):
        if page_number == 1: 
            page_url = base_url
        else: 
            page_url = f"{base_url}&pg={page_number}"
            
        html_content = get_html_content_zyte(page_url)


        if html_content:
            save_html_content(html_content, output_folder, page_number)
        else:
            print(f"Failed to retrieve data from page {page_number}")
        
        time.sleep(random.uniform(5.5, 20.8))


def read_master_cars(file_path=URL_LIST_PATH):
    df = pd.read_excel(file_path, engine="odf")
    return df


def url_table_to_car_class(file_path=URL_LIST_PATH):
    df_url_list = pd.read_excel(file_path, engine="odf")
    cars = [Car(**row) for row in df_url_list.to_dict(orient="records")]
    return cars


# =============================================================================
# def get_html_content(url):
#     
#     # Retrieve HTML content from a given URL.
# 
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "es-ES,en;q=0.9",
#         "Referer": "https://www.bing.com/"
#         # Add more headers if needed
#     }
# 
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return response.text
#     except requests.RequestException as e:
#         print(f"Error fetching URL {url}: {e}")
#         return None
#     
# =============================================================================

def get_html_content_zyte(url, api_keys_path=API_KEYS_PATH, ca_cert_path=CA_CERT_PATH):
    
    #https://docs.zyte.com/zyte-api/usage/browser.html#zyte-api-set-browser-headers
    
    # Retrieve HTML content from a given URL.

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,en;q=0.9",
        "Referer": "https://www.bing.com/"
        # Add more headers if needed
    }

    with open(api_keys_path, "r", encoding="utf-8") as f:
        api_keys = yaml.safe_load(f)
    zyte_api_key = api_keys["zyte_api_key"]

    proxies = {
        "http": f"http://{zyte_api_key}:@api.zyte.com:8011/",
        "https": f"http://{zyte_api_key}:@api.zyte.com:8011/",
    }
    try:
        response = requests.get(
            url,
            headers=headers,
            proxies=proxies,
            verify=ca_cert_path,
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    

def save_html_content(html_content, output_folder, page_number):
    file_name = f"page_{str(page_number).zfill(2)}.html"
    file_path = Path(output_folder) / file_name

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML content saved to {file_path}")


if __name__ == "__main__":
    cars = url_table_to_car_class(URL_LIST_PATH)

    for car in cars:
        if car.flag_load == "yes":
            scrape_data(
                base_url=car.first_url,
                max_pages=car.pages,
                output_folder=DATA_RAW_DIR / car.destination_folder,
            )
            print(car.destination_folder)


# =============================================================================
# # %%
# if __name__ == "__main__":
#     
#     base_url = "https://zikzero.com"
#     max_pages = 10
#     
#     scrape_data(base_url=base_url, 
#                 max_pages=max_pages ,
#                 output_folder= (r"data\raw\test2")  )
# =============================================================================
    