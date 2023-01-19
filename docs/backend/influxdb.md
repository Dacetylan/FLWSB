# Backend

## InfluxDb Time-Series Database

Voor dit project is er gekozen om te werken met InfluxDb.
Dit is een time-series database, wat wilt zeggen dat aan alle datapunten een timestamp, of datum en tijdstip is gekoppeld. Dit maakt het uitermate geschikt om historische data te verzamelen en deze om te zetten in grafieken. Ideaal dus voor klimatologische data zoals in dit project.

De keuze voor deze database ligt ook bij onze keuze voor het gebruik van Grafana als frontend visualisatie van de verzamelde data. Grafana beschikt over een eenvoudige, en gratis, plug-in die de verbinding tussen de twee super simpel maakt om op te zetten.

Enkele specificaties:
- InfluxDb 2.0
- Open-source Time Series Database (TSDB)
- geschreven in GO programeertaal
- Flux query-taal

[Officiële documentatie website](https://www.influxdata.com/_resources/)

Voordelen:
- Zeer performant in queriën van zeer grote hoeveelheden data.
- Wanneer geschreven wordt naar de database werkt dit het beste in grote blokken data in één keer.
- Zeer eenvoudig data op te vragen door schema systeem (zie Schema Design onderaan) met tags.

---

### Werking

InfluxDb beschikt over een CLI, maar kan ook eenvoudig beheerd worden aan de hand een web interface.

#### Buckets

Buckets zijn eenvoudig te beheren.

![InfluxDb web interface: Buckets.](./assets/influxdb-buckets.png 'Figuur 1: InfluxDb web interface: Buckets.')

#### API Tokens

API tokens aanmaken, om connecties naar buiten op te zetten, met specifieke machtigingen kunnen ook zeer eenvoudig.

![InfluxDb web interface: API tokens.](./assets/influxdb-api-tokens.png 'Figuur 2: InfluxDb web interface: API tokens.')

#### Data Explorer

De web interface beschikt ook over een Data Explorer. Een zeer handige tool om query's op te stellen, als ook een snelle visualisatie van data.

![InfluxDb web interface: Data Explorer, Query Builder en graph view.](./assets/influxdb-data-explorer-query-builder-graph.png 'Figuur 3: InfluxDb web interface: Data Explorer, Query Builder en graph.')

![InfluxDb web interface: Data Explorer, Script Editor en raw data view.](./assets/influxdb-data-explorer-script-editor-raw-data.png 'Figuur 4: InfluxDb web interface: Data Explorer, Script Editor en raw data view.')

---

### Schema Design

De InfluxDb documentatie heeft een onderdeel over InfluxDb schema design onder [Write data - Best practices- Schema design](https://docs.influxdata.com/influxdb/v2.4/write-data/best-practices/schema-design/).

InfluxDb bestaat uit volgende onderdelen:

<table style="width: 100%">
    <colgroup>
        <col span="0" style="width: 15%;">
        <col span="1" style="width: 15%;">
        <col span="2" style="width: 50%;">
        <col span="3" style="width: 30%;">
    </colgroup>
    <tr>
        <th>Naam (Name)</th>
        <th>Datatype</th>
        <th>Beschrijving</th>
        <th>Voorbeeld (Example)</th>
    </tr>
    <tr>
        <td>
            bucket
        </td>
        <td>
            string
        </td>
        <td>
            Benoemde locatie waar time series data wordt opgeslagen. Vergelijkbaar met een collection in MongoDb of een relationele database op zichzelf. Het kan automatisch datapunten gaan verwijderen afhankelijk van hoe oud ze zijn. Dit is data persistence. <br>
            Vb. 6 maanden, of 2 jaar. Dit is de retention period. <br>
            <i>Bevat measurements.</i>
        </td>
        <td>
            flwsb <br>
            sis
        </td>
    </tr>
    <tr>
        <td>
            _measurement
        </td>
        <td>
            string
        </td>
        <td>
            Elke measurement is een simpele naam dat een schema en de data in de fields beschrijft.
            Vergelijkbaar met een document in MongoDb, of een tabel in een relationele database. <br>
            <i>Bevat fields, tags en timestamps.</i>
        </td>
        <td>
            airSensor
        </td>
    </tr>
    <tr>
        <td>
            _field
        </td>
        <td>
            string: string/double/int
        </td>
        <td>
            Field key-value pairs hebben een naam en bevatten numerische data. De key houd metadata bij en de value houd unieke of sterk variabele data bij verbonden aan een timestamp. <br>
            <i>Fields worden niet geïndexeerd, lees niet performant in queries.</i>
        </td>
        <td>
            temperature: 22.5
        </td>
    </tr>
    <tr>
        <td>
            tag
        </td>
        <td>
            string: string
        </td>
        <td>
            Tag key-value pairs voegen metadata toe die meerdere datapunten met elkaar linken. <br>
            <i>Tag keys en values worden geïndexeerd, lees performant in queries.</i>
        </td>
        <td>
            tags: { <br>
              location: "home", <br>
              sensor: "bme280" <br>
            }
        </td>
    </tr>
    <tr>
        <td>
            _time / timestamp
        </td>
        <td>
            Datetime:RFC3339
        </td>
        <td>
            Standaard de tijd wanneer het datapunt wordt toegevoegd, in nanoseconden. Kan worden meegegeven bij het wegschrijven en in miliseconden wanneer gespecificeerd.
        </td>
        <td>
            2022-10-28T16:43:56.175Z
        </td>
    </tr>
</table>



_**Keys** herhalen niet binnen een schema en kunnen geen gereserveerde keywords zijn of speciale tekens bevatten._

_**Measurements** en **keys** bevatten geen data; **tag values** en **field values** bevatten wel data._

_Een **datapunt / point** bevat een series key, een field value en een timestamp.
vb. ```2019-08-18T00:00:00Z census ants 30 portland mullen```. Waarbij measurement = census, field key = ants, field value = 30, location tag = portland, en scientist tag = mullen._

_Een **series key** is een collectie van datapunten dat een measurement, tag set en field key delen.
Een **series** bevat timestamps en field values voor een bepaalde series key._

[_Bron: InlfuxDb data elements_](https://docs.influxdata.com/influxdb/cloud/reference/key-concepts/data-elements/#bucket)

<br>
