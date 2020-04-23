# Toorny - työkalu turnausten järjestämiseen

## Kuvaus

Tarkoituksena on luoda työkalu, jolla käyttäjät voivat luoda turnauksia, sekä osallistua niihin. Lähtökohtaisesti tarkoitus on luoda tennisturnauksiin sopiva järjestelmä, mutta miksei myös muihin käyttötarkoituksiin.

Turnauksia voi luoda usean tyyppisiä (Single-elimination, Round-robin, ~~Double-elimination~~, ~~Swiss-system~~), jonka jälkeen palvelu luo niistä kaaviot sekä mahdollistaa niiden ylläpidon. Turnauksen ylläpitäjä voi kutsua turnaukseen käyttäjiä tai lisätä ne käsin. Turnauksen ylläpitäjä voi merkitä kaikkien pelien tulokset, jonka lisäksi palveluun rekisteröityneet käyttäjät voivat merkitä tulokset omiin peleihinsä. Palvelu pitää myös tilastotietoa tuloksista.

## Heroku

[Sovellus herokussa](https://tsoha-toorny.herokuapp.com)

Tunnukset:  
testi - testaaja

## Tunnetut ongelmat

- Tietoturva puuttuu
- Turnaustyypin valinta ei toimi
- Turnauksiin voi osallistua monta kertaa samalla tunnuksella
- Active users kysely footerissa ei toimi kaikilla sivuilla
- Toimintoja puuttuu
- Tyyli ei vastaa lopullista

## Toimintoja

- Kirjautuminen
- Turnauksen luominen
- Turnaukseen ilmoittautuminen
- Turnauksen hallinta
- Tuloksien syöttö
- Tulosten ja tilastojen tarkastelu

## Dokumentaatio

[Tietokantakaavio](https://github.com/msha/toorny/blob/master/documentation/tietokanta.jpg)

[Käyttötapaukset](https://github.com/msha/toorny/blob/master/documentation/usecases.md)

[Asennusohje](https://github.com/msha/toorny/blob/master/documentation/install.md)

[Käyttöohjeet](https://github.com/msha/toorny/blob/master/documentation/manual.md)
