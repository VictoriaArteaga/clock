# Pais con metadatos suficientes para el panel "Relojes del Mundo":
# codigo (lo usa FlagRenderer), nombre, capital y zona horaria IANA.

from dataclasses import dataclass


@dataclass(frozen=True)
class Country:
    code: str
    name: str
    capital: str
    timezone: str


# Catalogo fijo de paises mostrados en la vista global.
COUNTRIES = [
    Country("UK", "Reino Unido",    "Londres",       "Europe/London"),
    Country("FR", "Francia",        "Paris",         "Europe/Paris"),
    Country("ES", "Espana",         "Madrid",        "Europe/Madrid"),
    Country("DE", "Alemania",       "Berlin",        "Europe/Berlin"),
    Country("IT", "Italia",         "Roma",          "Europe/Rome"),
    Country("RU", "Rusia",          "Moscu",         "Europe/Moscow"),
    Country("CZ", "Rep. Checa",     "Praga",         "Europe/Prague"),
    Country("US", "Estados Unidos", "Nueva York",    "America/New_York"),
    Country("MX", "Mexico",         "CDMX",          "America/Mexico_City"),
    Country("BR", "Brasil",         "Brasilia",      "America/Sao_Paulo"),
    Country("AR", "Argentina",      "Buenos Aires",  "America/Argentina/Buenos_Aires"),
    Country("JP", "Japon",          "Tokio",         "Asia/Tokyo"),
    Country("CN", "China",          "Pekin",         "Asia/Shanghai"),
    Country("IN", "India",          "Nueva Delhi",   "Asia/Kolkata"),
    Country("AU", "Australia",      "Sidney",        "Australia/Sydney"),
]
