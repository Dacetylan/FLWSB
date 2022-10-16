# BaaVend

## Introductie

De BaaVend is de naam voor de backend van dit project.
Het bestaat uit services, voor zowel backend als frontend, in Docker containers opgezet met Docker-Compose.
Voor LoRaWAN connectiviteit wordt gebruik gemaakt van The Things Network (TTN).
In dit hoofdstuk wordt de backend acrhitectuur beschreven, de algemende werking, hoe deze is opgezet, en hoe de connectiviteit naar buiten de Docker omgeving toe werkt.
De frontend als user interface en de werking hiervan volgt in het Frontend hoofdstuk.

---

## Architectuur

In dit onderdeel wordt de architectuur van de backend beschreven.
Als referentie is er onderstaand een blokdiagram met een algemeen overzicht van de structuur.

### Blokdiagram

![BaaVend Blokdiagram](./assets/baavend-diagram.png)

*__Mosquitto nog toevoegen!__

### Services

- The Things Stack FLWSB applicatie (extern op TTN) voor LoRaWAN ontvangst.
- Weerstation?
- baavend-red: Node-Red container voor dataverwerking en alles te verbinden.
- baavend-db: MongoDb container als database.
- baavend-mqtt: [Mosquitto](https://github.com/vvatelot/mosquitto-docker-compose) container als MQTT broker voor het weerstation.
- baavend-connect: Angular container met frontend web applicatie als user interface voor het Sensor Identification System (SIS).
- baavend-vis: Grafana container met frontend web applicatie voor data visualisatie.


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

#### REST API

De REST API dient als comminucatie met de frontend services.

Voor de Angular frontend web applicatie zijn volgende endpoints beschikbaar:

| Endpoint | Functie |
| --- | --- |
| / | ? |

Voor de data visualisatie in Grafana zijn de volgende endpoints beschikbaar zoals  [hier](https://grafana.com/grafana/plugins/grafana-simple-json-datasource/) beschreven:

| Endpoint | Functie |
| --- | --- |
| / | Should return 200 ok. Used for "Test connection" on the datasource config page. |
| /search | Used by the find metric options on the query tab in panels. |
| /query | Should return metrics based on input. |
| /annotations | Should return annotations. |
| /tag-keys | Should return tag keys for ad hoc filters.* |
| /tag-values | Should return tag values for ad hoc filters.* |

*_optioneel_




---
