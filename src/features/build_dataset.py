from datetime import date
from pathlib import Path
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DEFAULT_OUTPUT_PATH = PROCESSED_DIR / "df_auto.pkl"
MASTER_PATH = BASE_DIR / "config" / "url_list.ods"

AUTO_PARAMETERS = [
    "title",
    "year",
    "km",
    "fuelTypeId",
    "fuelType",
    "isProfessional",
    "mainProvince",
    "hasWarranty",
    "warrantyMonths",
    "includesTaxes",
    "price",
]


def html_to_auto_string(html_path: Path) -> list:
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    script_tag = soup.find("script", string=re.compile("window.__INITIAL_PROPS__ = JSON.parse"))
    if not script_tag or not script_tag.string:
        return []

    html_match = re.search(r"JSON.parse\((.*)\)", script_tag.string)
    if not html_match:
        return []

    html_part = html_match.group(1)
    pattern = r'\\"offerType\\":{\\"id\\".*?\\"price\\":\d+,'
    matches = re.findall(pattern, html_part)
    return [match.replace("\\", "") for match in matches]


def extract_string(text: str, word: str):
    target = f'"{word}":'
    try:
        part = text.split(target, 1)[1]
        result = part.split(",", 1)[0]
        return result.strip("\"")
    except Exception:
        return float("nan")


def extract_auto_parameters(html_path: Path) -> pd.DataFrame:
    matches_clean = html_to_auto_string(html_path)
    df = pd.DataFrame(columns=AUTO_PARAMETERS)

    for matches_string in matches_clean:
        output_parameters = [extract_string(text=matches_string, word=param) for param in AUTO_PARAMETERS]
        temp_df = pd.DataFrame([output_parameters], columns=AUTO_PARAMETERS)
        df = pd.concat([df, temp_df], ignore_index=True)

    return df


def clean_df_auto(df_auto: pd.DataFrame) -> pd.DataFrame:
    df_auto = df_auto.copy()
    df_auto["year"] = df_auto["year"].astype(str).str.replace("}", "").str.replace("]", "")

    df_auto = df_auto.drop_duplicates(subset=["title", "year", "km"])
    df_auto = df_auto.dropna(subset=["title", "year", "km", "price"])

    fuel_map = {
        "1": "gasolina",
        "2": "diesel",
        "3": "electrico",
        "4": "hibrido",
        "5": "hibrido ench.",
        "6": "glp",
        "7": "cng",
    }
    df_auto["fuelType"] = df_auto["fuelTypeId"].map(fuel_map)

    df_auto["title"] = df_auto["title"].astype(str)
    df_auto["year"] = pd.to_numeric(df_auto["year"], errors="coerce")
    df_auto["km"] = pd.to_numeric(df_auto["km"], errors="coerce")
    df_auto["price"] = pd.to_numeric(df_auto["price"], errors="coerce")
    df_auto["cv"] = pd.to_numeric(df_auto.get("cv"), errors="coerce")
    df_auto["kw"] = pd.to_numeric(df_auto.get("kw"), errors="coerce")

    km_bins = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 1000000]
    km_labels = [
        "0-10",
        "10-20",
        "20-30",
        "30-40",
        "40-50",
        "50-60",
        "60-70",
        "70-80",
        "80-90",
        "90-10",
        ">100",
    ]
    df_auto["km_range"] = pd.cut(df_auto["km"], bins=km_bins, labels=km_labels, right=False)

    cv_bins = [0, 80, 100, 120, 150, 200, 1000]
    cv_labels = ["0-80", "80-100", "100-120", "120-150", "150-200", ">200"]
    df_auto["cv_range"] = pd.cut(df_auto["cv"], bins=cv_bins, labels=cv_labels, right=False)

    df_auto["age"] = date.today().year - df_auto["year"]
    df_auto["warrantyMonths"] = df_auto["warrantyMonths"].fillna(0)

    df_auto["price_calc"] = df_auto.apply(
        lambda row: row["price"] * 1.21 if row["includesTaxes"] is False and row["isProfessional"] is True else
        row["price"] * 1.05 if row["includesTaxes"] is False and row["isProfessional"] is False else
        row["price"],
        axis=1,
    )

    df_auto = df_auto.dropna(subset=["km"])
    df_auto = df_auto[~((df_auto["km"] < 1000) & (df_auto["age"] > 3))]
    df_auto = df_auto[df_auto["price"] > 2000]

    return df_auto


def remove_duplicated_autos(df_auto: pd.DataFrame) -> pd.DataFrame:
    return df_auto.drop_duplicates(subset=["title", "km"], keep="first")


def merge_data_auto_master(df_auto: pd.DataFrame, master_path=MASTER_PATH) -> pd.DataFrame:
    auto_master = pd.read_excel(master_path, engine="odf")
    return pd.merge(
        df_auto,
        auto_master[["destination_folder", "brand", "model", "segment", "body_type"]],
        left_on="brand_model",
        right_on="destination_folder",
    )


def kw_to_cv(kw):
    return str(int(kw) * 1.36)


def get_power_from_title(df_auto: pd.DataFrame) -> pd.DataFrame:
    df_auto = df_auto.copy()
    df_auto.loc[:, "kw"] = df_auto["title"].str.extract(r"(?i)(\d+)KW")
    df_auto.loc[:, "cv"] = df_auto["title"].str.extract(r"(?i)(\d+)CV")

    df_auto["kw"] = df_auto["kw"].replace(np.nan, 0)
    df_auto.loc[:, "cv"] = df_auto["cv"].fillna(df_auto["kw"].apply(kw_to_cv))

    df_auto["kw"] = df_auto["kw"].replace([0], np.nan)
    df_auto["cv"] = df_auto["cv"].replace([0], np.nan)

    return df_auto


def build_raw_dataframe(raw_dir=RAW_DATA_DIR) -> pd.DataFrame:
    df_auto = pd.DataFrame()
    raw_dir = Path(raw_dir)

    for folder in sorted(raw_dir.iterdir()):
        if not folder.is_dir():
            continue

        for file in sorted(folder.iterdir()):
            if file.suffix.lower() != ".html":
                continue

            temp = extract_auto_parameters(file)
            temp["brand_model"] = folder.name
            df_auto = pd.concat([df_auto, temp], ignore_index=True)

    return df_auto


def build_dataset(raw_dir=RAW_DATA_DIR, master_path=MASTER_PATH, output_path=DEFAULT_OUTPUT_PATH) -> pd.DataFrame:
    df_auto = build_raw_dataframe(raw_dir)
    df_auto = get_power_from_title(df_auto)
    df_auto = clean_df_auto(df_auto)
    df_auto = remove_duplicated_autos(df_auto)
    df_auto = merge_data_auto_master(df_auto, master_path=master_path)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_auto.to_pickle(output_path)

    return df_auto


if __name__ == "__main__":
    build_dataset()


