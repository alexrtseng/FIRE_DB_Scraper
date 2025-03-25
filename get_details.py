from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import json
import os


def get_detail_url(id):
    return f"https://www.thefire.org/research-learn/campus-deplatforming-database#campus-deplatforming/campus-deplatforming-details/{id}/"


def get_detail_page(id):
    try:
        driver.get(get_detail_url(id))
    except Exception as e:
        print(f"failed to get detail page for {id}")
        return ""
    time.sleep(4)
    html = driver.page_source
    driver.delete_all_cookies()
    return html


FIELDS = { # TODO: Luke can finish this
    "Year": "field_94",
    "School": "field_95",
    "School Type": "field_96",
    "Controversy": "field_103"
}

# function that gets the field value from the html
def get_field_value(html, field_num):
    pattern = rf'<td class="{field_num}.*?>.*?>(.*?)<'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# decode the html of a detail page into a json object
def decode_detail_html(html):
    dict = {}

    for field, field_num in FIELDS.items():
        value = get_field_value(html, field_num)
        if value:
            dict[field] = value
    return dict



if __name__ == "__main__":
    ids = []
    # load in the ids
    with open("ids.json", "r") as f:
        ids = json.load(f)

    # set up the driver
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    print(f"Fetching details for {len(ids)} ids")

    # get the details for each id
    detail_dicts = []

    # do this for all ids (can change num of ids)
    for id in ids:
        page_html = get_detail_page(id)
        detail_dicts.append(decode_detail_html(page_html))

    
