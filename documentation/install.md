# Asennusohje
### Esivaatimukset

Paikallisella koneella tulee olla asennettuna ainakin seuraavat ohjelmat:
* Python 3.x (+Flask)
* SQLite3
* Git

### Asentaminen paikallisesti ja sovelluksen käynnistäminen
1. Kloonaa projekti omalle koneellesi GitHubista komennolla
```
git clone git@github.com:msha/toorny.git
```
2. Käynnistä Pythonin virtuaaliympäristö 
```
python -m venv venv
source ./venv/bin/activate
```
3. Lataa projektin riippuvuudet
```
pip install -r requirements.txt
```
4. Käynnistä ohjelma (ohjelma käynnistyy oletuksena osoitteeseen http://localhost:5000)
```
python run.py
```

## Sovelluksen käyttö Herokussa

### Esivaatimukset
* Sovellus asennettuna paikallisella koneella
* Tunnukset Herokuun
* Heroku CLI asennettuna

0. Varmista että requirements.txt on ajantasalla, jos olet tehnyt sovellukseen muutoksia ja poista sieltä rivi "pkg-resources==0.0.0", jos se on olemassa

1. Alusta Heroku komennolla
```
heroku create <projektin nimi herokussa tähän>
```
Heroku ilmoittaa tässä kohtaa ohjelman url-osoitteen, sekä Herokun git-polun
2. Lisää git paikalliseen versionhallintaan
```
git remote add heroku <Herokun ilmoittama git-polku tähän>
```
3. Luo PostgreSQL-tietokanta Herokuun kommennolla 
```
heroku config:set HEROKU=1
heroku addons:add heroku-postgresql:hobby-dev
```
4. Puske projekti Herokuun
```
git push heroku master
```
Voit nyt tarkistaa ohjelman toimivuuden Herokussa, sekä asettaa automaattisen GitHub synkronoinnin projektille Herokun hallintapaneelista