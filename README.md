# Registar objekata sigurnosti plovidbe

Registar objekata sigurnosti plovidbe je API za pohranu i dohvaćanje podataka o objektima sigurnosti plovidbe. 

Podaci se pohranjuju u PostgreSQL bazi podataka (uz korištenje PostGIS ekstenzije za pohranu podataka o lokaciji), a prikazuju/isporučuju se u GeoJSON formatu:

```{
        "type": "Feature",
        "id": 1695,
        "properties": {
            "naziv_objekta": "Bravoalpha Test",
            "ps_br": "1234",
            "e_br": "56",
            "tip_objekta": 7,
            "lucka_kapetanija": "Disneyland",
            "fotografija": "/fotografije/nova-fotografija.jpg",
            "id_ais": "LD(D)-888",
            "simbol_oznaka": "/simboli/oznaka5.png",
            "pk": "1695"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                33.33,
                33.444
            ]
        }
    }
  ```

## Upotreba

### Dohvaćanje svih objekata

Endpoint: `/api/safety_objects/`   
Metoda: `GET`

### Dohvaćanje pojedinačnog objekta

Endpoint: `/api/safety_objects/<id_objekta>`   
Metoda: `GET`

### Kreiranje novog objekta
Endpoint: `/api/safety_objects/`   
Metoda: `POST`

Podaci za `POST` moraju biti u JSON formatu

```
{
    "naziv_objekta": "Bravoalpha Test",
    "ps_br": "1234",
    "e_br": "56",
    "tip_objekta": 7,
    "lucka_kapetanija": "Disneyland",
    "fotografija": "/fotografije/nova-fotografija.jpg",
    "id_ais": "LD(D)-888",
    "simbol_oznaka": "/simboli/oznaka5.png",
    "lokacija": "33.33, 33.444"
}
```

Obavezna polja:

`"naziv_objekta"` - format: string, maksimalne dužine 255 znakova   

`"lokacija"` - format: string, u obliku `"lat, long"` (obavezan zarez između vrijednosti) - npr. `"12.33, 45.44"`


Sva ostala polja su opcionalna.


### Ažuriranje postojećeg objekta
Endpoint: `/api/safety_objects/<id_objekta>`   
Metoda: `PATCH`

Podaci za `PATCH` moraju biti u JSON formatu

```
{
    "naziv_objekta": "Bravoalpha Test Updated",
    "lucka_kapetanija": "New Disneyland",
    "tip_objekta": 12,
}
```

Sva polja za `PATCH` su opcionalna (u bazi će se ažurirati samo ono što je poslano u `PATCH` zahtjevu), međutim, ako se ažuriraju `naziv_objekta` i/ili `lokacija`, njihove vrijednosti ne smiju biti prazne (`""` niti `null`) i moraju biti u ispravnom formatu:

`"naziv_objekta"` - format: string, maksimalne dužine 255 znakova   

`"lokacija"` - format: string, u obliku `"<lat>, <long>"` (obavezan zarez između vrijednosti) - npr. `"12.33, 45.44"`


### Brisanje postojećeg objekta
Endpoint: `/api/safety_objects/<id_objekta>`   
Metoda: `DELETE`


## Moguće greške

`404 - Object with id=<object_id> not found.`   
U bazi ne postoji objekt s traženim ID-om. (prilikom `GET` za pojedinačni objekt, `PATCH` ili `DELETE`)

`400 - Location data must not be empty.`   
1. Pokušana je kreacija novog objekta (`POST`) bez polja `lokacija` ili s praznom vrijednošću polja `lokacija.` 
2. Pokušano je ažuriranje objekta (`PATCH`) s praznom vrijednošću polja `lokacija.` 

`400 - Submitted location data is invalid.`  
Prilikom kreiranja novog objekta (`POST`) ili ažuriranja postojećeg (`PATCH`), vrijednost polja `lokacija` ne zadovoljava format `"<lat>, <long>"`.

`400 - <naziv polja>: [<greška>]`

Primjer:
```
"naziv_objekta": ["This field is required."]
```

1. Prilikom kreiranja novog objekta (`POST`) obavezno polje je prazno ili nije poslano, ili vrijednost polja ne udovoljava traženom formatu.
2. Prilikom ažuriranja postojećeg objekta (`PATCH`), obavezno polje je prazno ili vrijednost polja ne udovoljava traženom formatu.
