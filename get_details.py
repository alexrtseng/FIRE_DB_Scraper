from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

FIELDS = { 
    "Year": "field_94",
    "School": "field_95",
    "School Type": "field_96",
    "Speaker/Performer/Title": "field_97",
    "Type of Expression": "field_98",
    "Controversy Topic(s)": "field_102",
    "Source(s)": "field_99",
    "Political Motives of Source(s)": "field_100",
    "Petition For": "field_107",
    "Petition Against": "field_106",
    "Outcome": "field_101",
    "Reinvited/ Rescheduled/ Relocated?": "field_109",
    "Controversy Explanation": "field_103",
    "Public Response": "field_108",
    "Read More": "field_105"
}


def get_detail_url(id):
    return f"https://www.thefire.org/research-learn/campus-deplatforming-database#campus-deplatforming/campus-deplatforming-details/{id}/"


def get_detail_page(driver, id):
    url = get_detail_url(id)
    print(f"Getting detail page for {id} at {url}")
    driver.get(url)
    try:
        # Replace 'specific-element-class-or-id' with an actual class or ID of an element that appears after loading
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "field_94"))
        )
        print("Page loaded successfully.")
        html = driver.page_source
    except Exception as e:
        print("Error: Page did not load within the timeout period.", e)
        print(f"Succesfully got detail page for {id}")
        return ""
    html = driver.page_source
    return html


# function that gets the field value from the html
def get_field_value(html, field_num):
    if field_num == "field_105":
        pattern = r'<a class="in-cell-link" target="_blank" href="(https?://.*?)">'
        matches = re.findall(pattern, html, re.DOTALL)
        if matches:
            return [url.strip() for url in matches]
        else:
            print(f"Error: No URLs found for field number {field_num}")
            return []
        
    pattern = rf'<tr class="{field_num}".*?>.*?<td class="kn-value">.*?<span.*?>(.*?)<'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        print(f"Error: No match found for field number {field_num}")
        return None


# decode the html of a detail page into a json object
def decode_detail_html(html, id):
    # Create an empty DataFrame with columns labeled as the keys of FIELDS
    df = pd.DataFrame()
    for field, field_num in FIELDS.items():
        value = get_field_value(html, field_num)
        df[field] = [value]
        df["fire_id"] = [id]
    return df


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
    df = pd.DataFrame(columns=list(FIELDS.keys()) + ["fire_id"])

    for id in ids:
        page_html = get_detail_page(driver, id)
        detail_df = decode_detail_html(page_html, id)
        df = pd.concat([df, detail_df], ignore_index=True)

    output_file = f"big_details.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved details to {output_file}")

    driver.quit()