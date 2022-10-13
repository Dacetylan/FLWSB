# Data formatting

## Introductie

Het **Flexible LoRaWAN Sensor Board (FLWSB)** is een project binnen ICT-Elektronica van de major Internet of Things op vraag van de minor Artificial Intelligence.
Eén van de hoofddoelen is een zo flexibel mogelijk modulair systeem bekomen. Hiervoor moet er rekening gehouden worden met dat er op elk afzonderlijk FLWS-board andere sensoren kunnen worden aangesloten. De metingen van deze sensoren moeten vervolgens draadloos verzonden worden aan de hand van LoRaWAN. Dit protocol verzend data geformatteerd in een bitstream. Hierbij moet er ook in acht genomen worden dat dit een batterij gevoede toepassing is. Elke extra bit die verzonden moet worden kost stroom en moet dus tot een minimum beperkt worden.
Om deze vraag te beantwoorden hebben we het **Sensor Identification System (SIS)** bedacht.

---

## Sensor Identification System (SIS)

### Principe

Om een modulair systeem te behouden en tegelijkertijd de hoeveelheid data die verzonden moet worden te beperken wordt er gewerkt met het Sensor Identification System (SIS). Dit koppelt een uniek sensor-id aan elke sensor die aangeeft over wat voor data het gaat en welke grote deze heeft. Zo hoeft het FLWSB-board enkel de data door te sturen waarover het daadwerkelijk beschikt. De backend weet vervolgens ook over wat voor data het gaat en kan deze correct verwerken en opslagen.

### Sensor-id

De sensor-id kan één of twee bytes zijn. Is de eerste bit een "1" dan bestaat het uit twee bytes. Is de eerste bit een "0" dan is er maar één byte gebruikt voor het sensor-id. Zo kan er eerst gewerkt worden met maar één byte, maar kan er ook voldoende uitgebreid worden indien nodig.

De in dit project ontwikkelde sensoren die met I²C werken worden reeds voorzien en kunnen automatisch herkend worden. Op de FLWSB-boards gebeurd dit aan de hand van hun I²C adres die voorgeprogrammeerd zijn. Voor andere I²C sensoren worden vrije sensor-id's voorzien om aan gekoppeld te worden.

De analoge sensoren, bijvoorbeeld via UART, worden herkend door op welke poort ze zijn aangesloten. Deze sensor-id's zijn dus gekoppeld aan de poort op het FLWSB-board en geven enkel deze poort aan. In de database moet voor een correcte werking aangegeven worden welke sensor op welke poort is aangesloten. Zo kan de backend uit de database opvragen over welke sensor het gaat.
Is dit niet aangegeven dan gaat de achterliggende data verloren. (**Oplossing voor?**)

Elke sensor-id geeft dus aan welke meting data er op volgt (grootheid en eenheid, bijvoorbeeld "temperatuur" in "°C"), het datatype en dus het aantal bytes, en eventuele omzetting die moet gebeuren bij het verwerken. Hierbij wordt rekening gehouden met sensoren die meerdere metingen uitvoeren, zoals bijvoorbeeld de Bosch Sensortec BME280. Eén enkel sensor-id kan dus gevolgd worden door data van meerdere metingen die door hun lengte in bytes onderscheid kunnen worden.


### Werking

#### 1. FLWSB-board

Het FLWSB-board detecteert de sensoren door de I²C adressen te lezen en te meten of er iets op de analoge poorten aanwezig is.
De metingen worden verzameld en de data wordt geformatteerd naar een bitstream.
Waarna de bitstream wordt verzonden over LoRaWAN.

#### 2. TTN applicatie

De uitgestuurde bitstream wordt ontvangen door een TTN gateway en verwerkt door hun servers.
Hierbij wordt de data beschikbaar gemaakt via MQTT.

*(Het is mogelijk data reeds te formateren in de TTN applicatie aan de hand van de TTN Formatter. Met het SIS is dit echter niet mogelijk omdat het data vereist vanuit de database.)*

#### 3. BaaVend (backend met Node-RED en MongoDb)

In Node-RED is er een MQTT node aanwezig die gesubscribeerd is op het topic van het FLWSB-board.
Van zodra de data door de TTN applicatie verwerkt is wordt deze beschikbaar en ontvangen als JSON in Node-RED.

