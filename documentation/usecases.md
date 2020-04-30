# Käyttäjätarinat

## Käyttäjä voi rekisteröityä palveluun

Käyttäjä rekisteröityy palveluun lomakkeen kautta, jonka jälkeen hän voi käyttää turnauksen luontitoimintoa, sekä lisätä tuloksia

SQL-kysely:
```
INSERT INTO users (username, password, name, date_created, date_modified, user_group) 
VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)
```

## Rekisteröitynyt käyttäjä voi luoda turnauksia palvelussa

Käyttäjä luo turnauksen ja asettaa sille haluamansa formaatin, sekä muut tiedot(nimi, päivämäärä, kuvaus, twitch-stream osoite, jne.)

SQL-kysely:
```
INSERT INTO tournament (name, type, description, date_created, date_modified, start_date, end_date, status, owner) 
VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)
```
**HUOM**: _Päivämäärää ei nykyisessä versiossa kysytä tai näytetä sivuilla, joten kenttiin syötetään vain nykyinen aikaleima_

## Rekisteröitynyt käyttäjä hallita luomaansa turnausta

Käyttäjä voi lisätä turnaukseen osallistujia, merkata sen alkaneeksi, vaihtaa nimeä yms.

SQL-kysely muokkaukselle
```
UPDATE tournament SET name=?, description=?, date_modified=CURRENT_TIMESTAMP 
WHERE tournament.tournament_id = ?
```

SQL-Kysely turnauksen aloitukselle
```
UPDATE tournament SET date_modified=CURRENT_TIMESTAMP, status=? 
WHERE tournament.tournament_id = ?
```
jonka yhteydessä luodaan tarvittavat ottelut
```
INSERT INTO "match" (match_no, tournament_id, parent_id, round, husers_id, vusers_id, winner, date) 
VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
```
tai vastaavasti poistetaan turnauksen *kaikki* ottelut, jos turnaus keskeytetään
```
DELETE FROM "match" 
WHERE "match".tournament_id = ?
```

Turnauksen poisto
```
DELETE FROM tournament WHERE tournament.tournament_id = ?
```
jonka yhteydessä turnaukseen liittyneet käyttäjät poistetaan liitostaulusta
```
DELETE FROM users_to_tournaments 
WHERE users_to_tournaments.tournament_id = ?
```

## Rekisteröitynyt käyttäjä voi osallistua olemassa olevaan turnaukseen

Käyttäjä liittyä turnaukseen pelaajaksi

SQL-kysely
```
INSERT INTO users_to_tournaments (tournament_id, user_id, sort_order) 
VALUES (?, ?, ?)
```

## Rekisteröitynyt käyttäjä voi syöttää tuloksia pelaamiinsa otteluihin

Käyttäjä voi syöttää tuloksen otteluun, johon hän on osallistunut

SQL-kysely
```
INSERT INTO score (matches_id, husers_score, vusers_score) VALUES (?, 
?, ?)
```

## Käyttäjät voivat tarkastella olemassa olevia turnauksia

Käyttäjä voi tarkastella turnauksia ja katsoa niiden tietoja, sekä tuloksia

SQL-kyselyt:
Etusivulla kaikkien turnausten näyttö
```
SELECT * FROM tournament
```
**HUOM**: _Tällä hetkellä tulosten määrää ei suodateta, joten sovellus ei toimisi isommilla käyttäjämäärillä. Tulosten määrän rajoitus olisi kuitenkin suht. helppo lisätä_

```
SELECT users_to_tournaments.tournament_id AS users_to_tournaments_tournament_id, users_to_tournaments.user_id AS users_to_tournaments_user_id, users_to_tournaments.sort_order AS users_to_tournaments_sort_order, users.users_id AS users_users_id, users.username AS users_username, users.password AS users_password, users.name AS users_name, users.date_created AS users_date_created, users.date_modified AS users_date_modified, users.user_group AS users_user_group
FROM users_to_tournaments, users
WHERE users_to_tournaments.tournament_id = ? AND users.users_id = users_to_tournaments.user_id ORDER BY users_to_tournaments.sort_order, users.name
```

## Käyttäjät voivat tarkastella tilastotietoja turnauksista

Käyttäjät voivat katsoa tilastoja toisen käyttäjän pelaamista peleistä, voittoprosenteista jne.

SQL-kysely top 10 käyttäjät voittojen mukaan
```
select top 10 u.name, count(*) as wins, (select count(*) from match where husers_id = u.users_id or vusers_id = u.users_id) 
from users u 
join users_to_tournaments utt on u.users_id = utt.user_id  
join tournament t on utt.tournament_id = t.tournament_id  
join match m on m.tournament_id = t.tournament_id  
where (u.users_id = m.husers_id and m.winner = 1) or (u.users_id = m.vusers_id and m.winner = 2) 
group by u.users_id 
order by wins
limit 10
```
