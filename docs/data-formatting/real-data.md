# Data Formatting

## Effectieve Data

In het onderdeel [Data Structuur](./data-formatting/data-structure.md) is uiteengezet hoe de data er kan uitzien enkele stappen in de datastroom. Er wordt ook toegelicht hoe deze verwerkt kan worden.

In dit onderdeel worden de datastromen van effectieve (real) data bekeken.

1. Sensor data SAMDaaNo21 over LoRaWAN
2. Weather Station data over MQTT

![FLWSB Project overzichtsdiagram.](./assets/project-overview-diagram.jpg 'Figuur 1: FLWSB Project overzichtsdiagram.')

---

### Sensor data SAMDaaNo21 over LoRaWAN

Een illustratie van hoe de data van een meting van de BME280, die temperatuur, luchtdruk en luchtvochtigheid bevat, wordt verzonden en verwerkt wordt in de backend.

#### SIS Web Formulieren

Voor er data wordt verzonden moeten zowel het board als de hierop eengesloten sensoren worden geregistreerd in het SIS, of Sensor Identification System, via een web formulier.

![SIS web forms voorbeeld.](./assets/node-red-dashboard-sis-forms.png 'Figuur 2: SIS web forms voorbeeld.')

Dit werkt met volgende Node-RED flow:

![SIS web forms Node-RED flow.](./assets/node-red-flow-sis-form.png 'Figuur 3: SIS web forms Node-RED flow.')

Dit brengt volgende msg's in Node-RED binnen:

```javascript
{
  "payload":
  {
    "board_id":"eui-0004a30b0020da72",
    "sensor_id":8,
    "sensor_name":"BME280",
    "nr_of_measurements":3,
    "quantity":"temp, pressure, humidity",
    "unit":"°C, hPa, %",
    "range":"-40.00 85.00, 300 1100, 0 100",
    "conversion":"/100 -40, 1, 1",
    "datatype":"float, uint16_t, byte"
  },
  "socketid":"ScYUaiaHGHdfmQYWAAAT",
  "_msgid":"804621b4d4723594"
}
```

```javascript
{
  "payload":
  {
    "board_id":"eui-0004a30b0020da72",
    "board_name":"samdaano21-poc",
    "latitude":51.22999030805754,
    "longitude":4.416285765591264
  },
  "socketid":"ScYUaiaHGHdfmQYWAAAT",
  "_msgid":"a973b9015232c834"
}
```

Met resulterende push naar de InfluxDb database:

```javascript
[
  {
    "sensor_name":"BME280",
    "nr_of_measurements":3,
    "quantity":"temp, pressure, humidity",
    "unit":"°C, hPa, %",
    "range":"-40.00 85.00, 300 1100, 0 100",
    "conversion":"/100 -40, 1, 1",
    "datatype":"float, uint16_t, byte",
    "time":"2023-01-17T21:50:37.960Z"
  },
  {
    "board_id":"eui-0004a30b0020da72",
    "sensor_id":8
  }
]
```

```javascript
[
  {
    "board_name":"samdaano21-poc",
    "latitude":51.22999030805754,
    "longitude":4.416285765591264,
    "time":"2023-01-17T21:50:42.690Z"
  },
  {
    "board_id":"eui-0004a30b0020da72"
  }
]
```

Het resultaat in de InfluxDb database Data Explorer web interface.

![SIS data in InfluxDb Data Explorer web interface.](./assets/sis-influxdb-board-sensor.png 'Figuur 4: SIS data in InfluxDb Data Explorer web interface.')

#### Bitstream

De meting wordt opgevraagd en omgezet van een byte array naar een bitstream:

```c
// Voorbeeld code van op de SAMDaaNo21
```

