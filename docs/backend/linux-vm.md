# Backend

## Linux Virtual Machine

Voor het draaien van Docker wordt er gebruik gemaakt van een Linux VM, of Virtual Machine.
Er is gekozen om de cloud service van Digital Ocean te gebruiken.
Digital Ocean noemt deze droplets en er is gekozen voor Ubuntu 22.04 (LTS) x64 als Linux versie met de standaard 25 GB aan SSD opslag ruimte.
DigitalOcean beschikt ook over een periodiek backup systeem, voor draaiende droplets. Als ook een snapshot systeem waarmee je images van de droplet/VM kan bij houden wanneer de droplet niet draaid. Dit aan een extra kost uiteraard. Deze zijn echter wel beperkt tot DigitalOcean en kunnen niet worden gedownload.
Als externe backup van dit project zijn de bestanden gebackupt als encrypteerde zip-file met daarin alle betsanden als ook een .tar.gz van al deze betsanden. Te vinden in `src/backend` van deze repository. (Bij het maken van de .tar.gz gaf het wel aan op het einde dat er errors waren, maar in de logs stonden geen errors. Dus deze bevat al dan niet errors.)
Voor meer informatie heeft [Digital Ocean uitstekende documentatie](https://docs.digitalocean.com/) beschikbaar. Voor zowel hun services als het opzetten van specifieke Ubuntu versies in een VM.

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=568af813537f&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

*[DigitalOcean droplet (baavend-ubuntu-s-1vcpu-1gb-intel-ams3-01)](https://cloud.digitalocean.com/droplets/328289429/graphs?i=8bcdff&period=hour) IP: 167.71.75.179 __(Niet meer actief vanaf 20-01-2023)__*

![DigitalOcean droplet logging graph na resize van 1GB RAM naar 2GB.](./assets/digitalocean-graph-resize.png 'Figuur 1: DigitalOcean droplet logging graph na resize van 1GB RAM naar 2GB.')

### Troubleshooting

Bij het opstarten van de __Node-RED__ en __Grafana__ containers op een Linux Virtual Machine kan je stuiten op permission errors.

Dit gebeurt omdat er volumes gemount worden en de user van de Docker container geen rechten heeft om in de directories van de host user te schrijven.

Om deze error op te lossen moet er dus schrijf rechten gegeven worden aan de uid van de specifieke container, zoals beschreven in [deze oplossing op stackoverflow](https://stackoverflow.com/questions/74487200/can-i-run-node-red-under-docker-on-vm-eflow-azure-iot-edge-on-windows-device/74488060#74488060).

#### Node-RED

Bij Node-RED is de error als volgt:

```bash
baavend-red  | <date time> - [error] Failed to start server:
baavend-red  | <date time> - [error] Error: EACCES: permission denied, mkdir '/data/node_modules'
```

Voor Node-RED is de container user uid 1000.
Voor baavend-red wordt het commando:

```bash
sudo chown -R 1000:1000 ~/baavend/baavend-red/
```

#### Grafana

Bij Grafana is de error als volgt:

```bash
baavend-vis  | GF_PATHS_DATA='/var/lib/grafana' is not writable.
baavend-vis  | You may have issues with file permissions, more information here: http://docs.grafana.org/installation/docker/#migrate-to-v51-or-later
baavend-vis  | mkdir: can't create directory '/var/lib/grafana/plugins': Permission denied
...
```

Zoals beschreven in [de link die gegeven wordt bij de error](http://docs.grafana.org/installation/docker/#migrate-to-v51-or-later) kan de uid van de container verschillend zijn afhankelijk van versie van Grafana die gebruikt wordt.

> User ID changes
In Grafana v5.1, we changed the ID and group of the Grafana user and in v7.3 we changed the group. Unfortunately this means that files created prior to v5.1 won’t have the correct permissions for later versions. We made this change so that it would be more likely that the Grafana users ID would be unique to Grafana. For example, on Ubuntu 16.04 104 is already in use by the syslog user.

| Version | User | User ID | Group | Group ID |
| --- | --- | --- | --- | --- |
| < 5.1 | grafana | 104	| grafana |	107 |
| >= 5.1 | grafana | 472 | grafana | 472 |
| >= 7.3 | grafana | 472 | root | 0 |

> There are two possible solutions to this problem. Either you start the new container as the root user and change ownership from 104 to 472, or you start the upgraded container as user 104.

Er zijn dus verschillende opties.
Volgende commando werkt voor baavend-vis:

```bash
sudo chown -R 104:104 ~/baavend/baavend-vis/
sudo chown -R 472:472 ~/baavend/baavend-vis/
```

### Mosquitto mqtt

Bij de Mosquitto container is het vermoedlijk hetzelfde probleem.
Hier is het probleem dat de config files niet geschreven zijn en er dus geen authenticatie mogelijk is.

Als docker nog nooit opgestart is geweest is het (vermoedelijk) voldoende om de map `baavend-mqtt` aan te maken met de [uid 1883](https://github.com/eclipse/mosquitto/issues/1031):

```bash
mkdir ~/baavend/baavend-mqtt/
sudo chown -R 1883:1883 ~/baavend/baavend-mqtt/
```

Als dat niet werkt moet de config files handmatig gekopiëerd worden met sudo.


---
