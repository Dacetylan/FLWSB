# BaaVend Backend

## Introductie

De BaaVend is de naam voor de backend van dit project.
Het bestaat uit services, voor zowel backend als frontend, in Docker containers opgezet met Docker-Compose.
Voor LoRaWAN connectiviteit wordt gebruik gemaakt van The Things Network (TTN).
In dit hoofdstuk wordt de backend acrhitectuur beschreven, de algemende werking, hoe deze is opgezet, en hoe de connectiviteit naar buiten de Docker omgeving toe werkt.
Vervolgens wordt er ingezoomed op de verschillende backend specifieke onderdelen, zijnde Node-RED, MongoDb, InfluxDb en Mosquitto.
Als laatste worden de aanwezige beveiligingsmaatregelen beschreven.
De frontend als user interface en de werking hiervan volgt in het Frontend hoofdstuk.

---

## Architectuur

In dit onderdeel wordt de architectuur van de backend beschreven.
Als referentie is er onderstaand een blokdiagram met een algemeen overzicht van de structuur.

### Blokdiagram

![BaaVend Blokdiagram](./assets/baavend-diagram.png)

*__Updaten: Angular weg, en InfluxDb en Mosquitto toevoegen!__

### Services

- The Things Stack FLWSB applicatie (extern op TTN) voor LoRaWAN ontvangst.
- baavend-red: [Node-RED](https://flows.nodered.org/) container voor dataverwerking en alles te verbinden.
- baavend-sis-db: [MongoDb](https://www.mongodb.com/) container als database voor het SIS.
- baavend-time-db: [InlfuxDb v2.0](https://www.influxdata.com/blog/running-influxdb-2-0-and-telegraf-using-docker/) container als database voor de meetresultaten.
- baavend-mqtt: [Mosquitto](https://github.com/vvatelot/mosquitto-docker-compose) container als MQTT broker voor het weerstation.
- baavend-vis: [Grafana](https://grafana.com/oss/grafana/) container met frontend web applicatie voor data visualisatie.


### Connectiviteit

Als connectiviteit wordt er gebruik gemaakt van __MQTT__ en een [REST](https://www.redhat.com/en/topics/api/what-is-a-rest-api) __API__.

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
