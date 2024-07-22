"""
Author: Pratima Sakpal
Date: 21 July 2024
Description: Crawling script for a link
https://doctors.adena.org/search?categories=clinical_keywords%2Cspecialties%2Cprovider_name%2Clocation_name%2\
Cprimary_care&sort=networks%2Crelevance%2Cavailability_density_best&search_alerts=false&shuffle_seed=\
73bed092-8cf2-4b3d-8636-fa28c40bb966&provider_fields=-clinical_keywords
"""
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

def get_html(link):
    """
    Description: Fetch data from link
    Input: link (string)
    Output: html (string)
    """
    html = requests.get(link, verify=False, proxies=None)
    time.sleep(1)
    if html.status_code == 200:
        return html.text
    return None

def get_soup(html):
    """
    Description: Generate soup of HTML
    Input: html (string)
    Output: Soup (BeautifulSoup Object)
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_details(soup):
    """
    Description: Extract details from HTML page
    Input: soup (BeautifulSoup Object)
    Output: all_data (List of dict)
    """
    all_data = []
    dr_cards = soup.find_all("div", {"class": "css-1k7k16a-ProviderContainer e16v8r6n0"})
    if not dr_cards:
        return None
    for dr_card in dr_cards:
        name = dr_card.find("h2").text
        if ',' in name:
            dr_name = name.split(', ')[0]
            qualification = name.split(', ')[1]
        else:
            dr_name = name.split(', ')
        specialities = dr_card.find('li', {"class": "css-p6aqbe-SummaryColumnItem eeq4ow44"})
        if specialities:
            specialities = specialities.text
        addresses = dr_card.find_all('td', {'class': 'css-9msay7'})
        phone_nums = dr_card.find_all('td', {'class': 'css-anxvi'})
        for index, add in enumerate(addresses):
            details = {}
            details['Dr Name'] = dr_name
            details['Qualification'] = qualification
            details['Specialities'] = specialities
            address = add.text
            details['Practice Locations'] = address
            phone_num = phone_nums[index].text
            details['Phone'] = phone_num
            all_data.append(details)
    return all_data

def write_into_csv(all_data):
    """
    Description: Funtion to write into a csv.
    Input: all_data List of dict
    Output: None
    """
    df = pd.DataFrame(all_data)
    df.to_csv("Doctors_informations.csv", index=False)

def main():
    """
    Description: Main calls
    Input: None
    Output: None
    """
    all_data = []
    page = 1
    while True:
        print(page)
        link = "https://doctors.adena.org/search?categories=clinical_keywords%2Cspecialties%2Cprovider_name%2Clocation_name%2Cprimary_care&sort=networks%2Crelevance%2Cavailability_density_best&search_alerts=false&shuffle_seed=73bed092-8cf2-4b3d-8636-fa28c40bb966&provider_fields=-clinical_keywords&page=" + str(page)
        html = get_html(link)
        print(html)
        if not html:
            break
        soup = get_soup(html)
        results = get_details(soup)
        if not results:
            break
        all_data.extend(results)
        write_into_csv(all_data)
        page += 1

if __name__ == "__main__":
    main()