```

De verzonden bitstream, of toch enkel de data zelf, ziet er als volgt uit:
```c
00001000
00010111
11010100
00000011
11101001
00110000
```

Dit representeerd volgende bytes array: `[8,23,212,3,233,48]`.

#### TTN Uplink message

Eens ontvangen door The Things Network wordt de bitstream omgezet in een Uplink message om te verzenden over MQTT en wordt vervolgens ontvangen in Node-RED.

De bitstream wordt omgezet naar `CBfUA+kw` in [Base64 (RFC 3548, RFC 4648)](https://cryptii.com/pipes/base64-to-binary) codering. Deze komt terecht in `msg.payload.uplink_message.frm_payload`.

Er is verder een hele hoop extra data aan toegevoegd.
Onderstaande code is het volledige msg object. Hierbij representeerd `data` de `msg.payload`.

```javascript
{
  "name": "as.up.data.forward",
  "time": "2022-12-23T16:58:11.318059995Z",
  "identifiers": [
    {
      "device_ids": {
        "device_id": "eui-0004a30b0020da72",
        "application_ids": {
          "application_id": "flwsb"
        },
        "dev_eui": "0004A30B0020DA72",
        "join_eui": "0004A30B0020DA72",
        "dev_addr": "260B386C"
      }
    }
  ],
  "data": {
    "@type": "type.googleapis.com/ttn.lorawan.v3.ApplicationUp",
    "end_device_ids": {
      "device_id": "eui-0004a30b0020da72",
      "application_ids": {
        "application_id": "flwsb"
      },
      "dev_eui": "0004A30B0020DA72",
      "join_eui": "0004A30B0020DA72",
      "dev_addr": "260B386C"
    },
    "correlation_ids": [
      "as:up:01GMZYQEFJ9WFPS1RANANBJK6A",
      "ns:uplink:01GMZYQE8VDPC2WR4K8R9C359Q",
      "pba:conn:up:01GM367NPGXHWVSHN6JFKFKPVR",
      "pba:uplink:01GMZYQE8RVEDGBZC7S9ZJ7RJZ",
      "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01GMZYQE8VN437T3PHHFFF16ZN",
      "rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01GMZYQEFH6D3MQKT445TBD0ET"
    ],
    "received_at": "2022-12-23T16:58:11.314080290Z",
    "uplink_message": {
      "session_key_id": "AYU/6AGa+vh+WfbYP5XQGA==",
      "f_port": 1,
      "f_cnt": 33,
      "frm_payload": "CBfUA+kw",
      "decoded_payload": {
        "bytes": [
          8,
          23,
          212,
          3,
          233,
          48
        ]
      },
      "rx_metadata": [
        {
          "gateway_ids": {
            "gateway_id": "packetbroker"
          },
          "packet_broker": {
            "message_id": "01GMZYQE8RVEDGBZC7S9ZJ7RJZ",
            "forwarder_net_id": "000013",
            "forwarder_tenant_id": "ttnv2",
            "forwarder_cluster_id": "ttn-v2-legacy-eu",
            "forwarder_gateway_eui": "7276FF0000062E94",
            "forwarder_gateway_id": "eui-7276ff0000062e94",
            "home_network_net_id": "000013",
            "home_network_tenant_id": "ttn",
            "home_network_cluster_id": "eu1.cloud.thethings.network"
          },
          "time": "2022-12-23T16:58:09.998443Z",
          "fine_timestamp": "955291031",
          "rssi": -111,
          "signal_rssi": -113,
          "channel_rssi": -111,
          "snr": 1,
          "frequency_offset": "4464",
          "location": {
            "latitude": 51.22994085,
            "longitude": 4.41383496,
            "altitude": 30
          },
          "uplink_token": "eyJnIjoiWlhsS2FHSkhZMmxQYVVwQ1RWUkpORkl3VGs1VE1XTnBURU5LYkdKdFRXbFBhVXBDVFZSSk5GSXdUazVKYVhkcFlWaFphVTlwU25Oa2F6RkRWakJzYWxJelNtOVBWVnBMVFRJMWRFbHBkMmxrUjBadVNXcHZhVmRYZUZkV1ZGRXlVWHBWTVZKck1IUlZVekV3WWxjMVdFMVhiRmxSVTBvNUxqUlRUMWg1YkU1R01HZG5Ra1EwVnpsTmF6WnJUMEV1TVdnMU9IaGtjMWRNVjFNNU5FSmhTQzVVTW5ONFIxSllWMmxwWlV4NVZYaGpaMGs0UVZSaU9HbFZORGhaZWt4UGNWbEVaRlY2Tlc5SGVrSnBMVU5rYXpJMGRGQkxaVVpMYWpVMWRXNU5Tbk14UTBOd2NpMVRkbTFoT0Y5SGRFTmxTVXRIUzBWNFR6Rm9jMlExVTBoT05HTm1UV3BOV2xFNE5tZGlWRE4zUkZWSWFWTndlazQyYlZkclgyZzFaak5ZUkVablQzVXpUWFZaYlRKMlVqWTNkSEV0UXpBMFNVUnplVFZ5VkVrd1NtdGlWM0JxVkd4RFIwZE1iRnBZZW1OVkxrTklhMVk0V0hCbGRHcEJTa1JpVFRGaVJsaFpSbEU9IiwiYSI6eyJmbmlkIjoiMDAwMDEzIiwiZnRpZCI6InR0bnYyIiwiZmNpZCI6InR0bi12Mi1sZWdhY3ktZXUifX0=",
          "received_at": "2022-12-23T16:58:11.093770044Z"
        },
        {
          "gateway_ids": {
            "gateway_id": "packetbroker"
          },
          "packet_broker": {
            "message_id": "01GMZYQE8RVEDGBZC7S9ZJ7RJZ",
            "forwarder_net_id": "000013",
            "forwarder_tenant_id": "ttnv2",
            "forwarder_cluster_id": "ttn-v2-legacy-eu",
            "forwarder_gateway_eui": "7276FF0000062E94",
            "forwarder_gateway_id": "eui-7276ff0000062e94",
            "home_network_net_id": "000013",
            "home_network_tenant_id": "ttn",
            "home_network_cluster_id": "eu1.cloud.thethings.network"
          },
          "antenna_index": 1,
          "time": "2022-12-23T16:58:09.998443Z",
          "rssi": -112,
          "signal_rssi": -117,
          "channel_rssi": -112,
          "rssi_standard_deviation": 1,
          "snr": -4,
          "frequency_offset": "4457",
          "uplink_token": "eyJnIjoiWlhsS2FHSkhZMmxQYVVwQ1RWUkpORkl3VGs1VE1XTnBURU5LYkdKdFRXbFBhVXBDVFZSSk5GSXdUazVKYVhkcFlWaFphVTlwU25Oa2F6RkRWakJzYWxJelNtOVBWVnBMVFRJMWRFbHBkMmxrUjBadVNXcHZhVmRYZUZkV1ZGRXlVWHBWTVZKck1IUlZVekV3WWxjMVdFMVhiRmxSVTBvNUxqUlRUMWg1YkU1R01HZG5Ra1EwVnpsTmF6WnJUMEV1TVdnMU9IaGtjMWRNVjFNNU5FSmhTQzVVTW5ONFIxSllWMmxwWlV4NVZYaGpaMGs0UVZSaU9HbFZORGhaZWt4UGNWbEVaRlY2Tlc5SGVrSnBMVU5rYXpJMGRGQkxaVVpMYWpVMWRXNU5Tbk14UTBOd2NpMVRkbTFoT0Y5SGRFTmxTVXRIUzBWNFR6Rm9jMlExVTBoT05HTm1UV3BOV2xFNE5tZGlWRE4zUkZWSWFWTndlazQyYlZkclgyZzFaak5ZUkVablQzVXpUWFZaYlRKMlVqWTNkSEV0UXpBMFNVUnplVFZ5VkVrd1NtdGlWM0JxVkd4RFIwZE1iRnBZZW1OVkxrTklhMVk0V0hCbGRHcEJTa1JpVFRGaVJsaFpSbEU9IiwiYSI6eyJmbmlkIjoiMDAwMDEzIiwiZnRpZCI6InR0bnYyIiwiZmNpZCI6InR0bi12Mi1sZWdhY3ktZXUifX0=",
          "received_at": "2022-12-23T16:58:11.093770044Z"
        }
      ],
      "settings": {
        "data_rate": {
          "lora": {
            "bandwidth": 125000,
            "spreading_factor": 7,
            "coding_rate": "4/5"
          }
        },
        "frequency": "867100000"
      },
      "received_at": "2022-12-23T16:58:11.099382830Z",
      "consumed_airtime": "0.051456s",
      "network_ids": {
        "net_id": "000013",
        "tenant_id": "ttn",
        "cluster_id": "eu1",
        "cluster_address": "eu1.cloud.thethings.network"
      }
    }
  },
  "correlation_ids": [
    "as:up:01GMZYQEFJ9WFPS1RANANBJK6A",
    "ns:uplink:01GMZYQE8VDPC2WR4K8R9C359Q",
    "pba:conn:up:01GM367NPGXHWVSHN6JFKFKPVR",
    "pba:uplink:01GMZYQE8RVEDGBZC7S9ZJ7RJZ",
    "rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01GMZYQE8VN437T3PHHFFF16ZN",
    "rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01GMZYQEFH6D3MQKT445TBD0ET"
  ],
  "origin": "ip-10-100-4-181.eu-west-1.compute.internal",
  "context": {
    "tenant-id": "CgN0dG4="
  },
  "visibility": {
    "rights": [
      "RIGHT_APPLICATION_TRAFFIC_READ"
    ]
  },
  "unique_id": "01GMZYQEFP4GQ5WK1EW6PWYFV2"
}
```

##### Payload formatter

De `decoded_payload` wordt toegevoegd als er een Payload formatter voorzien wordt in de TTN applicatie. Hier is de standaard formatter gebruikt als debugging methode. Zo kan de base64 string die in `frm_payload` zit, de verzonden bitstream, al worden gelezen als afzonderlijke bytes.

Deze Payload formatter is, net zoals de code in Node-RED, JavaScript.
De volgende code, de standaard code die gegeven wordt door TTN onder *Custom Javascript formatter* is gebruikt.

```JavaScript
function decodeUplink(input) {
  return {
    data: {
      bytes: input.bytes
    },
    warnings: [],
    errors: []
  };
}
```

![TTN FLWSB applicatie default payload formatter.](./assets/ttn-flwsb-app-payload-formatter.png 'Figuur 5: TTN FLWSB applicatie default payload formatter.')

Er wordt in dit project verder gekozen om geen gebruik te maken van de Payload formatter in de TTN applicatie om de controle over het formatteren in de eigen backend in Node-Red te houden. Dit geeft bnetere flexibiliteit.

#### Base64

De `frm_payload` bevat de bitstream die door TTN ontvangen is. Deze is echter gecodeerd als een base64 string. Om de data te kunnen formatteren moet deze eerst worden omgezet in een byte array.

Omzetting functie van base64 naar bytes array, of Buffer:

```javascript
function base64ToArrayBuffer(value) {
	var load = value.replace(/\s+/g, '');  // remove any whitespace
	value = Buffer.from(load, 'base64');
	return value;
}
```

Links:
- [Node-RED javascript code om base64 om te zetten in een bytes Buffer](https://github.com/node-red/node-red-nodes/blob/master/parsers/base64/70-base64.js)
- [Base64 data omzetter](https://cryptii.com/pipes/base64-to-binary)

#### Formateren in Node-RED JavaScript

Om de data nu te gaan schrijven naar de InfluxDb database moet deze gestructureerd worden om aan het bepaalde model te voldoen.

![Node-RED ttn-sis-flwsb flow.](./assets/node-red-flow-ttn-sis-flwsb.png 'Figuur 6: Node-RED ttn-sis-flwsb flow.')

Eerst gebeurt er een query naar de `sis` bucket inde InfluxDb database voor de nodige informatie.

```javascript
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

