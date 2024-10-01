"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michaela Terelya
email: michaela.terelya@gmail.com
discord: reikha.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import sys

# Funkce pro získání základních dat o obcích (kód a název) + odkaz na detaily z voleb (počet hlasů, názvy jednotlivých stran, počet obálek a validních hlasů)
def get_city_data_with_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba při přístupu k URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    city_data = []

    # Najdeme všechny <div> s třídou "t3"
    divs = soup.find_all('div', class_='t3')

    # Projdeme všechny <div> a hledáme v nich <table> s třídou "table"
    for div in divs:
        table = div.find('table', class_='table')
        if table:
            # Projdeme všechny <tr> v tabulce a získáme hodnoty z <td> s třídou "cislo" a "overflow_name"
            for row in table.find_all('tr'):
                code_td = row.find('td', class_='cislo')
                name_td = row.find('td', class_='overflow_name')
                detail_td = row.find('td', class_='center')

                if code_td and name_td and detail_td:
                    # Získáme text z obou <td> a odkaz na detaily, který uchováme pro další zpracování
                    city_code = code_td.get_text(strip=True)
                    city_name = name_td.get_text(strip=True)
                    detail_link_tag = detail_td.find('a', href=True)
                    if detail_link_tag:
                        detail_link = f"https://volby.cz/pls/ps2017nss/{detail_link_tag['href']}"
                        city_data.append({
                            'CityCode': city_code,
                            'CityName': city_name,
                            'DetailLink': detail_link
                        })

    return city_data

# Funkce pro získání detailních výsledků z odkazu pro jednotlivé obce
def get_city_details(detail_url):
    try:
        response = requests.get(detail_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba při přístupu k URL {detail_url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Najdeme div s id "publikace" a uvnitř tabulku
    detail_data = {}
    publication_div = soup.find('div', id='publikace')

    if publication_div:
        table = publication_div.find('table')
        if table:
            # Získání počtu voličů v seznamu
            voters_td = table.find('td', class_='cislo', headers='sa2')
            if voters_td:
                detail_data['Voters'] = voters_td.get_text(strip=True)

            # Získání počtu vydaných obálek
            envelopes_td = table.find('td', class_='cislo', headers='sa3')
            if envelopes_td:
                detail_data['Envelopes'] = envelopes_td.get_text(strip=True)

            # Získání počtu platných hlasů
            valid_votes_td = table.find('td', class_='cislo', headers='sa6')
            if valid_votes_td:
                detail_data['ValidVotes'] = valid_votes_td.get_text(strip=True)

        # Najdeme strany a jejich hlasy v tabulce pod div class="t2_470"
        parties_table = soup.find('div', class_='t2_470')
        if parties_table:
            for row in parties_table.find_all('tr'):
                # Názvy stran
                party_name_td = row.find('td', class_='overflow_name', headers='t1sa1 t1sb2')
                # Hlasy pro strany
                party_votes_td = row.find('td', class_='cislo', headers='t1sa2 t1sb3')

                if party_name_td and party_votes_td:
                    party_name = party_name_td.get_text(strip=True)
                    party_votes = party_votes_td.get_text(strip=True)

                    # Uložíme název strany a její počet hlasů do detail_data
                    detail_data[party_name] = party_votes

    return detail_data

def main():
    parser = argparse.ArgumentParser(description='Scraping volebních výsledků z webu.')
    parser.add_argument('url', type=str, help='URL územního celku')
    parser.add_argument('output_file', type=str, help='Jméno výstupního CSV souboru')

    args = parser.parse_args()
    
    # Zajištění správnosti URL
    if not args.url.startswith('https://volby.cz') or not args.output_file:
        print("Chyba: Zadejte platný odkaz a název výstupního souboru.")
        sys.exit(1)

    url = args.url
    output_file = args.output_file

    # Získání dat z měst (kód, název, odkaz na detailní výsledky)
    city_data = get_city_data_with_links(url)

    if not city_data:
        print("Nebyla nalezena žádná data o městech.")
        sys.exit(1)

    print(f"Data o {len(city_data)} městech byla nalezena. Začínám stahovat detailní výsledky...")

    all_results = []

    # Pro každé město získáme detailní výsledky z detailních odkazů
    for city in city_data:
        detail_results = get_city_details(city['DetailLink'])
        if detail_results:
            city.update(detail_results)  # Přidání detailních výsledků do dat města
            del city['DetailLink']  # Odstranění odkazu před uložením do CSV
            all_results.append(city)

    # Uložení dat do CSV
    df = pd.DataFrame(all_results)
    df.to_csv(output_file, index=False)

    print(f"Data byla úspěšně uložena do {output_file}")
    sys.exit(0)  

if __name__ == "__main__":
    main()
