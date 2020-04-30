# Toorny - työkalu turnausten järjestämiseen

## Kuvaus

Tarkoituksena on luoda työkalu, jolla käyttäjät voivat luoda turnauksia, sekä osallistua niihin. Lähtökohtaisesti tarkoitus on luoda tennisturnauksiin sopiva järjestelmä, mutta miksei myös muihin käyttötarkoituksiin.

Turnauksia voi luoda usean tyyppisiä (Single-elimination, ~~Round-robin~~, ~~Double-elimination~~, ~~Swiss-system~~), jonka jälkeen palvelu luo niistä kaaviot sekä mahdollistaa niiden ylläpidon. Turnauksen ylläpitäjä voi kutsua turnaukseen käyttäjiä tai lisätä ne käsin. Turnauksen ylläpitäjä voi merkitä kaikkien pelien tulokset, jonka lisäksi palveluun rekisteröityneet käyttäjät voivat merkitä tulokset omiin peleihinsä. Palvelu pitää myös tilastotietoa tuloksista.

## Heroku

[Sovellus herokussa](https://tsoha-toorny.herokuapp.com)

Tunnukset:  
testi - testaaja

## Toimintoja

- Kirjautuminen
- Turnauksen luominen
- Turnaukseen ilmoittautuminen
- Turnauksen hallinta
- Tuloksien syöttö
- Tulosten ja tilastojen tarkastelu

## Puutteita

#### UX
- Teema jäi MVP tasolle
- Ei varmistuskyselyitä turnauksen poistolle jne. käyttäjä voi väärillä klikeillä tuhota oman turnauksen helposti
- Käyttöliittymästä ei näe suoraan mihin otteluun pelaaja etenee
- Osassa toimintoja feedback käyttäjälle voisi olla selvempi

#### Toiminnallisuudet
- Turnaukselle ei voi syöttää päivämääriä,tarkempaa lajia/peliä
- Muut turnaustyypit kuin Single Elimination puuttuvat
- Turnauksiin ei voi lisätä(tai kutsua) kirjautumattomia käyttäjiä
- Käyttäjien sijoituksia ei voi käsin vaihtaa
- Käyttäjillä ei ole profiileja
- Salasanoja ei kryptata (ei kannata käyttää oikeaa salasanaa :D )

## Dokumentaatio

[Tietokantakaavio](https://github.com/msha/toorny/blob/master/documentation/tietokanta.jpg)

[Käyttötapaukset](https://github.com/msha/toorny/blob/master/documentation/usecases.md)

[Asennusohje](https://github.com/msha/toorny/blob/master/documentation/install.md)

[Käyttöohjeet](https://github.com/msha/toorny/blob/master/documentation/manual.md)