Aan de hand van de FLWSB-board naam wordt de nodige SIS data opgevraagd uit de database.
De dataverwerking van de bitstream gebeurt in volgende herhalende stappen tot het einde van de data bereikt wordt:
 - Het sensor-id wordt gelezen en opgezocht.
 - De hoeveelheid bytes van de achterliggende data wordt bepaald en geformatteerd naar het juiste datatype.
 - De geformatteerde meting wordt in een JSON object bewaard met onderstaande structuur:

 ```javascript
 {
   "0":[
     {"Quantity":"Temperature", "Value":15.0, "Unit":"°C", "Sensor":"BME280", "Sensor-id":1}
   ]
 }
 ```

Vervolgens worden nog extra info over het FLWSB-board toegevoegd aan de JSON structuur.
Eens volledig wordt de JSON weggeschreven naar de MongoDb database en als document toegevoegd aan de collection van dat FLWSB-board.


---

## Metingen

### Welke data wordt er gemeten

#### Gevraagde data voor AI
De studenten van de AI minor vragen volgende data:
 - (Temperatuur)
 - Luchtdruk
 - Luchtvochtigheid
 - Neerslag
 - Windsnelheid
 - Windrichting

#### Data van weerstation
Om een aantal zaken te meten zoals Windsnelheid en Windrichting wordt een bestaand weerstation gebruikt. Namelijk de Bresser ClimateConnect Tuya 7003600QT5000. Deze voert volgende metingen uit:
 - Temperatuur
 - Luchtdruk
 - Luchtvochtigheid
 - Windsnelheid
 - Windrichting
 - Lichtintensiteit
 - UV-niveau
 - Neerslag

#### Data van Expansion Boards
Er worden ook enkele Expansion Boards, of uitbreidingsborden, ontwikkeld voor het FLWSB eco systeem.

 - TaMM-o-Meter (Anemometer):
    - Windsnelheid (wind tam-heid?) (gebasseerd op <a href="https://hackaday.io/project/185642-anemosens-sla-printed-anemometer">AnemoSens - SLA printed anemometer</a>)
 - TaMM-oisture (Analoge geleidingssensor):
    - Grondvochtigheid (gebasseerd op de Zanzibar Salinity sensor)



### Analyse metingen en data

<table style="width: 100%">
    <colgroup>
        <col span="1" style="width: 25%;">
        <col span="2" style="width: 25%;">
        <col span="3" style="width: 50%;">
    </colgroup>
    <tr>
        <th>Grootheid (Quantity/Measurement)<br>& <i>Sensor</i></th>
        <th>Eénheid (Unit)<br>& <i>Bereik</i></th>
        <th>Datatype (Offset)<br> & <i>Aantal bits/bytes</i></th>
    </tr>
    <tr>
        <td>
            Temperatuur (Temperature)<br>
            <i>Bosch Sensortec BME280</i><br>
        </td>
        <td>
            <b>°C</b> = graden Celcius<br>
            <i>-40 tot 85</i>
        </td>
        <td>
            <b>byte</b> (+40)<br>
            <i>0 tot 125, max. 125 = 0111 1101 → 7 bits = 1 byte</i>
        </td>
    </tr>
    <tr>
        <td>
            Luchtdruk (Pressure)<br>
            <i>Bosch Sensortec BME280</i><br>
        </td>
        <td>
            <b>hPa</b> = hectopascal (= 1 mbar)<br>
            <i>300 tot 1100</i>
        </td>
        <td>
            <b>unsigned int / uint16_t</b><br>
            <i>max. 1100 = 0100 0100 1100 → 11 bits = 2 bytes</i>
    </tr>
    <tr>
        <td>
            Luchtvochtigheid (Humidity)<br>
            <i>Bosch Sensortec BME280</i><br>
        </td>
        <td>
            <b>%</b> = percentage relatieve luchtvochtigheid<br>
            <i>0 tot 100</i>
        </td>
        <td>
            <b>byte</b><br>
            <i>max. 100 = 0110 0100 → 7 bits = 1 byte</i>
        </td>
    </tr>
    <tr>
        <td>
            -
        </td>
        <td>
            -
        </td>
        <td>
            -
        </td>
    </tr>
    <tr>
        <td>
            <i>TaMM-o-Meter</i><br>
            Windsnelheid
        </td>
        <td>
            <b>m/s</b> = meter per seconde<br>
            <i>0.0 tot 32.7 (0 tot 12 Beaufort)</i>
        </td>
        <td>
            <b>unsigned int / uint16_t</b> (x10)<br>
            <i>00 tot 327 = 1 0100 0111 → 9 bits = 2 bytes</i>
        </td>
    </tr>
    <tr>
        <td>
            <i>TaMM-oisture</i><br>
            Grondvochtigheid
        </td>
        <td>
            ADC omzetting van analoge spanning<br>
            <i>0 tot 1023 (resolutie ADC)</i>
        </td>
        <td>
            <b>unsigned int / uint16_t</b><br>
            <i>max. 1023 = 0000 0011 1111 1111 → 10 bits = 2 bytes</i>
        </td>
    </tr>
    <tr>
        <td>
            -
        </td>
        <td>
            -
        </td>
        <td>
            -
        </td>
    </tr>
    <tr>
        <td>
            Buiten-Temperatuur (Out Temperature)<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>°C</b> = graden Celcius<br>
            <i>-40.0 tot 60.0</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Luchtdruk (Pressure)<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>mbar</b> = millibar = hPa<br>
            <i>540 tot 1100</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
    </tr>
    <tr>
        <td>
            Buiten-Luchtvochtigheid (Out Humidity)<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>%</b> = percentage relatieve luchtvochtigheid<br>
            <i>1 tot 99</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Windsnelheid<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>m/s</b> = meter per seconde<br>
            <i>0.0 tot 50.0</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Windrichting<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>°</b> → hoek in graden<br>
            <i>16 of 360 (wind direction)</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Lichtintensiteit (Light Intensity)<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>Klux</b> = kilo lux (1 lux = 1 lumen/m²)<br>
            <i>0.00 tot 200.00</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            UV-niveau (UV Index)<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>Index</b> (<a href="https://ozone.meteo.be/research-themes/uv/todays-uv-index-at-uccle">voorbeeld</a>)<br>
            <i>0.0 tot 16.0</i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Neerslag (Rain)<br>
            <i>Bresser ClimateConnect Tuya 7003600QT5000</i><br>
        </td>
        <td>
            <b>mm/10min.</b> = millimeter (= l/m²) om de 10 min. (basis meting, x144 voor een dag/etmaal)<br>
            <i>0.0 tot ?.0 (resolutie: 0,4 mm)<a href="https://nl.wikipedia.org/wiki/Lijst_van_weerrecords">weer records</a></i>
        </td>
        <td>
            <b>n/a</b><br>
            <i>n/a</i>
        </td>
    </tr>
