# Kirjakerho-sovellus

Sovelluksen avulla kirjakerhon jäsenet voivat kommentoida luettuja kirjoja ja ehdottaa uusia kirjoja kerhon luettavaksi.

Nykytilanteessa:
- Sovellukseen voi rekisteröityä. Ylläpitäjäksi rekisteröityminen tapahtuu antamalla salasanaksi "admin".
- Rekisteröitynyt käyttäjä voi kirjautua sovellukseen.
- Käyttäjä näkee sovelluksen etusivulla navigointipalkin, listan luetuista kirjoista (ja jokaisen kirjan kommenttimäärän sekä annettujen arvosanojen keskiarvon) sekä listan ehdotetuista kirjoista.
- Käyttäjä voi lisätä uuden kommentin luetulle kirjalle ja lukea muiden antamia kommentteja.
- Käyttäjä voi poistaa ja muokata omia kommenttejaan.
- Käyttäjä voi antaa kirjalle arvosanan.
- Käyttäjä voi ehdottaa uusia kirjoja luettavaksi.
- Ylläpitäjä voi lisätä ja arkistoida luettuja kirjoja.
- Ylläpitäjä voi katsella arkistoa ja palauttaa arkistoidut kirjat etusivulle.
- Ylläpitäjä voi poistaa kaikkien käyttäjien kommentteja.
- Ylläpitäjä voi poistaa ehdotettuja kirjoja tai hyväksyä niitä luettavaksi.

Sovellusta ei voi testata tuotannossa. Alla on ohje sovelluksen käyttämiseen paikallisesti:

## Käynnistysohje
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon `.env`-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

`DATABASE_URL=<tietokannan-paikallinen-osoite>`

`SECRET_KEY=<salainen-avain>`

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r ./requirements.txt`

Määritä vielä tietokannan skeema komennolla:

`psql < schema.sql`

Nyt voit käynnistää sovelluksen komennolla:

`flask run`



