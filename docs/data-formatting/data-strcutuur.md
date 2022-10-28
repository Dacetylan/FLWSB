## Data Structuur

In dit onderdeel wordt bekeken hoe de data vanuit The Things Network in de backend binenkomt. Hoe de data in de database kan worden opgeslagen en hoe dit dan effectief zal gebeuren.

### The Things Network (TTN) & The Things Stack applicatie

De data die ontvangen wordt via MQTT uit de TTN applicatie is een JSON object die de bitstream bevat van het FLWSB-board, maar ook nog een hoop extra informatie aangeleverd door TTN. In onderstaand code block staat de beschrijving van elk onderdeel van een uplink message.

```javascript
{
  "end_device_ids" : {
    "device_id" : "dev1",                    // Device ID
    "application_ids" : {
      "application_id" : "app1"              // Application ID
    },
    "dev_eui" : "0004A30B001C0530",          // DevEUI of the end device
    "join_eui" : "800000000000000C",         // JoinEUI of the end device (also known as AppEUI in LoRaWAN versions below 1.1)
    "dev_addr" : "00BCB929"                  // Device address known by the Network Server
  },
  "correlation_ids" : [ "as:up:01...", ... ],// Correlation identifiers of the message
  "received_at" : "2020-02-12T15:15..."      // ISO 8601 UTC timestamp at which the message has been received by the Application Server
  "uplink_message" : {
    "session_key_id": "AXA50...",            // Join Server issued identifier for the session keys used by this uplink
    "f_cnt": 1,                              // Frame counter
    "f_port": 1,                             // Frame port
    "frm_payload": "gkHe",                   // Frame payload (Base64)
    "decoded_payload" : {                    // Decoded payload object, decoded by the device payload formatter
      "temperature": 1.0,
      "luminosity": 0.64
    },
    "rx_metadata": [{                        // A list of metadata for each antenna of each gateway that received this message
      "gateway_ids": {
        "gateway_id": "gtw1",                // Gateway ID
        "eui": "9C5C8E00001A05C4"            // Gateway EUI
      },
      "time": "2020-02-12T15:15:45.787Z",    // ISO 8601 UTC timestamp at which the uplink has been received by the gateway
      "timestamp": 2463457000,               // Timestamp of the gateway concentrator when the message has been received
      "rssi": -35,                           // Received signal strength indicator (dBm)
      "channel_rssi": -35,                   // Received signal strength indicator of the channel (dBm)
      "snr": 5.2,                            // Signal-to-noise ratio (dB)
      "uplink_token": "ChIKEA...",           // Uplink token injected by gateway, Gateway Server or fNS
      "channel_index": 2                     // Index of the gateway channel that received the message
      "location": {                          // Gateway location metadata (only for gateways with location set to public)
        "latitude": 37.97155556731436,       // Location latitude
        "longitude": 23.72678801175413,      // Location longitude
        "altitude": 2,                       // Location altitude
        "source": "SOURCE_REGISTRY"          // Location source. SOURCE_REGISTRY is the location from the Identity Server.
      }
    }],
    "settings": {                            // Settings for the transmission
      "data_rate": {                         // Data rate settings
        "lora": {                            // LoRa modulation settings
          "bandwidth": 125000,               // Bandwidth (Hz)
          "spreading_factor": 7              // Spreading factor
        }
      },
      "coding_rate": "4/6",                  // LoRa coding rate
      "frequency": "868300000",              // Frequency (Hz)
    },
    "received_at": "2020-02-12T15:15..."     // ISO 8601 UTC timestamp at which the uplink has been received by the Network Server
    "consumed_airtime": "0.056576s",         // Time-on-air, calculated by the Network Server using payload size and transmission settings
    "locations": {                           // End device location metadata
      "user": {
        "latitude": 37.97155556731436,       // Location latitude
        "longitude": 23.72678801175413,      // Location longitude
        "altitude": 10,                      // Location altitude
        "source": "SOURCE_REGISTRY"          // Location source. SOURCE_REGISTRY is the location from the Identity Server.
      }
    },
    "version_ids": {                          // End device version information
        "brand_id": "the-things-products",    // Device brand
        "model_id": "the-things-uno",         // Device model
        "hardware_version": "1.0",            // Device hardware version
        "firmware_version": "quickstart",     // Device firmware version
        "band_id": "EU_863_870"               // Supported band ID
    },
    "network_ids": {                          // Network information
      "net_id": "000013",                     // Network ID
      "tenant_id": "tenant1",                 // Tenant ID
      "cluster_id": "eu1"                     // Cluster ID
    }
  },
  "simulated": true,                         // Signals if the message is coming from the Network Server or is simulated.
}
```
[_Bron: The Things Stack v3.22.0 - Reference - Data Formats - JSON Payload_](https://www.thethingsindustries.com/docs/reference/data-formats/)

_Note: Deze data blijkt wel niet helemaal up-to-date. De informatie van de Identity Server moet worden opgehaald uit een API. Dit is de locatie die handmatig kan worden ingesteld op The Things Stack applicatie. De end device location metadata heeft ook een ander formaat, zie onderstaande code block en Figuur 1._

![TTN uplink message in Node-RED, Zanzibar Project 2022](./assets/zanzibar/node-red-ttn-uplink-msg.png ":size=900")
_Figuur 1.: TTN uplink message in Node-RED, Zanzibar Project 2022_

Het meeste van deze informatie is niet nuttig voor dit project en zal dus niet worden bijgehouden. Wat wel zal bijgehouden worden is:

- ```payload/device-id```: het id toegekend in The Things Stack applicatie.
- ```payload/frm_payload```: de verzonden bitstream.
- ```payload/rx_metadata/0/time```: tijd waarop de gateway het bericht ontvangen heeft.
- ```payload/locations/frm-payload/latitude & longitude```: coördinaten van het FLWSB-board, automatisch ingesteld door TTN.

```javascript
{
   topic: "v3/flwsb@ttn/devices/<device_id>/up",
   payload: {
      end_device_ids: {
         device_id: "<device-id>",
         ...
      received_at: "<timestamp, ISO 8601 YYYY-MM-DDTHH:mm:ss.sssZ>"
      uplink_message: {
          ...
          frm_payload: "<bitstream (base64)>",
          ...
          rx_metadata: {
            0: {
              ...
              time: "<timestamp, ISO 8601 YYYY-MM-DDTHH:mm:ss.sssZ>"
              ...
            }
          },
          ...
          locations: {
            frm-payload: {
                    latitude: <coördinaat, float>,
                    longitude: <coördinaat, float>
                }
            }
          },
    ...
}
```

---

### InfluxDb

InfluxDb 2.0 is de database die gebruikt wordt. Het is een open-source Time Series Database (TSDB) geschreven in de GO programeertaal. Meer uitleg kan gevonden worden in het hoofdstuk Backend, onderdeel InfluxDb.

Het belangrijkste is dat deze zeer geschikt is om data gebonden aan tijd bij te houden. Ideaal dus om metingen van sensoren bij te houden. Verder heeft het ook een handig tagging systeem om het Sensor Identification System aan de data te koppelen.

Onderstaand zijn twee voorbeelden hoe data vanuit Node-RED naar de database kan gestuurd worden en hoe deze gestructureerd kunnen worden.

#### Output Node
```javascript
msg.payload = [
    [{
        intValue: '9i',
        numValue: 10,
        randomValue: Math.random()*10,
        strValue: "message1",
        time: new Date().getTime()-1
    },
    {
        tag1:"sensor1",
        tag2:"device2"
    }],
    [{
        intValue: '11i',
        numValue: 20,
        randomValue: Math.random()*10,
        strValue: "message2",
        time: new Date().getTime()
    },
    {
        tag1:"sensor1",
        tag2:"device2"
    }]
];
return msg;
```
[Bron: Node-RED node-red-contrib-influxdb nodes documentatie.](https://flows.nodered.org/node/node-red-contrib-influxdb)
_if msg.payload is an array of arrays, it will be written as a series of points containing fields and tags. For example, the following flow injects two points into an InfluxDb 2.0 database with timestamps specified._

#### Batch Output Node
```javascript
msg.payload = [
    {
        measurement: "weather_sensor",
        fields: {
            temp: 5.5,
            light: 678,
            humidity: 51
        },
        tags:{
            location:"garden"
        },
        timestamp: new Date()
    },
    {
        measurement: "alarm_sensor",
        fields: {
            proximity: 999,
            temp: 19.5
        },
        tags:{
            location:"home"
        },
        timestamp: new Date()
    }
];
return msg;
```
[Bron: Node-RED node-red-contrib-influxdb nodes documentatie.](https://flows.nodered.org/node/node-red-contrib-influxdb)
_The following example flow writes two points to two measurements, setting the timestamp to the current date._

---

### Gekozen data structuur
