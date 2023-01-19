# Backend

## Node-RED

Node-RED vormt het sleutelpunt van de backend. Het is een node-based omgeving voor visueel programmeren met JavaScript. Hier wordt er gesubscribed op MQTT servers voor de connectiviteit en wordt de data geformatteerd en weggeschreven naar de InfluxDb database.
Ook een deel van de frontend, het SIS web formulier, wordt hier gecodeerd.
Enkel de connectie tussen InfluxDb en Grafana gebeurt niet via Node-RED, want daar is een plug-in voor in Grafana zelf.

---

### Flows

De functionaliteiten in Node-RED worden onderverdeeld in *flows*.
Dit zijn:
 - sis-form: het Sensor Identification System (SIS) webformulier, aan de hand van Node-RED Dashboard.
 - ttn-flwsb: data verwerking voor de FLWSB-board met The Things Network (TTN).
 - ttn-sis-flwsb: data verwerking voor de FLWSB-board via The Things Network (TTN), met gebruik van SIS.
 - weather-station-sis: data verwerking voor de weerstations via de Mosquitto MQTT broker, met gebruik van SIS.
 - mqtt-logging: opslag van logging van de Mosquitto MQTT broker naar de InfluxDB database.

__*Broncode voor elke flow kan gevonden worden in deze repository onder `src\backend\baavend\node-red-flows`.
Deze kan in Node-RED geïmporteerd worden om de flow te creëren.*__

Een voorbeeld van effectieve data voor flows kan gevonden worden in [Real Data](data-formatting/real-data.md).

---

#### Sensor Identification System (SIS) Webformulier (sis-form)

Om data te kunnen ingeven in het Sensor Identification System is er een web formulier gemaakt aan de hand van Node-RED Dashboard.

![Node-RED flow sis-form.](./assets/node-red-flow-sis-form.png 'Figuur : Node-RED flow sis-form.')

Deze bestaat uit:
1. [Node-Red Dashboard](https://flows.nodered.org/node/node-red-dashboard) `form` nodes (niet standaard, apart te installeren).
2. `function` nodes voor de Data Formatting.
3. `influx out` [InfluxDB nodes](https://flows.nodered.org/node/node-red-contrib-influxdb) (niet standaard, apart te installeren)

##### Web Formulier

De `form` nodes creëren volgende web pagina:

![SIS Registration Form webpagina.](./assets/node-red-dashboard-sis-forms.png 'Figuur : SIS Registration Form webpagina.')

##### Data Formatting

De `function` nodes bevatten volgende JavaScript code om de inkomende forms te verwerken en te formateren naar een JSON object voor de push naar InfluxDB.
Dit wordt gedaan zoals bepaald in het [Data Structuur](data-formatting/data-structuur.md) onderdeel.

###### Data Formatting Board reg

```javascript
var form = msg.payload

msg.payload = [
    {
        board_name: form.board_name,
        latitude: form.latitude,
        longitude: form.longitude,
        time: new Date()
    },
    {
        board_id: form.board_id,
    }
];

return msg;
```

###### Data Formatting Sensor reg

```javascript
var form = msg.payload

msg.payload = [
    {
        sensor_name: form.sensor_name,
        nr_of_measurements: form.nr_of_measurements,
        quantity: form.quantity,
        unit: form.unit,
        range: form.range,
        conversion: form.conversion,
        datatype: form.datatype,
        time: new Date()
    },
    {
        board_id: form.board_id,
        sensor_id: form.sensor_id,
    }
];

return msg;
```

###### Data Formatting Weather Station reg

```javascript
var form = msg.payload

msg.payload = [
    {
        name: form.name,
        latitude: form.latitude,
        longitude: form.longitude,
        time: new Date()
    },
    {
        id: form.id,
    }
];

return msg;
```

##### Push naar de InfluxDb database

Om een push te kunnen doen met de `influx out` node moeten twee zaken correct ingesteld worden:
1. De node instellingen: ![InfluxDb influx-out node instellingen voorbeeld.](./assets/influxdb-node-settings.png 'Figuur : InfluxDb influx-out node instellingen voorbeeld.')

2. De server instellingen: ![InfluxDb server instellingen voorbeeld.](./assets/baavend-db-server-settings.png 'Figuur : InfluxDb server instellingen voorbeeld.')

Hierbij is de *Bucket* vergelijkbaar met een collection of afzonderlijke database, en *Measurement* vergelijkbaar met een document of tabel.
SIS heeft zijn eigen afzonderlijke Bucket met een Measurement per groep, namelijk: board, sensor, en weather-station.

Vervolgens gebeurt de push automatisch als het inkomende bericht het juiste formaat heeft.

---

#### FLWSB-board Dataverwerking (ttn-flwsb & ttn-sis-flwsb)

Data verwerking voor FLWSB-board met gebruik van The Things Network voor LoRaWAN connectiviteit.

![Node-RED flow ttn-sis-flwsb.](./assets/node-red-flow-ttn-sis-flwsb.png 'Figuur : Node-RED flow ttn-sis-flwsb.')

Deze flow bestaat uit drie, of eerder vijf, stappen:
1. MQTT msg van de TTN applicatie.
2. Flux query naar de InfluxDb database voor SIS informatie over het board en aangesloten sensoren.
3. 3a) Samenvoeging van het MQTT bericht en het query resultaat.
4. 3b) Data Formatting.
5. 3c) Push naar InfluxDb.

