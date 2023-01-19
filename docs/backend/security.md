# Backend

## Security

In dit onderdeel worden de beveiligingsmaatregelen op een rijtje gezet en beschreven van alle onderdelen waaruit de backend is opgebouwd.

Over het algemeen is alles beveiligd met een wachtwoord.
Het instellen van deze wachtworden gebeurt meestal op niveau van Docker Compose om zo geautomatiseerd mogelijk te kunnen zijn. Dit door bestanden in te lezen bij het opstarten met `docker compose up -d`.
De loggins, gebruikersnaam en wachtwoord, zijn uiteraard niet aanwezig in de bronbestanden in deze repository. De bestanden zijn wel aanwezig met `.default` achtervoegsel, maar zijn enkel templates. Hieronder een voorbeeld van `influxdb.env.default` waar de velden zijn aangegeven door `<te-vervangen>`. Deze `<>` moeten uiteraard niet blijven, maar dienen enkel om aan te geven waar er iets vervangen moet worden.

```
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=<username>
DOCKER_INFLUXDB_INIT_PASSWORD=<password>
DOCKER_INFLUXDB_INIT_ORG=<org-name>
DOCKER_INFLUXDB_INIT_BUCKET=<bucket-name>
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=<api-key>
```

 [TLS/SSL](https://www.digitalocean.com/community/tutorials/how-to-use-certbot-standalone-mode-to-retrieve-let-s-encrypt-ssl-certificates-on-ubuntu-1804) is ook een optie, maar buiten de scope van deze iteratie.

---

### Docker

Docker is opgebouwd om veilig te zijn. Meer info hieroer kan teruggevonden worden in [de officële Docker documentatie](https://docs.docker.com/engine/security/).

Meer info hoe Docker omgaat met user en group id's in Linux kan je vinden in het volgende artikel met onderwerp "[Understand how uid and gid work in Docker containers](https://www.elephdev.com/cDocker/294.html?ref=addtabs&lang=en)".

### Docker-Compose en GitHub

Om ervoor te zorgen dat wachtworden en andere gevoelige data niet op GitHub terecht komen worden volgende voorzorgen getroffen:

- Geen gevoelige gegevens in de docker-compose.yml file.
- Wachtwoorden worden gehashed waar mogelijk.
- Container initialisatie aan de hand van environment variables worden in een aparte .env file bijgehouden die geëxclude worden.
- .gintignore voor bestanden die wachtwoorden bevatten, de .env bestanden en de self-signed test certificaten.


Voorbeeld .env file in docker-compose.yaml:
```yaml
# Gebruik .env file
  env_file:
    - grafana.env

# In plaats van
  environment:
    - GF_SECURITY_ADMIN_USER=<username>
    - GF_PATHS_PROVISIONING=/var/grafana-docker/provisioning
    - GRAFANA_INFLUX_DB=<db-name>
    - GRAFANA_INFLUX_USER=<username>
    - GRAFANA_INFLUX_PASSWORD=<password>
```


Voorbeeld .gintignore:
```
# Docker security
*.env
mosquitto-password.txt
mosquitto-tls/
influxdb-ssl/
nodered-settings.js
```


### Node-RED

Node-RED beschikt over user authentication met een gehashed wachtwoord.
Deze wordt ingesteld in nodered-settings.js samen met TLS certificaten instellingen voor HTTPS.

[Securing Node-RED documentatie](https://nodered.org/docs/user-guide/runtime/securing-node-red).

##### nodered-settings.js.default:

```javascript
...

/*******************************************************************************
 * Security
 *  - adminAuth
 *  - https
 *  - httpsRefreshInterval
 *  - requireHttps
 *  - httpNodeAuth
 *  - httpStaticAuth
 ******************************************************************************/

    /** To password protect the Node-RED editor and admin API, the following
     * property can be used. See http://nodered.org/docs/security.html for details.
     */
    adminAuth: {
        type: "credentials",
        users: [{
            username: "<username>",
            password: "<hashed-password>",
            permissions: "*"
        }]
    },

    /** The following property can be used to enable HTTPS
     * This property can be either an object, containing both a (private) key
     * and a (public) certificate, or a function that returns such an object.
     * See http://nodejs.org/api/https.html#https_https_createserver_options_requestlistener
     * for details of its contents.
     */

    /** Option 1: static object */
    //https: {
    //  key: require("fs").readFileSync('privkey.pem'),
    //  cert: require("fs").readFileSync('cert.pem')
    //},

    /** Option 2: function that returns the HTTP configuration object */
    // https: function() {
    //     // This function should return the options object, or a Promise
    //     // that resolves to the options object
    //     return {
    //         key: require("fs").readFileSync('privkey.pem'),
    //         cert: require("fs").readFileSync('cert.pem')
    //     }
    // },

    /** If the `https` setting is a function, the following setting can be used
     * to set how often, in hours, the function will be called. That can be used
     * to refresh any certificates.
     */
    //httpsRefreshInterval : 12,

    /** The following property can be used to cause insecure HTTP connections to
     * be redirected to HTTPS.
     */
    //requireHttps: true,

    /** To password protect the node-defined HTTP endpoints (httpNodeRoot),
     * including node-red-dashboard, or the static content (httpStatic), the
     * following properties can be used.
     * The `pass` field is a bcrypt hash of the password.
     * See http://nodered.org/docs/security.html#generating-the-password-hash
     */
    //httpNodeAuth: {user:"user",pass:"$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6tl8sJogENOMcxWV9DN."},
    //httpStaticAuth: {user:"user",pass:"$2a$08$zZWtXTja0fB1pzD4sHCMyOCMYz2Z6dNbM6tl8sJogENOMcxWV9DN."},
...
```

---

### TTN

The Things Network maakt gebruik van gebruikersprofielen die aan een TTN applicatie gekoppeld kunnen worden.

![TTN FLWSB applicatie Collaborators web pagina.](./assets/ttn-collaborators.png 'Figuur : TTN FLWSB applicatie Collaborators web pagina.')

Dit is dus user authentication met een geheim wachtwoord.
Handmatig aan te maken op de [TTN website](https://id.thethingsnetwork.org/).

![TTN ID web pagina.](./assets/ttn-id.png 'Figuur : TTN ID web pagina.')

TLS certificaten voor HTTPS zijn ook mogelijk. Meer info via onderstaande links:
- [Integratie in Node-RED documentatie.](https://www.thethingsindustries.com/docs/integrations/node-red/receive/#configure-mqtt-in-node)
- [TTN Addresses documentatie.](https://www.thethingsindustries.com/docs/getting-started/ttn/addresses/#console)

---

### InfluxDb

InfluxDb maakt gebruik van user authentication met geheim wachtwoord.
Er kunnen meerdere users ingesteld worden, maar enkel de initiële admin gebruiker is in te stellen met environment variables in de docker-compose file.
Om deze environment variables niet in de docker-compose file zelf te hoeven zetten wordt er gebruik gemaakt van een `.env` file.

In de `.env` file kan ook TLS worden ingesteld (uncomment) om gebruik te maken van HTTPS.
Deze verwijzen naar een TLS certificaat en key.

##### influxdb.env.default:

```
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=<username>
DOCKER_INFLUXDB_INIT_PASSWORD=<password>
DOCKER_INFLUXDB_INIT_ORG=<org-name>
DOCKER_INFLUXDB_INIT_BUCKET=<bucket-name>
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=<api-key>

# Uncomment to use TLS for HTTPS + provide the files through docker-compose volumes
# INFLUXD_TLS_CERT=/etc/ssl/influxdb-selfsigned.crt
# INFLUXD_TLS_KEY=/etc/ssl/influxdb-selfsigned.key
```

Als authenticatie voor aandere services is er een API key, of Token, systeem.

![InfluxDb web interface: API tokens.](./assets/influxdb-api-tokens.png 'Figuur : InfluxDb web interface: API tokens.')

---

### Mosquitto

De Mosquitto Broker maakt gebruik van user authentication met een gehashed wachtwoord.
Deze wordt geconfigureerd bij opstart van de container aan de hand van een `.conf` bestand die verwijst naar een `password.txt` bestand dat een gehashed wachtwoord bevat.

Voor meer info: [Mosquitto Username and Password Authentication -Configuration and Testing](http://www.steves-internet-guide.com/mqtt-username-password-example/)

##### mosquitto.conf:

```
listener 1883
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log

## Authentication ##
# By default, Mosquitto >=2.0 allows only authenticated connections. Change to true to enable anonymous connections.
allow_anonymous false
password_file /mosquitto/config/password.txt
```

##### mosquitto-password.txt.default:

```
bavo:<hashed-password>
```

TLS certificaten voor HTTPS zijn ook mogelijk.

---

### Grafana

Grafana maakt gebruik van user authentication met geheim wachtwoord.
Net zoals InfluxDb kan een initiële admin gebruiker ingesteld worden aan de hand van environment variables, en dus een `.env` bestand.

##### grafana.env.default:

```
GF_SECURITY_ADMIN_USER=<username>
GF_SECURITY_ADMIN_PASSWORD=<password>
GF_PATHS_PROVISIONING=/var/grafana-docker/provisioning
GRAFANA_INFLUX_DB=<bucket-name>
GRAFANA_INFLUX_USER=<username>
GRAFANA_INFLUX_PASSWORD=<password>
```

Is er geen admin via environment variables ingesteld ken bij het voor eerst ingelogd worden met de default admin user, wachtwoord: admin.
Vervolgens kan een nieuw wachtwoord opgegeven worden en kan de username admin aangepast worden in de instellingen.
