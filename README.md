# Diablo 4 Gear Affixes

Generate tables of Diablo 4 gear affixes. Data is based on: https://d4builds.gg/database/gear-affixes/

Final spreadsheet: https://docs.google.com/spreadsheets/d/1QWiOOcqh3jp8ynkRZaFq-EVTc3uPO8tdfGOcp9hrAoo/edit?usp=sharing

## Requirements

- Python
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Usage

```
$ curl https://d4builds.gg/database/gear-affixes/ -o gear_affixes.html
$ python src/extract_data.py gear_affixes.html data.json
$ python src/convert_data.py data.json affix_slots.csv slot_affixes.csv
```