##### TTN MQTT msg

Voor het FLWSB-board moet er data binnen gehaald worden over MQTT vanuit de The Things Network (TTN) applicatie.

Om te kunnen subscriben zijn er drie zaken vereist:
 - TTN server adres: eu1.cloud.thethings.network
 - TTN username: "flwsb@ttn" (applicatie-naam@ttn)
 - TTN password/API key: aan te maken in de TTN applicatie.

Meer informatie beschikbaar in de [TTN MQTT documentatie](https://www.thethingsindustries.com/docs/integrations/mqtt/).

De instellingen van de node zijn als volgt:

![TTN MQTT in node instellingen.](./assets/ttn-mqtt-in-node-settings.png 'Figuur : TTN MQTT in node instellingen.')

![TTN MQTT broker node connection instellingen.](./assets/ttn-mqtt-broker-node-connection-settings.png 'Figuur : TTN MQTT broker node connection instellingen.')

![TTN MQTT broker node security instellingen.](./assets/ttn-mqtt-broker-node-security-settings.png 'Figuur : TTN MQTT broker node security instellingen.')

##### Flux Query

Om data op te halen uit het SIS moet er een query gebeuren, geschreven in Flux query-taal.
Deze haalt alle nodige informatie op om de data correct te kunnen interpreteren en formateren.

```flux
const board_id = msg.payload.end_device_ids.device_id;

// Flux query
msg.query = `from(bucket: "sis")
  |> range(start: -100y, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "sensor" or r["_measurement"] == "board")
  |> filter(fn: (r) => r["board_id"] == "${board_id}")
  |> filter(fn: (r) => r["_field"] == "board_name" or r["_field"] == "latitude" or r["_field"] == "longitude" or r["_field"] == "conversion" or r["_field"] == "nr_of_measurements" or r["_field"] == "quantity" or r["_field"] == "sensor_name" or r["_field"] == "datatype")
  |> aggregateWindow(every: 1y, fn: last, createEmpty: false)
  |> yield(name: "last")`

return msg;
```

##### Join

Deze node combineerd beide inkomende berichten eenvoudig weg door de msg.payload te combineren in een array.

#### Data formatting

```javascript
const ttn = msg.payload[0]; // TTN MQTT msg
const sis = msg.payload[1]; // SIS query result msg

// ID & Timestamp from TTN msg
const id = ttn.end_device_ids.device_id;
const timestamp = new Date(ttn.received_at);  // timestamp TTN

// Board info from SIS query
const board_name = (sis.find(obj => obj._field == "board_name"))["_value"];
const latitude = (sis.find(obj => obj._field == "latitude"))["_value"];
const longitude = (sis.find(obj => obj._field == "longitude"))["_value"];
// node.warn(`location: ${latitude}, ${longitude}`);  // Debug info

// Bitstream
function base64ToArrayBuffer(value) {
	var load = value.replace(/\s+/g, '');  // remove any whitespace
	value = Buffer.from(load, 'base64');
	return value;
}

const bitstream = base64ToArrayBuffer(ttn.uplink_message.frm_payload);
node.warn(bitstream); // Debug info

// Sensor ID
const sensor_id = bitstream[0]; // Only for signle byte ID's
node.warn(`sensor_id: ${sensor_id}`); // Debug info

// Sensor info from SIS query by Sensor ID
const sensor_name = (sis.find(obj => obj._field == "sensor_name" && obj.sensor_id == sensor_id))["_value"];
const nr_of_measurements = (sis.find(obj => obj._field == "nr_of_measurements" && obj.sensor_id == sensor_id))["_value"];
const datatype = (sis.find(obj => obj._field == "datatype" && obj.sensor_id == sensor_id))["_value"];
const quantity = (sis.find(obj => obj._field == "quantity" && obj.sensor_id == sensor_id))["_value"];
const conversion = (sis.find(obj => obj._field == "conversion" && obj.sensor_id == sensor_id))["_value"];

// Formatting the payload for InfluxDb push
msg.payload = [
	[{
		latitude: latitude,
		longitude: longitude,
		consumed_airtime: +(ttn.uplink_message.consumed_airtime.slice(0, -1)), // remove "s" and convert to number
		time: timestamp
	},
	{
		board_id: id,  // device-id TTN en SIS
		board_name: board_name,
	}]
];

let sensor_data = [
	{
		// temp: ((((bitstream[1] << 8) + bitstream[2]) / 100) - 40),
		// pressure: ((bitstream[3] << 8) + bitstream[4]),
		// humidity: bitstream[5],
		time: timestamp
	},
	{
		board_id: id,  // device-id TTN en SIS
		sensor_id: sensor_id,
		sensor_name: sensor_name,
	}
];

if (nr_of_measurements > 1) {
	// Sensor info for multiple measurements to Arrays
	const quantities = quantity.split(", ");
	node.warn(`quantities: ${quantities}`); // Debug info
	const conversions = conversion.split(", ");
	node.warn(`conversions: ${conversions}`); // Debug info
	const datatypes = datatype.split(", ");
	node.warn(`datatypes: ${datatypes}`); // Debug info

	// Define iteration length
	let length = nr_of_measurements;
	for (let i = 1; i < length; i++) { // Skip the first byte(s) of the bitstream, the sensor_id.
		node.warn(datatypes[i]);
		if (!(datatypes[i] == "byte")) {
			length++;
		}
	}
	node.warn(`length: ${length}`); // Debug info

	// Values array
	let values = [];
	for (let i = 1; i < length; i++) { // Skip the first byte(s) of the bitstream, the sensor_id.
		node.warn(datatypes[i]);
		if (datatypes[i] == "byte") {
			values[i] = bitstream[i];
		}
		else {
			values.push((bitstream[i] << 8) + bitstream[i + 1]);
			i++;
		}
	}

	// Quantities and Measurement data to key value pairs
	for (let i = 0; i < nr_of_measurements; i++) {
		sensor_data[0][`${quantities[i]}`] = values[i];
	}

	//sensor_data[0]["test"] = ((bitstream[3] << 8) + bitstream[4]),
}
else {
	if (datatype == "byte") {
		sensor_data[0][`${quantity}`] = bitstream[1];
	}
	else {
		sensor_data[0][`${quantity}`] = (bitstream[1] << 8) + bitstream[2];
	}
}

node.warn(sensor_data[0]); // Debug info
msg.payload.push(sensor_data);

return msg;
```

##### PoC Flow

Een vereenvoudigde versie van de flow specifiek voor de SAMDaaNo21 Proof-of-Concept verbonden met een BME280:

![Node-RED flow ttn-flwsb.](./assets/node-red-flow-ttn-flwsb.png 'Figuur : Node-RED flow ttn-flwsb.')

---

#### Weerstations Dataverwerking (weather-station-sis)

Data verwerking voor de weerstations.

![Node-RED flow weather-station-sis.](./assets/node-red-flow-weather-station-sis.png 'Figuur : Node-RED flow weather-station-sis.')

Deze flow gebeurt zeer gelijkaardig aan de *ttn-sis-flwsb* flow.

##### Mosquitto MQTT

De instellingen van de MQTT node zijn als volgt:

![Mosquitto MQTT (baavend-mqtt) in node instellingen.](./assets/baavend-mqtt-in-node-settings.png 'Figuur : Mosquitto MQTT (baavend-mqtt)  in node instellingen.')

![Mosquitto MQTT (baavend-mqtt)  broker node connection instellingen.](./assets/baavend-mqtt-broker-node-connection-settings.png 'Figuur : Mosquitto MQTT (baavend-mqtt)  broker node connection instellingen.')

![Mosquitto MQTT (baavend-mqtt)  broker node security instellingen.](./assets/baavend-mqtt-broker-node-security-settings.png 'Figuur : Mosquitto MQTT (baavend-mqtt)  broker node security instellingen.')

##### Flux Query

```flux
msg.query = `from(bucket: "sis")
  |> range(start: -100y, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "weather-station")
  |> filter(fn: (r) => r["_field"] == "name")
  |> aggregateWindow(every: 1y, fn: last, createEmpty: false)
  |> yield(name: "last")`

return msg;
```


##### Data formatting

```javascript
let mqtt = msg.payload[0];
let sis = msg.payload[1];

let source_id = (sis.find(obj => obj.id == mqtt.id))["_value"];

msg.payload = [
	{
		temp: mqtt.temperature_C,          // buiten temperatuur, °C, float
		humidity: mqtt.humidity,           // buiten luchtvochtigheid, %, int
		wind_speed: mqtt.wind_avg_m_s,     // windsnelheid, m/s, float
		wind_gust: mqtt.wind_max_m_s,      // windsnelheid, m/s, float
		wind_direction: mqtt.wind_dir_deg, // windrichting, hoek in graden °, int
		rain: mqtt.rain_mm,                // neerslag, mm/10min, float
		time: new Date(mqtt.time)		  // timestamp, YYYY-MM-DD hh:mm:ss
	},
	{
		source: source_id
	}];

return msg;
```

---

#### Mosquitto MQTT Broker Logging (mqtt-logging)

![Node-RED flow mqtt-logging.](./assets/node-red-flow-mqtt-logging.png 'Figuur : Node-RED flow mqtt-logging.')

```javascript

```

---

### Troubleshooting

#### Docker op Linux Virtual Machine

Bij het opstarten van de Node-RED container op een Linux Virtual Machine kan je stuiten op volgende error:

```bash
baavend-red  | <date time> - [error] Failed to start server:
baavend-red  | <date time> - [error] Error: EACCES: permission denied, mkdir '/data/node_modules'
```

Dit gebeurt omdat er volumes gemount worden en de user van de Docker container geen rechten heeft om in de directories van de host user te schrijven.
Voor Node-RED is de container user uid 1000. Om deze error op te lossen moet er dus schrijf rechten gegeven worden aan deze uid, zoals beschreven in [deze oplossing op stackoverflow](https://stackoverflow.com/questions/74487200/can-i-run-node-red-under-docker-on-vm-eflow-azure-iot-edge-on-windows-device/74488060#74488060).
Voor baavend-red wordt dit commando:

```bash
sudo chown -R 1000:1000 ~/baavend/baavend-red/
```

#### Credentials error bij Deployment

Bij het herstarten van docker krijg je een error over dat de credentials decryption niet lukt en dat er nieuwe credentials gemaakt worden met `$$$` achtervoegsel.

Errors:
```bash
"Flushing file /data/flows_cred.json to disk failed : Error: EBUSY: resource busy or locked, rename '/data/flows_cred.json.$$$' -> '/data/flows_cred.json'"

"Error saving flows: EBUSY: resource busy or locked, rename '/data/flows_cred.json.$$$' -> '/data/flows_cred.json'"
```

Voer de volgende commandos uit om deze te kunnen gebruiken en terug te kunnen deployen.

```bash
rm flows.json
rm flows_cred.json
cp 'flows.json.$$$' flows.json
cp 'flows_cred.json.$$$' flows_cred.json
hmod +x flows.json
chmod +x flows_cred.json
```
