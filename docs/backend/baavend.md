# Backend

## Introductie BaaVend

De BaaVend is de naam voor de backend van dit project.
Het bestaat uit services, voor zowel backend als frontend, in Docker containers opgezet met Docker-Compose in een Linux Virtual Machine omgeving.
Voor LoRaWAN connectiviteit wordt gebruik gemaakt van The Things Network (TTN).

In dit hoofdstuk wordt de backend acrhitectuur beschreven, de algemende werking, hoe deze is opgezet, en hoe de connectiviteit naar buiten de Docker omgeving toe werkt.

Vervolgens wordt er ingezoomed op de verschillende backend specifieke onderdelen, zijnde de [Linux VM](./backend/linux-vm.md), [Node-RED](./backend/nodered.md), [InfluxDb](./backend/influxdb.md), [Mosquitto](./backend/mosquitto.md).

In het onderdeel [Security](./backend/security.md) worden de aanwezige beveiligingsmaatregelen beschreven.

Er is ook samengewerkt met de AI studenten om testdata te voorzien, voor het AI project waar zij momenteel mee bezig zijn, en deze beschikbaar te stelen in de InfluxDb database. Dit is beschreven in het onderdeel [Testdata](./backend/testdata.md).

De frontend bestaat uit [Node-RED Dashboard](./frontend/dashboard.md) en [Grafana](./frontend/grafana.md). De werking hiervan wordt in het [Frontend](./frontend/dashboard.md) hoofdstuk beschreven.

Een voorbeeld van de volledige weg die data aflegd in deze backend kan gevonden worden in het onderdeel [Real Data](data-formatting/real-data.md).

1. Architectuur
2. Connectiviteit

---

## Architectuur

In dit onderdeel wordt de architectuur van de backend beschreven.
Als referentie is er onderstaand een blokdiagram met een algemeen overzicht van de structuur.

### Blokdiagram

![BaaVend Blokdiagram](./assets/baavend-diagram.jpg 'Figuur 1: BaaVend Blokdiagram')

### Services

