### projekt_3
Třetí projekt pro Engeto Akademii (Python)

# Název projektu – Scraping volebních výsledků

Jedná se o třetí projekt v rámci kurzu datového analytika s Pythonem, který je zaměřen na aplikaci poznatků ohledně získávání dat z webových stránek pomocí scrapingu. Konkrétně tento projekt spočíval v získání volebních výsledků z roku 2017 (https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro jednotlivé obce z hlavního webu pomocí Pythonu. Skript, po uvedení zvolené URL adresy, stáhne data odpovídajících měst spolu s volebními výsledky a uloží je do vybraného CSV souboru. 

## Obsah projektu
Projekt obsahuje dohromady 4 soubory, kterými jsou:
- `projekt_3.py`: Hlavní skript pro scraping volebních výsledků.
- `requirements.txt`: Seznam knihoven potřebných k běhu skriptu.
- `README.md`: Dokumentace k projektu.
- `vysledky_beroun.csv`: CSV soubor s ukázkou výstupu po spuštění kódu a uvedení správných parametrů.

### Požadavky na správný průběh programu
1. Před spuštěním skriptu je potřeba nainstalovat potřebné knihovny. To lze provést pomocí souboru `requirements.txt`. Pro instalaci potřebných knihoven postupujte následovně:
   a. Ujistěte se, že máte nainstalován Python 3.2.
   b. Vytvořte virtuální prostředí (doporučeno, ale volitelné):
   
      i. Na Linuxu a macOS spusťte:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

      ii. Na Windows spusťte:

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

   c. Jakmile máte aktivované virtuální prostředí, spusťte instalaci knihoven:

   ```bash
   pip install -r requirements.txt

### Použití skriptu
1. Ujistěte se, že jste v adresáři obsahujícím `projekt_3.py`.
2. Spusťte skript s potřebnými argumenty:

   a. Skript očekává dva argumenty:
   
      i. URL územního celku (např. odkaz na stránku s volebními výsledky).
      
      ii. Název výstupního CSV souboru.

#### Příklad použití:
```bash
python projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps1111?xjazyk=CZ&xkraj=02&xnumnuts=2102&xobec=531061" vysledky_beroun.csv
```
Tento příkaz stáhne volební výsledky pro Beroun a uloží je do souboru vysledky_beroun.csv.
Doporučuji vkládat URL adresy uvnitř uvozovek, abyste se vyhnuli chybám při špatné interpretaci znaků Pythonem.
Pokud nezadáte oba argumenty (např. nesprávné pořadí nebo nesprávný odkaz), program vás na to upozorní a ukončí svoji činnost.

### Příklad výstupu pro Beroun
Pokud použijete příklad pro město Beroun, výsledný CSV soubor bude obsahovat následující sloupce:

- `CityCode`: Kód města.
- `CityName`: Název města.
- `Voters`: Počet voličů.
- `Envelopes`: Počet vydaných obálek.
- `ValidVotes`: Počet platných hlasů.
- Další sloupce budou obsahovat názvy jednotlivých politických stran a počet hlasů, které dané strany obdržely.
- Program vás po použití informuje o těchto skutečnostech:
```bash
Data o X městech byla nalezena. Začínám stahovat detailní výsledky...
Data byla úspěšně uložena do XYZ.csv
```

#### Ukázka části výstupního CSV souboru pro Beroun:
```bash
CityCode,CityName,Voters,Envelopes,ValidVotes...
534421,Bavoryně,239,151,150,18,0,0,6,0,8,7,5,2,4,0,0,16
531073,Běštín,262,158,157,27,2,0,21,0,2,11,3,3,3,1,0,12
531081,Broumy,743,491,489,62,1,0,35,2,20,54,6,5,8,0,0,76
531090,Březová,246,168,168,30,0,0,12,0,21,14,2,1,0,0,0,12
```
