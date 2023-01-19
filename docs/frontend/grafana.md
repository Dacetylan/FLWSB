# Frontend

## Grafana

Grafan is gekozen in dit project als frontend web interface voor de visualisatie van de vergaarde data.
Deze heeft een hele hoop visualisatie mogelijkheden beschikbaar en het is ook mogelijk visualisaties toe te voegen in JavaScript.

Een extra voordeel is dat er ook Alerts kunnen worden ingesteld in Grafana op basis van inkomende data. Zo kan bijvoorbeeld via de MQTT logging van de Mosquitto MQTT broker een alert gegeven worden wanneer deze down is voor een bepaalde tijd.

---

### InfluxDb als Data Source

Het instellen van een Data Source kan jammer genoeg niet automatisch met Docker Compose.
Deze moet bij eerste opstart dus nog zelf ingesteld worden.

Bij de instellingen om dit te doen is het belangrijk Flux als Query-language/taal te selecteren.
Dit geeft de mogelijkheid om de authenticatie aan de hand van een Token, of API key van InfluxDb, te gebruiken in plaats van username en password.
Dit is eenvoudiger en veiliger in gebruik.

De URL van de InfluxDb container is: http://influxdb:8086

![Grafana Data Sources web interface pagina.](./assets/grafana-data-sources.png 'Figuur 1: Grafana Data Sources web interface pagina.')

![Grafana Data Sources web interface InfluxDb instellingen pagina.](./assets/grafana-data-sources-settings.png 'Figuur 2: Grafana Data Sources web interface InfluxDb instellingen pagina.')

[Officiële documentatie over InfluxDb als Data Source.](https://grafana.com/docs/grafana/latest/datasources/influxdb/)

---

### Provisioning

[Grafana Provisioning documentatie.](https://grafana.com/docs/grafana/latest/administration/provisioning/)

Provisioning in Grafana is een manier om instellingen te maken, van Data Sources tot Dashboards, met het gebruik van YAML files. De werking hiervan moet achter nog verder onderzocht worden en is dus nog geen gebruik van gemaakt in deze iteratie van het project.

#### Voorbeeld bij Data Sources

[Grafana Provisioning Data Sources documentatie.](https://grafana.com/docs/grafana/latest/administration/provisioning/#data-sources)

```yaml
apiVersion: 1

datasources:
  - name: InfluxDB_v2_Flux
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: ap
      defaultBucket: flwsb
      tlsSkipVerify: true
    secureJsonData:
      token: <Grafana token>
```

---

### Dashboards

De gemaakte Dashboards voor deze iteratie van het project zijn:

#### Climate Data

![Grafana dashboard: Climate Data (SAMDaaNo21)](./assets/grafana-climate-data.png 'Figuur 3:Grafana dashboard: Climate Data (SAMDaaNo21)')

#### Weather Station

![Grafana dashboard: Weather Station](./assets/grafana-weather-station.png 'Figuur 4:Grafana dashboard: Weather Station')

#### Panels

Het is zeer eenvoudig nieuwe panels toe te voegen.

![Grafana dashboard: add panel](./assets/grafana-add-panel.png 'Figuur 5: Grafana dashboard: add panel')

Aan de hand van de Data Explorer Query Builder in de InfluxDb web interface kunnen de juiste queries samengesteld worden.

![Grafana dashboard: edit panel](./assets/grafana-edit-panel.png 'Figuur 6: Grafana dashboard: edit panel')

Het moeilijkste komt in de vorm van de instellingen voor de grafieken. Deze zijn enorm uitgebreid. Zo kun je bijvoorbeeld de kleur laten veranderen afhankelijk van de waarde, zoals bij onderstaand Airtime panel. Deze gaat naar rood als de Airtime limiet overschreden wordt.

![Grafana dashboard: edit pane Airtimel](./assets/grafana-edit-panel-airtime.png 'Figuur 6: Grafana dashboard: edit panel Airtime')

In deze iteratie van het project zijn er enkel een aantal snelle weergaven aangemaakt om te illustreren wat Grafana kan, maar deze zijn niet geoptimaliseerd of zelfs geschikt voor de specifieke data.
Dit onderzoeken en toepassen is voor een volgende iteratie.
