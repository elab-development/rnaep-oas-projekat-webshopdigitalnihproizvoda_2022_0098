# Platforma za prodaju digitalnih proizvoda

Mikroservisna aplikacija za kupovinu i prodaju digitalnih proizvoda (kursevi, e-knjige, grafički materijali) sa automatskom isporukom, konverzijom valuta i sistemom in-app notifikacija.

## Arhitektura sistema

| Servis | Opis | Baza | Port |
|---|---|---|---|
| User Service | Registracija, prijava, upravljanje korisnicima | PostgreSQL | 8001 |
| Product Service | Katalog proizvoda, kategorije | PostgreSQL | 8002 |
| Order Service | Narudžbine, plaćanje, preuzimanje | PostgreSQL | 8003 |
| Notification Service | In-app notifikacije | MongoDB | 8004 |
| API Gateway | Jedinstvena ulazna tačka, Circuit Breaker | - | 8000 |
| Frontend | React + Vite + TailwindCSS | - | 3000 |

## Preduslovi

- Docker i Docker Compose
- Git

## Pokretanje

**1. Kloniraj repozitorijum:**
```bash
git clone https://github.com/elab-development/rnaep-oas-projekat-webshopdigitalnihproizvoda_2022_0098.git
cd rnaep-oas-projekat-webshopdigitalnihproizvoda_2022_0098
```

**2. Kreiraj .env fajl u korenu projekta:**
```env
UNSPLASH_ACCESS_KEY=tvoj_unsplash_api_kljuc
PAYMENT_MODE=mock
```

**3. Pokreni sve servise:**
```bash
docker-compose up --build
```

**4. Otvori browser:**

| Servis | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API Gateway | http://localhost:8000 |
| Swagger dokumentacija | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 (admin/admin) |

**5. Kreiraj admin korisnika:**
```bash
curl -X POST "http://localhost:8000/api/users/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"Admin\", \"last_name\": \"Admin\", \"email\": \"admin@test.com\", \"password\": \"admin1234\", \"role\": \"admin\"}"
```

## Eksterni API-ji

- **Unsplash** — automatsko pribavljanje naslovne slike proizvoda pri kreiranju
- **Exchange Rates API** — konverzija cene proizvoda u EUR i USD

## Event-Driven Architecture (Kafka)

Komunikacija između mikroservisa transformisana je iz sinhrone (HTTP) u asinhronu korišćenjem Apache Kafka.

**Topics:**
- `product-created` — kreiran je novi digitalni proizvod
- `order-created` — inicirana je nova narudžbina
- `payment-confirmed` — plaćanje je uspešno potvrđeno
- `payment-failed` — plaćanje nije uspelo
- `download-unlocked` — preuzimanje je omogućeno kupcu

**Producer-i:** Product Service, Order Service

**Consumer-i:** Order Service, Notification Service

**Hibridni modul (Consumer + Producer):**

Order Service — konzumira `payment-confirmed`, ažurira status narudžbine i publikuje `download-unlocked`

## Bezbednost

| Napad | Zaštita |
|---|---|
| XSS | Pydantic validacija sa html.escape na svim ulaznim podacima |
| CORS | Konfigurisan na API Gateway-u, dozvoljen pristup samo sa http://localhost:3000 |
| IDOR | JWT middleware proverava vlasništvo nad resursom pre svake izmene |
| SQL Injection | SQLAlchemy ORM — parametrizovani upiti |
| CSRF | JWT autentifikacija u Authorization headeru umesto cookija |

## CI/CD

Proces razvoja je automatizovan korišćenjem GitHub Actions. Pipeline se okida na svaki push i pull request i sastoji se od dve faze:
- **test** — instalira zavisnosti i pokreće testove za svaki mikroservis
- **build** — builduje Docker image za svaki mikroservis ako testovi prođu
- **publish** — objavljuje Docker image-e na GitHub Container Registry (okida se samo na main grani)

## Monitoring

Prometheus i Grafana su podignuti kroz Docker Compose za prikupljanje i vizualizaciju metrika.

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

Svi mikroservisi izlažu `/metrics` endpoint sa podacima o broju HTTP zahteva, vremenu odgovora i health statusu servisa.

## Distribuirani paterni

**Circuit Breaker** je implementiran u API Gateway-u za sve mikroservise. Ako mikroservis ne odgovori nakon 3 uzastopna neuspela pokušaja, prekidač se otvara i odmah vraća fallback odgovor klijentu umesto da čeka na timeout, čime se sprečava kaskadno otkazivanje sistema. Nakon 30 sekundi, prekidač prelazi u half-open stanje i testira da li je servis oporavio.

Status svih Circuit Breaker-a dostupan je na: `GET /circuit-breakers/status`


## Testiranje Kafka toka

Nakon kupovine proizvoda, možeš pratiti tok događaja kroz logove:

```bash
docker logs order-service -f
docker logs notification-service -f
```

Očekivani tok:
1. `order-service` kreira narudžbinu i publikuje `order-created`
2. `order-service` procesira plaćanje i publikuje `payment-confirmed`
3. `order-service` konzumira `payment-confirmed`, generiše download token i publikuje `download-unlocked`
4. `notification-service` konzumira `payment-confirmed` i `download-unlocked` i kreira in-app notifikacije

## Primeri API poziva

**Registracija korisnika:**
```bash
curl -X POST "http://localhost:8000/api/users/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"Ana\", \"last_name\": \"Jovic\", \"email\": \"ana@test.com\", \"password\": \"test1234\", \"role\": \"buyer\"}"
```

**Prijava:**
```bash
curl -X POST "http://localhost:8000/api/users/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"ana@test.com\", \"password\": \"test1234\"}"
```

**Pregled proizvoda:**
```bash
curl -X GET "http://localhost:8000/api/products/"
```

**Status Circuit Breaker-a:**
```bash
curl -X GET "http://localhost:8000/circuit-breakers/status"
```

## Zaustavljanje sistema

```bash
# Zaustavljanje sistema
docker-compose down

# Zaustavljanje sa brisanjem podataka
docker-compose down -v
```