- The Things Stack FLWSB applicatie (extern op TTN) voor LoRaWAN ontvangst.
- baavend-red: [Node-RED](https://flows.nodered.org/) container voor dataverwerking en alles te verbinden.
- baavend-db: [InlfuxDb v2.5](https://www.influxdata.com/blog/running-influxdb-2-0-and-telegraf-using-docker/) container als database voor de meetresultaten.
- baavend-mqtt: [Mosquitto](https://github.com/vvatelot/mosquitto-docker-compose) container als MQTT broker voor het weerstation.
- baavend-vis: [Grafana](https://grafana.com/oss/grafana/) container met frontend web applicatie voor data visualisatie.

#### Docker-Compose file

```yaml
version: "3"
services:
    nodered:
        depends_on:
            - influxdb
            - mosquitto
        build:
          context: .
          dockerfile: Dockerfile-nodered
        container_name: baavend-red  # Another name can be given here
        networks:
            - net
        ports:
            - 1880:1880
        links:
           - "influxdb:db"  # the container influxdb is reachable as the hostnames "influxdb" and "db" through this container, eg. http://influxdb:8086 or http://db:8086
        environment:
            - TZ=Europe/Brussels
        volumes:
            - ./baavend-red:/data
            # Comment out the following volumes after the first deployment, otherwise this will override the current files and produce errors on deploy of edited flows and revert changes in settings.
            - ./nodered-flows.json:/data/flows.json:rw  # Comment out after first deployment
            - ./nodered-flows_cred.json:/data/flows_cred.json:rw  # Comment out after first deployment
            - ./nodered-settings.js:/data/settings.js:ro  # Comment out after first deployment
        restart: on-failure:10

    influxdb:
        image: influxdb:latest
        container_name: baavend-db
        networks:
            - net
        ports:
            - 8086:8086   # http://localhost:8086 or http://influxdb:8086
        volumes:
            - ./baavend-db/data:/var/lib/influxdb2:rw
            - ./baavend-db/config:/etc/influxdb2:rw
            # - ./entrypoint.sh:/docker-entrypoint-initdb.d/entrypoint.sh
            # - ./influxdb-ssl/influxdb-selfsigned.crt:/etc/ssl/influxdb-selfsigned.crt:rw
            # - ./influxdb-ssl/influxdb-selfsigned.key:/etc/ssl/influxdb-selfsigned.key:rw
        env_file:
            - influxdb.env
        restart: on-failure:10

    mosquitto:
        image: eclipse-mosquitto:latest
        container_name: baavend-mqtt
        networks:
            - net
        ports:
            - 1883:1883
            - 9001:9001
        volumes:
            - ./baavend-mqtt/config/:/mosquitto/config/:rw
            - ./mosquitto.conf:/mosquitto/config/mosquitto.conf:rw
            - ./mosquitto-password.txt:/mosquitto/config/password.txt:rw
            - ./baavend-mqtt/log/:/mosquitto/log/
            - ./baavend-mqtt/data:/mosquitto/data/
        restart: on-failure:10

    grafana:
        depends_on:
          - nodered
          - influxdb
        image: grafana/grafana:latest
        container_name: baavend-vis
        networks:
            - net
        ports:
          - 3000:3000
        links:
            - "nodered:api"  # http://api:1880/flwsb-api/v1/
            - "influxdb"     # http://influxdb:8086
        env_file:
            - grafana.env
        volumes:
          - ./baavend-vis/provisioning/datasources:/etc/grafana/provisioning/datasources
          - ./baavend-vis:/var/lib/grafana
        restart: on-failure:10

networks:
   net:
      # Dit creërd een default netwerk met met filenaam_net = baavend_net
```

__*Merk op dat de Node-RED configuratie volumes uitgecomment moeten worden na de eerste deplyment. Anders gaat docker-compose de huidige versies van deze bestanden overschrijven bij opstarten met `docker-compose up -d`. Dit lijdt tot errors bij nieuwe deploys van gewijzigde flows, als ook het terugdraaien van eventuele wijzigingen in de instellingen.*__

#### Docker en docker-compose commando's

*In windows zijn de commanod's van docker-compose zonder het `-`, dus bijvoorbeeld `docker compose up -d` in plaats van `docker-compose op -d` in Ubuntu (Linux).

- `docker-compose build`: download en/of bouwt alle images al zonder deze op te starten.
- `docker-compose up -d`: download en/of bouwt de images indien nog niet gebeurt, en start alle services. `-d` staat voor *detached* wat betekend dat er niet in de terminals van de containers wordt gegaan.
- `docker-compose up -d --build` zelfde als voorgaande, maar herbouwt alle images.
- `docker-compose down`: stopt alle services. Combinatie van `docker stop` en `docker rm` voor alle services gedefiniëerd in het docker-compose bestand.
- `docker-compose exec -it <container-name> <bash-or-sh>`: Attach aan container terminal in Windows. Meeste werken met bash, maar sommige werken enkel met sh.
- `docker attach <container-id>`: Attach aan container terminal in Ubuntu (Linux).
- `docker ps`: geeft overzicht van conatiners, hun ID en status.

---

## Connectiviteit

Als connectiviteit wordt er gebruik gemaakt van __MQTT__ om data van The Things Network binnen te halen zowel als van het weerstation.

#### MQTT

MQTT wordt gebruikt om de data van de metingen te verkrijgen.
Dit gebeurd door op een endpoint te subscriben met een MQTT node in Node-RED.

Uit The Things Stack FLWSB applicatie kan dit als volgt:
```javascript
// Structure
v3/applicatie-naam@ttn/devices/board-name/up

// Example
v3/flwsb@ttn/devices/device-test/up
```

Voor het weerstation wordt een eigen MQTT broker opgezet met Mosquitto.
Dit wordt uitgelicht in het [Mosquitto](./backend/mosquitto.md) onderdeel.

---
