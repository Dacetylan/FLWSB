# Data Formatting

## Effectieve Data

In het onderdeel [Data Structuur](./data-formatting/data-structure.md) is uiteengezet hoe de data er kan uitzien enkele stappen in de datastroom. Er wordt ook toegelicht hoe deze verwerkt kan worden.

In dit onderdeel worden de datastromen van effectieve (real) data bekeken.

1. Sensor data SAMDaaNo21 over LoRaWAN
2. Weather Station data over MQTT

### Sensor data SAMDaaNo21 over LoRaWAN

Een illustratie van hoe de data van een meting van de BME280, die temperatuur, luchtdruk en luchtvochtigheid bevat, wordt verzonden en verwerkt wordt in de backend.

#### SIS Web Formulieren

Voor er data wordt verzonden moeten zowel het board als de hierop eengesloten sensoren worden geregistreerd in het SIS, of Sensor Identification System, via een web formulier.

![SIS web forms voorbeeld.](./assets/node-red-dashboard-sis-forms.png 'Figuur 1: SIS web forms voorbeeld.')

Dit werkt met volgende Node-RED flow:

![SIS web forms Node-RED flow.](./assets/node-red-flow-sis-form.png 'Figuur 2: SIS web forms Node-RED flow.')

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

![SIS data in InfluxDb Data Explorer web interface.](./assets/sis-influxdb-board-sensor.png 'Figuur 3: SIS data in InfluxDb Data Explorer web interface.')

#### Bitstream

De meting wordt opgevraagd en omgezet van een byte array naar een bitstream:

```c
// Voorbeeld code van op de SAMDaaNo21
```

```

De verzonden bitstream, of toch enkel de data zelf, ziet er als volgt uit:
```c
0101 0110 // DEC 86
1110 1001 // DEC 233
1111 1111 // DEC 255
0010 1111 // DEC 47
0110 0100 // DEC 100
```

#### TTN Uplink message

Eens ontvangen door The Things Network wordt de bitstream omgezet in een Uplink message om te verzenden over MQTT en wordt vervolgens ontvangen in Node-RED.
Er is een hele hoop extra data aan toegevoegd, en dit ziet er als volgt uit:

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
      "frm_payload": "Vun/L2Q=",
      "decoded_payload": {
        "bytes": [
          86,
          233,
          255,
          47,
          100
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

Om de data nu te gaan schrijven naar de InfluxDb database moet deze gestructureerd worden om aan het bepaalde model te voldoen. Onderstaande code is de code in het functie blok tussen de MQTT ontvanger en het InfluxDb schrijver blok.

```javascript
let id = msg.payload.end_device_ids.device_id;
//var location = msg.payload.locations.frm_payload;
let timestamp = new Date(msg.payload.received_at);  // timestamp TTN

function base64ToArrayBuffer(value) {
	var load = value.replace(/\s+/g, '');  // remove any whitespace
	value = Buffer.from(load, 'base64');
	return value;
}

let bitstream = base64ToArrayBuffer(msg.payload.uplink_message.frm_payload);
node.warn(bitstream);

msg.payload = [
	[{ // fields
		temp: ((((bitstream[0] << 8) + bitstream[1]) /100) -40),
		pressure: ((bitstream[2] << 8) + bitstream[3]),
		humidity: bitstream[4],
		time: timestamp
	},
	{ // tags
		board_id: "eui-0004a30b0020da72",  // devioce_id on TTN
		sensor: "BME280"
	}],

	[{ // fields
		//latitude: location.latitude,  // TTN device location latitude
		//longitude: location.longitude,  // TTN device location longitude
		consumed_airtime: +(msg.payload.uplink_message.consumed_airtime.slice(0, -1)), // remove "s" and convert to number
		time: timestamp
	},
	{ // tags
		board_id: "eui-0004a30b0020da72"  // devioce_id on TTN
	}]
];
return msg;
```

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

![Query resultaat visualisatie in Grafana dashboard van climate_data van de SAMDaaNo21, meer precies temperatuur, luchtdruk en luchtvochtigheid.](./assets/real-data-grafana-dashboard-climate-data-samdaano21.png 'Figuur 4: Query resultaat visualisatie in Grafana dashboard van climate_data van de SAMDaaNo21, meer precies temperatuur, luchtdruk en luchtvochtigheid.')

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

![SIS web forms voorbeeld.](./assets/node-red-dashboard-sis-forms.png 'Figuur 1: SIS web forms voorbeeld.')

Dit werkt met volgende Node-RED flow:

![SIS web forms Node-RED flow.](./assets/node-red-flow-sis-form.png 'Figuur 2: SIS web forms Node-RED flow.')

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

![SIS data in InfluxDb Data Explorer web interface.](./assets/sis-influxdb-weather-station.png 'Figuur 5: SIS data in InfluxDb Data Explorer web interface.')

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

Het formatteren voor InfluxDb gebeurt aan de hand van onderstaande code.

```javascript
var tmp = msg.payload
msg.payload = [
	{ // fields
		temp: tmp.temperature_C,          // buiten temperatuur, °C, float
		humidity: tmp.humidity,           // buiten luchtvochtigheid, %, int
		wind_speed: tmp.wind_avg_m_s,     // windsnelheid, m/s, float
		wind_gust: tmp.wind_max_m_s,      // windsnelheid, m/s, float
		wind_direction: tmp.wind_dir_deg, // windrichting, hoek in graden °, int
		rain: tmp.rain_mm,                // neerslag, mm/10min, float
		time: tmp.time					// timestamp, YYYY-MM-DD hh:mm:ss
	},
	{ // tags
		source: "weather-station-1"
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
