# Security

 In dit onderdeel worden de beveiligingsmaatregelen op een rijtje gezet en beschreven van alle onderdelen waaruit de backend is opgebouwd.

 -> overal ander wachtwoord gebruiken!

 -> [SSL](https://www.digitalocean.com/community/tutorials/how-to-use-certbot-standalone-mode-to-retrieve-let-s-encrypt-ssl-certificates-on-ubuntu-1804)

## Docker

Docker is opgebouwd om veilig te zijn. Meer info hieroer kan teruggevonden worden in [de officële Docker documentatie](https://docs.docker.com/engine/security/).

## Docker-Compose en GitHub

Om ervoor te zorgen dat wachtworden en andere gevoelige data niet op GitHub terecht komt worden volgende voorzorgen getroffen:

- Geen gevoelige gegevens in de docker-compose.yml file.
- Wachtwoorden worden gehashed waar mogelijk.
- Container initialisatie aan de hand van environment variables worden in een aparte .env file bijgehouden die geëxclude worden.
- .gintignore voor bestanden die wachtwoorden bevatten, de .env bestanden en de self-signed test certificaten.


Voorbeeld .env file in docker-compose.yaml:
```yaml
# Gebruik .env file
  env_file:
    - grafana.env

# In plaats van
  environment:
    - GF_SECURITY_ADMIN_USER=<username>
    - GF_PATHS_PROVISIONING=/var/grafana-docker/provisioning
    - GRAFANA_INFLUX_DB=<db-name>
    - GRAFANA_INFLUX_USER=<username>
    - GRAFANA_INFLUX_PASSWORD=<password>
```


Voorbeeld .gintignore:
```
# Docker security
*.env
mosquitto-password.txt
mosquitto-tls/
influxdb-ssl/
nodered-settings.js
```


## Node-RED

user authentication met gehashed wachtwoord
ingesteld in nodered-settings.js

TLS certificaten voor HTTPS

https://nodered.org/docs/user-guide/runtime/securing-node-red

## TTN

user authentication met geheim wachtwoord
handmatig aanmaken op website TTN

TLS certificaten voor HTTPS
https://www.thethingsindustries.com/docs/integrations/node-red/receive/#configure-mqtt-in-node
https://www.thethingsindustries.com/docs/getting-started/ttn/addresses/#console

## InfluxDb

user authentication met wachtwoord
nitiële admin gebruiker adhv env_file

Token of API key voor toegang naar andere conatiners.

TLS certificaten voor HTTPS

## Mosquitto

user authentication met gehashed wachtwoord

TLS certificaten voor HTTPS

## Grafana

user authentication met wachtwoord
nitiële admin gebruiker adhv env_file

Eerste maal inloggen met default admin user, wachtwoord: admin
Vervolgens nieuw wachtwoord opgeven en username admin aanpassen in instellingen.
