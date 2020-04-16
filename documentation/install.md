# Asennusohje
### Esivaatimukset

Paikallisella koneella tulee olla asennettuna ainakin seuraavat ohjelmat:
* Python 3.x (+Flask)
* SQLite3
* Git

### Asentaminen ja sovelluksen käynnistäminen
1. Kloonaa projekti omalle koneellesi GitHubista komennolla
```
git clone git@github.com:msha/toorny.git
```
2. Käynnistä Pythonin virtuaaliympäristö 
```
python3 -m venv venv
source ./venv/bin/activate
```
3. Lataa projektin riippuvuudet
```
pip install -r requirements.txt
```
4. Käynnistä ohjelma (ohjelma käynnistyy oletuksena osoitteeseen http://localhost:5000)
```
python3 run.py
```