Vervolgens wordt de `ttn` data geformatteerd aan de hand van deze `sis` query.

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

*Conversions, of omzettingen, zijn nog niet geïmplementeerd in deze code.*

#### InfluxDb query voor visualisatie in Grafana

Een query in Flux, de gespesialiseerde query taal van InfluxDb, om de data op te vragen voor visualisatie.
De time range wordt in het dashboard van Grafana ingesteld.

```flux
from(bucket: "flwsb")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "climate_data")
  |> filter(fn: (r) => r["_field"] == "temp, pressure, humidity")
  |> filter(fn: (r) => r["board_id"] == "eui-0004a30b0020da72")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

Het resultaat in Grafana Dashboard:

![Query resultaat visualisatie in Grafana dashboard van climate_data van de SAMDaaNo21, meer precies temperatuur, luchtdruk en luchtvochtigheid.](./assets/real-data-grafana-dashboard-climate-data-samdaano21.png 'Figuur 7: Query resultaat visualisatie in Grafana dashboard van climate_data van de SAMDaaNo21, meer precies temperatuur, luchtdruk en luchtvochtigheid.')

---

### Weather Station data over MQTT

#### Weerstation

Het weerstation zelf is een blackbox. Hoe de data hier juist verwerkt wordt is onbekend.

#### Raspberry Pi met RTL-SDR

De verwerking hier gebeurd geautomatiseerd door de gebruikte applicatie.
Er zijn beperkte opties voor het formateren van deze data beschikbaar.
Het betreft een open-source applicatie met repository op GitHub, maar hoe deze applicatie juist werkt is niet noodzakelijk te weten voor deze toepassing.
Voor meer info zie [ Weather STation: Reading/Sending Data](./weather-station/data.md).

#### Mosquitto MQTT Broker

#### SIS Web Formulier

Om de juiste herkening te kunnen doen in Node-RED moet het weerstation eerst geregistreerd worden in het SIS, of Sensor Identification System.

![SIS web forms voorbeeld.](./assets/node-red-dashboard-sis-forms.png 'Figuur 2: SIS web forms voorbeeld.')

Dit werkt met volgende Node-RED flow:

![SIS web forms Node-RED flow.](./assets/node-red-flow-sis-form.png 'Figuur 3: SIS web forms Node-RED flow.')

Dit brengt volgende msg's in Node-RED binnen:

```javascript
{
  "payload":
  {
    "id":-1646443428,
    "name":"weather-station-2",
    "latitude":51.23016015597968,
    "longitude":4.4162325532681965
  },
  "socketid":"ScYUaiaHGHdfmQYWAAAT",
  "_msgid":"474efd8c5d401103"}
