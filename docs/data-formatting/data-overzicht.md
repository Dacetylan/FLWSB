# Data Formatting

## Data Overzicht

Dit onderdeel geeft een overzicht van alle data die moet worden bijgehouden. Zowel wat de data inhoud en hoe deze eruit ziet.
Dit voor het Sensor Identification System, de metingen, en extra  informatie uit The Things Network.

### Sensor Identification System

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
            board-id
        </td>
        <td>
            string
        </td>
        <td>
            Gekoppeld aan TTN applicatie device-id.
        </td>
        <td>
            board-1
        </td>
    </tr>
    <tr>
        <td>
            sensor-id
        </td>
        <td>
            byte
        </td>
        <td>
            ID voor specifieke sensor, hardcoded I2C-adres of connector.
        </td>
        <td>
            8
        </td>
    </tr>
    <tr>
        <td>
            sensor-name
        </td>
        <td>
            string
        </td>
        <td>
            Naam van de sensor, hardcoded I2C-adres of connector.
        </td>
        <td>
            BME280
        </td>
    </tr>
    <tr>
        <td>
            quantity
        </td>
        <td>
            string
        </td>
        <td>
            Grootheid van de meting. Hardcoded of handmatig ingevoerd via Node-RED dashboard formulier.
        </td>
        <td>
            temp
        </td>
    </tr>
    <tr>
        <td>
            datatype
        </td>
        <td>
            string
        </td>
        <td>
            Daatype waarin de meting moet worden opgeslagen in de database. Hardcoded of handmatig ingevoerd via Node-RED dashboard formulier.
        </td>
        <td>
            int
        </td>
    </tr>
    <tr>
        <td>
            unit
        </td>
        <td>
            string
        </td>
        <td>
            Eénheid van de meting. Hardcoded of handmatig ingevoerd via Node-RED dashboard formulier.
        </td>
        <td>
            °C
        </td>
    </tr>
</table>

---

### Klimatologische data

#### Gevraagde data voor AI
De studenten van de AI minor vragen volgende data:
 - Temperatuur
 - Luchtdruk
 - Luchtvochtigheid
 - Neerslag
 - Windsnelheid
 - Windrichting

#### Data van weerstation
Om een aantal zaken te meten zoals Windsnelheid en Windrichting wordt een bestaand weerstation gebruikt, namelijk de Bresser 5-in-1 New. Deze voert volgende metingen uit:
 - Temperatuur (Temperature)
 - Luchtvochtigheid (Humidity)
 - Gemiddelde windsnelheid (Wind Speed)
 - Rukwindsnelheid (Wind Gust)
 - Windrichting (Direction)
 - Neerslag (Rain)

Meer informatie over het seerstation in het hoofdstuk [Weather Station](../weather-station/reverse-engineering.md). 

#### Data van Expansion Boards
Er worden ook enkele Expansion Boards, of uitbreidingsborden, ontwikkeld voor het FLWSB ecosysteem.

 - TaMM-o-Meter (Anemometer):
    - Windsnelheid (wind tam-heid?) (gebasseerd op <a href="https://hackaday.io/project/185642-anemosens-sla-printed-anemometer">AnemoSens - SLA printed anemometer</a>)
 - TaMM-oisture (Analoge geleidingssensor):
    - Grondvochtigheid (gebasseerd op de Zanzibar Salinity sensor)



### Analyse metingen en data

<table style="width: 100%">
    <colgroup>
        <col span="0" style="width: 33%;">
        <col span="1" style="width: 33%;">
        <col span="2" style="width: 33%;">
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
            Temperatuur (Temperature)<br>
            <i>Bresser 5-in-1 New</i><br>
        </td>
        <td>
            <b>°C</b> = graden Celcius<br>
            <i>-40.0 tot 60.0</i>
        </td>
        <td>
            <b>float</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Luchtvochtigheid (Humidity)<br>
            <i>Bresser 5-in-1 New</i><br>
        </td>
        <td>
            <b>%</b> = percentage relatieve luchtvochtigheid<br>
            <i>1 tot 99</i>
        </td>
        <td>
            <b>int</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Gemiddelde Windsnelheid (Wind Speed)<br>
            <i>Bresser 5-in-1 New</i><br>
        </td>
        <td>
            <b>m/s</b> = meter per seconde<br>
            <i>0.0 tot 50.0</i>
        </td>
        <td>
            <b>float</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Rukwindsnelheid (Wind Gust)<br>
            <i>Bresser 5-in-1 New</i><br>
        </td>
        <td>
            <b>m/s</b> = meter per seconde<br>
            <i>0.0 tot 50.0</i>
        </td>
        <td>
            <b>float</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Windrichting (Direction)<br>
            <i>Bresser 5-in-1 New</i><br>
        </td>
        <td>
            <b>°</b> → hoek in graden<br>
            <i>16 of 360 (wind direction)</i>
        </td>
        <td>
            <b>int</b><br>
            <i>n/a</i>
        </td>
    </tr>
    <tr>
        <td>
            Neerslag (Rain)<br>
            <i>Bresser 5-in-1 New</i><br>
        </td>
        <td>
            <b>mm/10min.</b> = millimeter (= l/m²) om de 10 min. (basis meting, x144 voor een dag/etmaal)<br>
            <i>0.0 tot ?.0 (resolutie: 0,4 mm)<a href="https://nl.wikipedia.org/wiki/Lijst_van_weerrecords">weer records</a></i>
        </td>
        <td>
            <b>float</b><br>
            <i>n/a</i>
        </td>
    </tr>
</table>


---

## The Things Network (TTN)

Bij het werken via The Things Network (TTN) wordt buiten de metingen data nog een heel wat extra info verstuurd over MQTT.
Zo wordt de id en naam van in The Things Stack applicatie meegestuurd, als ook een timestamp/date wanneer de data is ontvangen.
Mits gekend wordt ook de locatie van het board meegestuurd.
Onderstaande tabel geeft hiervan een overzicht.
Nog extra informatie uit de Identity Server van TTN kan opgevraagd worden via hun API.

<table style="width: 100%">
    <colgroup>
        <col span="0" style="width: 15%;">
        <col span="1" style="width: 15%;">
        <col span="2" style="width: 30%;">
        <col span="3" style="width: 30%;">
    </colgroup>
    <tr>
        <th>Naam (Name)</th>
        <th>Datatype</th>
        <th>Bron (Source)</th>
        <th>Voorbeeld (Example)</th>
    </tr>
    <tr>
        <td>
            device-id
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
    </tr>
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
</table>

Meer info over de TTN API kan <a href="https://www.thethingsindustries.com/docs/reference/api/end_device/">hier</a> gevonden worden.

---
