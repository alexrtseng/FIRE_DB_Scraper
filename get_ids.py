import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os

# returns url of page i in the table
def get_page_url(i):
    return f"https://www.thefire.org/research-learn/campus-deplatforming-database#campus-deplatforming/?view_44_page={i}"


# regular expression to extract id from html for a page
def extract_ids(html):
    return re.findall(r'<tr id="(.*?)">', html)

# get the page table i and return the ids
def get_page_ids(i, driver):
    try:
        driver.get(get_page_url(i))
        time.sleep(6)
    except Exception as e:
        print(f"failed to get page {i}")
        return []
    html = driver.page_source
    return extract_ids(html)

if __name__ == "__main__":
    # set up the driver
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    ids = []

    for i in range(1, 69):
        new_ids = get_page_ids(i, driver)
        print(f"Page {i} ids: {new_ids}")
        ids += new_ids

    if not os.path.exists("FIRE_ids.json"):
        with open("FIRE_ids.json", "w") as f:
            json.dump(ids, f)

    driver.quit()
