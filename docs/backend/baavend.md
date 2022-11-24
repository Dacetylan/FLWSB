# BaaVend Backend

## Introductie

De BaaVend is de naam voor de backend van dit project.
Het bestaat uit services, voor zowel backend als frontend, in Docker containers opgezet met Docker-Compose.
Voor LoRaWAN connectiviteit wordt gebruik gemaakt van The Things Network (TTN).
In dit hoofdstuk wordt de backend acrhitectuur beschreven, de algemende werking, hoe deze is opgezet, en hoe de connectiviteit naar buiten de Docker omgeving toe werkt.
Vervolgens wordt er ingezoomed op de verschillende backend specifieke onderdelen, zijnde Node-RED, InfluxDb en Mosquitto.
Als laatste worden de aanwezige beveiligingsmaatregelen beschreven.
De frontend bestaat uit Grafana en Node-Red Dashboard. De werking hiervan wordt in het Frontend hoofdstuk beschreven.

---

## Architectuur

In dit onderdeel wordt de architectuur van de backend beschreven.
Als referentie is er onderstaand een blokdiagram met een algemeen overzicht van de structuur.

### Blokdiagram

<iframe width="1920" height="1080" src="https://miro.com/app/live-embed/uXjVPAdIy0o=/?moveToViewport=-768,-413,1536,824&embedId=541050009056" frameborder="0" scrolling="no" allowfullscreen></iframe>

![BaaVend Blokdiagram](./assets/baavend-diagram.jpg)

*__Update: Angular wordt vevangen door Node-Red Dashboard, MongoDb wordt vervangen door InfluxDb en Mosquitto is toegevoegd als MQTT broker voor het weerstation.__

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
            - 8880:1880
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
            - influxdb2:/var/lib/influxdb2:rw
            - influxdb2:/etc/influxdb2:rw
            - ./baavend-db/data:/var/lib/influxdb2:rw
            - ./baavend-db/config:/etc/influxdb2:rw
            - ./influxdb-ssl/influxdb-selfsigned.crt:/etc/ssl/influxdb-selfsigned.crt:rw
            - ./influxdb-ssl/influxdb-selfsigned.key:/etc/ssl/influxdb-selfsigned.key:rw
        env_file:
            - influxdb.env
        restart: on-failure:1

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

volumes:
  influxdb2:

networks:
   net:

```

### Connectiviteit

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
Hiervoor is het endpoint bijvoorbeeld

```javascript
// Structure
sensors/rtl_433/Bresser-5in1/Alecto-id/measurement-quantity_unit

// Examples
sensors/rtl_433/Bresser-5in1/100/temperature_C
sensors/rtl_433/Bresser-5in1/100/humidity
```


---
