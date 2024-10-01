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

# 1. Funkce pro ověření platnosti URL
def is_valid_url(url):
    return url.startswith('https://www.volby.cz')

# 2. Funkce pro stažení HTML obsahu ze zdrojového kódu
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Chyba při přístupu k URL {url}: {e}")
        return None

# 3. Funkce pro parsování HTML a extrakci měst
def extract_city_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = find_divs_with_class(soup, 't3')
    city_data = [extract_city_info_from_table(div.find('table', class_='table')) for div in divs]
    return [city for sublist in city_data for city in sublist] 

# 4. Funkce pro nalezení <div> s třídou pro pozdější extrakci jmen jednotlivých měst
def find_divs_with_class(soup, class_name):
    return soup.find_all('div', class_=class_name)

# 5. Funkce pro extrakci detailů jednotlivých měst z tabulky
def extract_city_info_from_table(table):
    if not table:
        return []
    city_data = []
    for row in table.find_all('tr'):
        city_info = extract_city_info_from_row(row)
        if city_info:
            city_data.append(city_info)
    return city_data

# 6. Funkce pro extrakci kódu města, názvu a detailního odkazu z <tr>
def extract_city_info_from_row(row):
    code_td = row.find('td', class_='cislo')
    name_td = row.find('td', class_='overflow_name')
    detail_td = row.find('td', class_='center')

    if code_td and name_td and detail_td:
        city_code = code_td.get_text(strip=True)
        city_name = name_td.get_text(strip=True)
        detail_link = extract_detail_link(detail_td)
        return {'CityCode': city_code, 'CityName': city_name, 'DetailLink': detail_link}
    return None

# 7. Funkce pro extrakci detailního odkazu
def extract_detail_link(td):
    a_tag = td.find('a', href=True)
    if a_tag:
        return f"https://volby.cz/pls/ps2017nss/{a_tag['href']}"
    return None

# 8. Funkce pro získání detailních výsledků z odkazu pro jednotlivé obce
def extract_city_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    publication_div = soup.find('div', id='publikace')
    
    detail_data = {}
    if publication_div:
        table = publication_div.find('table')
        if table:
            detail_data.update(extract_voting_stats(table))
    
    parties_table = soup.find('div', class_='t2_470')
    if parties_table:
        detail_data.update(extract_party_votes(parties_table))

    return detail_data

# 9. Funkce pro extrakci základních statistik (voličů, obálek, platných hlasů)
def extract_voting_stats(table):
    stats = {}
    stats['Voters'] = extract_stat_value(table, 'sa2')
    stats['Envelopes'] = extract_stat_value(table, 'sa3')
    stats['ValidVotes'] = extract_stat_value(table, 'sa6')
    return stats

# 10. Funkce pro získání hodnoty statistiky z tabulky podle headers
def extract_stat_value(table, header_value):
    stat_td = table.find('td', class_='cislo', headers=header_value)
    return stat_td.get_text(strip=True) if stat_td else None

# 11. Funkce pro extrakci hlasů jednotlivých stran
def extract_party_votes(parties_table):
    party_votes = {}
    for row in parties_table.find_all('tr'):
        party_name, party_votes_count = extract_party_info(row)
        if party_name and party_votes_count:
            party_votes[party_name] = party_votes_count
    return party_votes

# 12. Funkce pro extrakci názvu a hlasů strany
def extract_party_info(row):
    party_name_td = row.find('td', class_='overflow_name', headers='t1sa1 t1sb2')
    party_votes_td = row.find('td', class_='cislo', headers='t1sa2 t1sb3')
    party_name = party_name_td.get_text(strip=True) if party_name_td else None
    party_votes_count = party_votes_td.get_text(strip=True) if party_votes_td else None
    return party_name, party_votes_count

# Hlavní funkce, která koordinuje celý proces
def main():
    parser = argparse.ArgumentParser(description='Scraping volebních výsledků z webu.')
    parser.add_argument('url', type=str, help='URL územního celku')
    parser.add_argument('output_file', type=str, help='Jméno výstupního CSV souboru')

    args = parser.parse_args()
    
    if not is_valid_url(args.url):
        print("Chyba: Zadejte platný odkaz na web volby.cz.")
        sys.exit(1)

    html = fetch_html(args.url)
    if not html:
        print("Chyba při načítání stránky.")
        sys.exit(1)

    city_data = extract_city_data(html)
    if not city_data:
        print("Nebyla nalezena žádná data o městech.")
        sys.exit(1)

    print(f"Nalezeno {len(city_data)} měst. Začínám stahovat detailní výsledky...")

    all_results = []
    for city in city_data:
        city_html = fetch_html(city['DetailLink'])
        if city_html:
            details = extract_city_details(city_html)
            city.update(details)
            del city['DetailLink']
            all_results.append(city)

    df = pd.DataFrame(all_results)
    df.to_csv(args.output_file, index=False)
    print(f"Data byla úspěšně uložena do {args.output_file}")

if __name__ == "__main__":
    main()