```

En volgende data wordt gepushed naar de InfluxDb database:

```javascript
[
  {
    "name":"weather-station-2",
    "latitude":51.23016015597968,
    "longitude":4.4162325532681965,
    "time":"2023-01-17T22:26:49.039Z"
  },
  {
    "id":-1646443428
  }
]
```

Het resultaat in de InfluxDb database Data Explorer:

![SIS data in InfluxDb Data Explorer web interface.](./assets/sis-influxdb-weather-station.png 'Figuur 8: SIS data in InfluxDb Data Explorer web interface.')

#### Node-RED backend

De data van het weerstation komt via MQTT binnen in Node-Red als een JSON object.
Er worden twee verschillende structuren doorgestuurd:

```json
{
  "topic":"weatherStation",
  "payload":
    {
      "time":"2022-12-16 14:53:13",
      "model":"Bresser6in1",
      "id":102004230,
      "channel":0,
      "battery_ok":1,
      "temperature_C":22.6,
      "humidity":21,
      "sensor_type":1,
      "wind_max_m_s":0,
      "wind_avg_m_s":0,
      "wind_dir_deg":248
      "mic":"CRC"
    },
  "qos":0,
  "retain":false,
  "_msgid":"48936e3e111fd7d7"
}
```
*Bovenstaande bevat geen `"rain_mm"`.*

*Onderstaande bevat geen `"temperature_C" en "humidity"`.*

```json
{
  "topic":"weatherStation",
  "payload":
    {"time":"2022-12-16 14:53:49",
    "model":"Bresser6in1",
    "id":102004230,
    "channel":0,
    "battery_ok":1,
    "sensor_type":1,
    "wind_max_m_s":0,
    "wind_avg_m_s":0,
    "wind_dir_deg":248,
    "rain_mm":15.6,
    "mic":"CRC"
  },
  "qos":0,
  "retain":false,
  "_msgid":"0835226af4c8083b"
}
```

##### Formatteren

Het formatteren voor InfluxDb gebeurt in twee stappen.

![Node-RED weather-station-sis flow.](./assets/node-red-flow-weather-station-sis.png 'Figuur 9: Node-RED weather-station-sis flow.')

Eerst wordt de nodige SIS informatie opgevraagd via een Flux query:

```javascript
msg.query = `from(bucket: "sis")
  |> range(start: -100y, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "weather-station")
  |> filter(fn: (r) => r["_field"] == "name")
  |> aggregateWindow(every: 1y, fn: last, createEmpty: false)
  |> yield(name: "last")`

