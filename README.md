# Tyggis E-handelsapplikasjon for tyggis

Denne Readme-en er laget med hjelp av ai
En Flask-basert e-handelsapplikasjon for å selge ulike tyggegumssmak.

## Funksjonalitet

- **Brukerautentisering**: Registrering og innlogging
- **Produktkatalog**: 9 ulike tyggegumssmak
- **Handlekurv**: Legg produkter til og fjern fra kurv
- **Bestillinger**: Lag og se handlekurv

## Teknologi

- **Backend**: Flask, Python
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Jinja2 templates
- **Sikkerhet**: Passordkryptering (SHA256), sesjonshåndtering

## Prosjektstruktur

```
├── app.py                 # Hovedapplikasjon med ruter
├── db.py                  # Databasefunksjoner
├── templates/             # HTML-maler
│   ├── base.html         # Basemål
│   ├── index.html        # Hjem
│   ├── product.html      # Produktdetaljer
│   ├── handlekurv.html   # Handlekurv
│   ├── bestillinger.html # Ordrer
│   ├── kontakt.html      # Kontakt
│   └── ...
├── static/               # Statiske filer
│   ├── css/              # Stilark
│   └── img/              # Produktbilder
└── env/                  # Virtuelt Python-miljø
```

## Installasjon og kjøring

### Systemkrav
- Python 3.7+
- pip
- flask

### Oppsett
1. Klon eller last ned prosjektet
2. Opprett virtuelt miljø: `python3 -m venv env`
3. Aktivér miljø: `source env/bin/activate`
4. Installer avhengigheter: `pip install -r requirements.txt`
5. Initialisér database: `python3 -c "from app import init_db; init_db()"`
6. Kjør applikasjonen: `python3 app.py`
7. Åpne nettleser på `http://localhost:5000`

## Databasestruktur

### users
- id (PRIMARY KEY)
- username
- email (UNIQUE)
- password_hash
- created_at

### cart
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- product_id
- quantity

### orders
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- total_price
- created_at

### order_items
- id (PRIMARY KEY)
- order_id (FOREIGN KEY)
- product_id
- quantity
- price

## Produkter

Applikasjonen tilbyr 9 smaksvarianter av tyggegummi, alle til kr 29:
1. Mint Gum
2. Strawberry Gum
3. Blueberry Gum
4. Watermelon Gum
5. Cinnamon Gum
6. Mango Gum
7. Cola Gum
8. Bubblegum Gum
9. Lakris Gum

## Lisens

Privat prosjekt - Periode 1 oppgave

## Kompetanse Mål

# Drift

utforske og beskrive komponenter i en driftsarkitektur
planlegge, implementere og drifte fysiske og virtuelle løsninger med segmenterte nettverk
utforske og beskrive relevante nettverksprotokoller, nettverkstjenester og serverroller
planlegge og dokumentere arbeidsprosesser og IT‑løsninger
gjennomføre risikoanalyse av nettverk og tjenester i en virksomhets systemer og foreslå tiltak for å redusere risikoen
planlegge, drifte og implementere IT‑løsninger som ivaretar informasjonssikkerhet og gjeldende regelverk for personvern
utforske trusler mot datasikkerhet og gjøre rede for dagens trusselbilde
feilsøke og rette feil ved hjelp av feilsøkingsstrategier og relevante rammeverk
beskrive og bruke rammeverk for kvalitetssikring av IT‑drift
bruke og administrere samhandlingsverktøy som effektiviserer samarbeid og deling av informasjon

# Utvikling

vurdere fordeler og ulemper ved ulike programmeringsspråk og velge og anvende relevante programmeringsspråk og algoritmer i eget arbeid
lage og begrunne funksjonelle krav til en IT‑løsning basert på behovskartlegging
vurdere brukergrensesnitt til IT‑tjenester og designe tjenester som er tilpasset brukernes behov
gjøre rede for hensikten med teknisk dokumentasjon og utarbeide teknisk dokumentasjon for IT‑løsninger
beskrive og anvende relevante versjonskontrollsystemer i utviklingsprosjekter
designe og implementere IT‑tjenester med innebygget personvern
analysere digitale trusler, verdier og sårbarheter og utvikle applikasjoner med innebygget sikkerhet
anvende relevant testmiljø og utføre testing tilpasset IT‑løsningen som utvikles
modellere og opprette databaser for informasjonsflyt i systemer
beskrive ulike datalagringsmodeller og metoder for å hente ut og sette inn bestemte data fra databaser som brukes av andre systemer
forenkle og automatisere arbeidsprosesser i utvikling av IT‑løsninger

# Brukerstøtte

utøve brukerstøtte og veilede i relevant programvare
kartlegge behovet for og utvikle veiledninger for brukere og kunder
utvikle kursmateriell og gjennomføre kurs i relevante IT‑systemer tilpasset en målgruppe
bruke og tilpasse kommunikasjonsform og fagterminologi i møte med brukere, kunder og fagmiljø
beskrive og anvende ulike metoder for å håndtere krevende situasjoner i kontakt med brukere og kunder
drøfte hvilke krav og forventninger som stilles til et likeverdig og inkluderende yrkesfellesskap

