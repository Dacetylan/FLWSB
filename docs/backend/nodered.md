## Node-RED

[TTN MQTT documentatie](https://www.thethingsindustries.com/docs/integrations/mqtt/)

## Docker op Linux Virtual Machine

Bij het opstarten van de Node-RED container op een Linux Virtual Machine kan je stuiten op volgende error:

```bash
baavend-red  | <date time> - [error] Failed to start server:
baavend-red  | <date time> - [error] Error: EACCES: permission denied, mkdir '/data/node_modules'
```

Dit gebeurt omdat er volumes gemount worden en de user van de Docker container geen rechten heeft om in de directories van de host user te schrijven.
Voor Node-RED is de container user uid 1000. Om deze error op te lossen moet er dus schrijf rechten gegeven worden aan deze uid, zoals beschreven in [deze oplossing op stackoverflow](https://stackoverflow.com/questions/74487200/can-i-run-node-red-under-docker-on-vm-eflow-azure-iot-edge-on-windows-device/74488060#74488060).
Voor baavend-red wordt dit commando:

```bash

```