return msg;
```

Vervolgens gebeurt de data formatting voor de push naar de InfluxDb database:

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

#### InfluxDb query voor visualisatie in Grafana

Een query in Flux, de gespesialiseerde query taal van InfluxDb, om de data op te vragen voor visualisatie.
De time range wordt in het dashboard van Grafana ingesteld.
Een gemiddelde berekening in de query kan nodig zijn om het aantal datapunten die gereturned wordt door InfluxDb te beperken.

Volgende query geeft alle data van een bepaald weerstation id weer:

```flux
from(bucket: "flwsb")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "weather_station")
  |> filter(fn: (r) => r["source"] == "weather-station-2")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

Het resultaat in Grafana Dashboard:

![Query resultaat visualisatie in Grafana dashboard van alle data van weather-station-2.](./assets/real-data-grafana-weather-station-all.png 'Figuur 6: Query resultaat visualisatie in Grafana dashboard van alle data van weather-station-2.')

Of enkel een gespecifieërde meting visualiseren, maar van meerdere bronnen gebeurd als volgt:

```flux
from(bucket: "flwsb")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "weather_station")
  |> filter(fn: (r) => r["_field"] == "temp")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
  |> movingAverage(n: 5)
```

Het resultaat in Grafana Dashboard:

![Query resultaat visualisatie in Grafana dashboard van temperatuur data van de twee weather_stations.](./assets/real-data-grafana-weather-station-temp.png 'Figuur 7: Query resultaat visualisatie in Grafana dashboard van temperatuur data van de twee weather_stations.')
