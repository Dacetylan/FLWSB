## Data Structuur

De data die ontvangen wordt via MQTT uit de TTN applicatie bevat de bitstream van het FLWSB-board, maar ook nog een hoop extra informatie:

__Voorbeeld MQTT msg van TTN__

De nuttige extra informatie, zoals timestamp en locatie worden eruit gefiltert en de bitstream wordt omgezet naar de juiste metingen.

...

InfluxDb [voorbeelden](https://flows.nodered.org/node/node-red-contrib-influxdb):

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
