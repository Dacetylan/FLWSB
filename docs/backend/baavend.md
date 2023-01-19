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

![BaaVend Blokdiagram](./assets/baavend-diagram.jpg)

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
        container_name: baavend-red #you can give another name here
        networks:
            - net
        ports:
            - 1880:1880
        links:
           - "influxdb:db"  # the container influxdb is reachable as the hostnames "influxdb" and "db" through this container.
        environment:
            - TZ=Europe/Brussels
        volumes:
            - ./baavend-red:/data
            - ./nodered-flows.json:/data/flows.json:rw
            - ./nodered-flows_cred.json:/data/flows_cred.json:rw
            - ./nodered-settings.js:/data/settings.js:ro
        restart: on-failure:10

    influxdb:
        image: influxdb:latest
        container_name: baavend-db
        networks:
            - net
        ports:
            - 8086:8086   # https://localhost:8086
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