</table>


---

## Extra Info

### The Things Network (TTN)

Bij het werken via The Things Network/Stack (TTN) wordt buiten de metingen data nog een heel wat extra info verstuurd over MQTT.
Zo wordt de id en naam van in The Things Stack applicatie meegestuurd, als ook een timestamp/date wanneer de data is ontvangen.
Mits gekend wordt ook de locatie van het board meegestuurd.
Onderstaande tabel geeft hiervan een overzicht.

<table style="width: 100%">
    <colgroup>
        <col span="1" style="width: 15%;">
        <col span="2" style="width: 15%;">
        <col span="3" style="width: 30%;">
        <col span="4" style="width: 30%;">
    </colgroup>
    <tr>
        <th>Naam (Name)</th>
        <th>Datatype</th>
        <th>Bron (Source)</th>
        <th>Voorbeeld (Example)</th>
    </tr>
    <tr>
        <td>
            id
        </td>
        <td>
            string
        </td>
        <td>
            Payload msg and API
        </td>
        <td>
            eui-0004a30b0020bb1b
        </td>
    <tr>
        <td>
            name
        </td>
        <td>
            string
        </td>
        <td>
            API
        </td>
        <td>
            Board 7
        </td>
    </tr>
    <tr>
        <td>
            date
        </td>
        <td>
            string ISO 8601
        </td>
        <td>
            Payload msg
        </td>
        <td>
            YYYY-MM-DDTHH:mm:ss.sssZ, 1996-10-13T08:35:32.000Z
        </td>
    </tr>
    <tr>
        <td>
            latitude
        </td>
        <td>
            float
        </td>
        <td>
            Payload msg (if triangulated) and API
        </td>
        <td>
            latitude: -6.220360548375914
        </td>
    </tr>
    <tr>
        <td>
            longitude
        </td>
        <td>
            float
        </td>
        <td>
            Payload msg (if triangulated) and API
        </td>
        <td>
            longitude: 39.21113847179748
        </td>
    </tr>
    </tr>
</table>

Meer info over de TTN API kan <a href="https://www.thethingsindustries.com/docs/reference/api/end_device/">hier</a> gevonden worden.

### Weerstation

...

---
