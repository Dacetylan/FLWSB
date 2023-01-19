# Backend

## Mosquitto MQTT Broker

De Mosquitto MQTT Broker dient als tussenschakel om MQTT berichten te ontvangen van de applicatie voor de weerstations, en deze vervolgens in Node-RED te kunnen binnenhalen.

### Logging

#### Log file

sudo tail -f ~/baavend/baavend-mqtt/log/mosquitto.log

#### mqtt

http://www.steves-internet-guide.com/mosquitto-logging/

Topic: $SYS/#

```json
{ topic: "$SYS/broker/uptime", payload: "600413 seconds", qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/messages/received/1min", payload: 7.65, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/messages/sent/1min", payload: 67.28, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/publish/received/1min", payload: 0.36, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/publish/sent/1min", payload: 55.09, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/bytes/received/1min", payload: 217.38, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/bytes/sent/1min", payload: 2392.66, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/sockets/1min", payload: 0.97, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/connections/1min", payload: 0.97, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/messages/received/5min", payload: 6.32, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/messages/sent/5min", payload: 50.62, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/publish/received/5min", payload: 1.18, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/publish/sent/5min", payload: 40.92, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/bytes/received/5min", payload: 364.4, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/bytes/sent/5min", payload: 1916.23, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/sockets/5min", payload: 0.67, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/connections/5min", payload: 0.67, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/messages/received/15min", payload: 5.12, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/messages/sent/5min", payload: 28.87, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/publish/received/15min", payload: 1.6, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/publish/sent/15min", payload: 22.99, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/bytes/received/15min", payload: 425.04, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/load/bytes/sent/15min", payload: 1257.84, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/messages/stored", payload: 36, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/store/messages/count", payload: 36, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/store/messages/bytes", payload: 198, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/retained messages/count", payload: 36, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/messages/sent", payload: 32586, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/publish/messages/sent", payload: 22062, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/bytes/sent", payload: 1164648, qos: 0, retain: true, messageExpiryInterval: 60 … }

{ topic: "$SYS/broker/publish/bytes/sent", payload: 328754, qos: 0, retain: true, messageExpiryInterval: 60 … }
```

Met Join node:

```json
$SYS/broker/publish/bytes/sent : msg : Object
{
  topic: "$SYS/broker/publish/bytes/sent"
  payload:
    {
      $SYS/broker/version: "mosquitto version 2.0.15"
      $SYS/broker/uptime: "602690 seconds"
      $SYS/broker/load/messages/received/1min: 7.15
      $SYS/broker/load/messages/received/5min: 4.09
      $SYS/broker/load/messages/received/15min: 4.43
      $SYS/broker/load/messages/sent/1min: 58.37
      $SYS/broker/load/messages/sent/5min: 42.49
      $SYS/broker/load/messages/sent/15min: 42.13
      $SYS/broker/load/publish/received/5min: 0.59
      $SYS/broker/load/publish/received/15min: 1.66
      $SYS/broker/load/publish/sent/1min: 46.69
      $SYS/broker/load/publish/sent/5min: 33.21
      $SYS/broker/load/publish/sent/15min: 32.78
      $SYS/broker/load/bytes/received/1min: 127.76
      $SYS/broker/load/bytes/received/5min: 178.27
      $SYS/broker/load/bytes/received/15min: 410.42
      $SYS/broker/load/bytes/sent/1min: 1918.26
      $SYS/broker/load/bytes/sent/5min: 1303.33
      $SYS/broker/load/bytes/sent/15min: 1465.16
      $SYS/broker/messages/received: 13190
      $SYS/broker/messages/sent: 38107
      $SYS/broker/publish/messages/sent: 27500
      $SYS/broker/publish/bytes/sent: 373421
      $SYS/broker/bytes/received: 367918
      $SYS/broker/bytes/sent: 1453470
      $SYS/broker/load/sockets/1min: 0.91
      $SYS/broker/load/connections/1min: 0.91
      $SYS/broker/load/sockets/5min: 0.3
      $SYS/broker/load/connections/5min: 0.3
      $SYS/broker/load/sockets/15min: 0.21
      $SYS/broker/load/connections/15min: 0.21
      $SYS/broker/messages/stored: 31
      $SYS/broker/store/messages/count: 31
      $SYS/broker/store/messages/bytes: 189
      $SYS/broker/retained messages/count: 34
    }
  qos: 0
  retain: true
  _msgid: "1a7d49c96124290f"
  messageExpiryInterval: 60
}
```


## Troubleshooting

### Verbinden met de broker werkt niet.

Een probleem waar mogelijks op gestuit wordt is dat de config files niet geschreven zijn en er dus geen authenticatie mogelijk is.

Als docker nog nooit opgestart is kan het voldoende zijn om de map `baavend-mqtt` aan te maken met de [uid 1883](https://github.com/eclipse/mosquitto/issues/1031) toegekend. Hierdoor heeft de container het recht naar het volume op de host te schrijven. Dit kan je doen met volgende commandos:

```bash
mkdir ~/baavend/baavend-vis/
sudo chown -R 18832:1883 ~/baavend/baavend-vis/
```

Voor andere gevallen moeten de config files handmatig in het volume geschreven worden met `sudo`.

### Berichten komen niet aan.

Dit ge-troubleshoot worden met de software [MQTT Explorer](http://mqtt-explorer.com/).
Met deze tool kan je monitoren wat er gebeurt in de broker.

![MQTT Explorer](./assets/mqtt-explorer.png)

In het voorbeeld is te zien dat er data van het weerstation binnenkomt op topic **weatherStation**.
*Wij hadden eerst het topic in onze Node-Red gezet op **/weatherStation**, waardoor we natuurlijk niets ontvangde.*

Merk op dat er hier ook verschillende structuren van berichten toekomen op hetzelfde topic.
Er zijn namelijk twee varianten berichten die van het weerstation komen. Eén waar *temperature_C* en *humidity* in zitten, en een tweede waar deze ontbreken maar in de plaats *rain_mm* in zit.

Er kan ook altijd nog extra getest worden in Node-Red door zelf berichten op het topic te sturen en aan de hand van debug nodes (debug = groen).

![weather station flow in Node-Red](./assets/node-red-flow-weather-station.png)
