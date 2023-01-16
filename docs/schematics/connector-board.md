# Connector board

Het connector board dient als verbindingspunt voor de SAMDaaNo21. Het is de tussenschakel om allerlei onderdelen te kunnen verbinden met de SAMD21 microcontroller. De focus ligt hier ook op fast prototyping en flexibiliteit. Dit wilt zeggen dat er enkel connectoren voorzien worden en geen sensoren rechtstreeks op dit bord zullen komen.

## Schema

![FLWSB Connector Board schema v1.1](./assets/FLWSB-connector-board-schema-v1.1.svg)

## Veresiten

#### Te connecteren onderdelen

- SAMDaaNo21 moederbord
- Zonne-energie (Solar Power) manager voor continu gebruik tussen batterij en zonnenpaneel.
- Sensoren:
  - [CCS811](https://www.sciosense.com/products/environmental-sensors/ccs811/): TVOC sensor met I2C op 1V8-3V3
  - [SDS011](https://www.tinytronics.nl/shop/nl/sensoren/lucht/stof/nova-sds011-hoge-precisie-laser-stofsensor): fijnstof sensor met UART 3V3 op 5V
  -  [BME280](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/): temperatuur, barometer en luchtvochtigheid sensor met I2C op 1V8-3V3
  - ([DHT22](https://www.tinytronics.nl/shop/nl/sensoren/lucht/vochtigheid/dht22-thermometer-temperatuur-en-vochtigheids-sensor): temperatuur en luchtvochtigheid sensor alternatief met Digitale I/O op 3V3-6V)

#### Uitbreidingsmogelijkheden

- 2x Extra I2C 3V3 met 3V3 voeding
- 1x Extra I2C met 5V voeding
- 1x Extra UART 3V3 met 3V3 voeding
- Mogelijke sensoren:
  - [SCD41](https://sensirion.com/products/catalog/SCD41/): CO2 met I2C op 3V3-5V
  - [SGP41](https://sensirion.com/products/catalog/SGP41/): TVOC en NOx met I2C op 1V8-3V3
  - [SPS30](https://sensirion.com/products/catalog/SPS30/): HVAC PM1.0, PM2.5, PM4 en PM10 met I2C en UART op 5V
  - [GY-NEO6MV2](https://www.tinytronics.nl/shop/nl/communicatie-en-signalen/draadloos/gps/modules/gy-neo6mv2-gps-module): GPS met UART 3V3 op 3V3-5V

## Blokdiagram

<iframe width="600" height="600" src="https://miro.com/app/embed/uXjVPAdIy0o=/?pres=1&frameId=3458764539645645619&embedId=776892473756" frameborder="0" scrolling="no" allowfullscreen></iframe>

![FLWSB Connector Board blokdiagram v1.0](./assets/connector-board-blockdiagram-v1.0.jpg)

*Note: in het ontwerp moet rekening gehouden worden met mechanische sterkte. De SAMDaaNo21 wordt gevoed via USB kabel. Deze kan echter loskomen. Dit moet voorkomen worden door het design.*

## Sensoren

Sensor analyse uit [AirQualitySensor documentatie](https://ap-it-gh.github.io/ssys21-docs-luchtsensor/#/./pagina/Hardware/PCB) (DHT22 toegevoegd):
<table>
    <tbody><tr>
        <th>Naam</th>
        <th width="40%">Eigenschappen</th>
        <th width="30%">Argumentatie</th>
        <th>Links</th>
    </tr>
    <tr>
        <td>CCS811</td>
        <td>
            <ul>
                <li><b>Temperatuur, eCO en eTVOC<sup>2</sup></b></li>
                <li>V<sub>cc</sub> = 1.8V-3.3V</li>
                <li>I<sub>max</sub> = 54mA</li>
                <li><a target="_blank" href="https://en.wikipedia.org/wiki/I%C2%B2C">I²C</a> protocol 3.3V</li>
                <li>Meetbereik temperatuur: -40°C ~ +85°C</li>
                <li>Meetbereik luchtvochtigheid: 10% ~ 95% </li>
                <li>Meetbereik eCO²: 400ppm<sup>1</sup> ~ 32768ppm</li>
                <li>Meetbereik eTVOC: 0ppb<sup>5</sup> ~ 29206ppb</li>
                <li>Leessnelheid: 100kHz (0.01ms)</li>
            </ul>
        </td>
        <td>Een minder bekende sensor maar zeker wel bekend in IoT toepassingen. Het kan temperatuur, eCO² en eTVOC meten. Het heeft geen opwarm tijd dus is direct bruikbaar en is ook een SMD component wat zeker een voordeel is om het zo compact mogelijk te maken.</td>
        <td>
            <a target="_blank" href="https://www.tinytronics.nl/shop/nl/sensoren/ccs811-luchtkwaliteit-sensor">Winkel</a><br>
            <a target="_blank" href="https://www.sciosense.com/wp-content/uploads/documents/SC-001232-DS-2-CCS811B-Datasheet-Revision-2.pdf">Datasheet</a><br>
            <a target="_blank" href="https://github.com/adafruit/Adafruit_CCS811">Bibliotheek</a>
        </td>
    </tr>
    <tr>
        <td>SDS011</td>
        <td>
            <ul>
                <li><b>Fijnstof</b></li>
                <li>V<sub>cc</sub> = 5V</li>
                <li>I<sub>rated</sub> = 70mA ±10mA</li>
                <li><a target="_blank" href="https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter">UART</a> protocol 3.3V</li>
                <li>Baudrate: 9600</li>
                <li>Meetbereik PM2.5<sup>3</sup> &amp; PM10<sup>4</sup>: 0μg/m3 ~ 999.9 μg/m3</li>
                <li>Meetbereik luchtvochtigheid: 10% ~ 95% </li>
                <li>Leessnelheid: 1Hz (1s)</li>
            </ul>
        </td>
        <td>De SDS011 is een veel gebruikte fijnstof sensor voor DIY-projecten. Het zal niet de nauwkeurigste zijn, maar het geeft toch al een sterke indicatie van wat het fijnstof gehalte is in de lucht. Daarnaast het een goedkope modele.<br><br>
        Het werkt met een ventilator die de lucht binnentrekt. Het zal dus eerst moeten opgezet wordne om de huidige lucht erin te trekken vooraleer we kunnen meten.</td>
        <td>
            <a target="_blank" href="https://www.tinytronics.nl/shop/nl/sensoren/nova-sds011-hoge-precisie-laser-stofsensor">Winkel</a><br>
            <a target="_blank" href="https://cdn-reichelt.de/documents/datenblatt/X200/SDS011-DATASHEET.pdf">Datasheet</a><br>
            <a target="_blank" href="https://www.arduinolibraries.info/libraries/sds011-sensor-library">Bibliotheek</a>
        </td>
    </tr>
    <tr>
        <td>BME280</td>
        <td>
            <ul>
                <li><b>Temperatuur, Barometer &amp; Luchtvochtigheid</b></li>
                <li>V<sub>cc</sub> = 1.8 - 3.6V</li>
                <li>I<sub>max</sub> = 4.5mA</li>
                <li><a target="_blank" href="https://en.wikipedia.org/wiki/I%C2%B2C">I²C</a> protocol 3.3V</li>
                <li>Meetbereik temperatuur: -40°C ~ +85°C</li>
                <li>Meetbereik luchtvochtigheid: 0% ~ 100%</li>
                <li>Meetbereik luchtdruk: 300hPa ~ 1100hPa</li>
                <li>Leessnelheid: 1Hz (1s)</li>
            </ul>
        </td>
        <td>Deze digitale IC heeft een tal van metingen aanboord (temperatuur, luchtvochtigheid en druk). Het is ook een SMD component, dus makkelijk integreerbaar op een pcb.</td>
        <td>
            <a target="_blank" href="https://www.tinytronics.nl/shop/nl/sensoren/temperatuur-lucht-vochtigheid/bme280-digitale-barometer-druk-en-vochtigheid-sensor-module">Winkel</a><br>
            <a target="_blank" href="https://www.mouser.com/datasheet/2/783/BST-BME280_DS001-11-844833.pdf">Datasheet</a><br>
            <a target="_blank" href="https://github.com/adafruit/Adafruit_BME280_Library">Bibliotheek</a>
        </td>
    </tr>
    <tr>
        <td>DHT22</td>
        <td>
            <ul>
                <li><b>Temperatuur, Luchtvochtigheid</b></li>
                <li>V<sub>cc</sub> = 3.3-6V DC</li>
                <li>I<sub>max</sub> = ? mA</li>
                <li>Digital signal via single-bus (zie datasheet)</li>
                <li>Meetbereik temperatuur: -40°C ~ +80°C</li>
                <li>Meetbereik luchtvochtigheid: 0% - 100%</li>
                <li>Leessnelheid: 2Hz (~2s)</li>
            </ul>
        </td>
        <td>Een handige temperatuur én vochtigheid sensor.</td>
        <td>
            <a target="_blank" href="https://www.tinytronics.nl/shop/nl/sensoren/lucht/vochtigheid/dht22-thermometer-temperatuur-en-vochtigheids-sensor">Winkel</a><br>
            <a target="_blank" href="https://www.tinytronics.nl/shop/index.php?route=product/product/get_file&file=136/DHT22.pdf">Datasheet</a><br>
            <a target="_blank" href="">Bibliotheek</a>
        </td>
    </tr>
</tbody></table>

### Stroomverbruik

Stroomverbruik per onderdeel en maximum wanneer alles aan is.

| Component | Stroomverbruik in operatie | Start-up | Meet periode | Stroomverbruik standby |
| --- | --- | --- | --- | --- |
| ATSAMD21G18A | I = 1 - 6 mA | n/a | n/a | I<sub>25-85°</sub> = 2.70 - 55.2µA |
| LDL1117S33R | ? | n/a | n/a | I<sub>Q typ.</sub> = 250µA
| CCS811  | I<sub>DD</sub> = 30mA , I<sub>DD peak</sub> = 54mA | 18 - 20ms | ? | I<sub>DD</sub> = 19µA |
| SDS011  | I<sub>rated</sub> = 70mA ±10mA | ? | <10s + 1s read | I < 4mA |
| BME280  | I<sub>DD H/P/T (1V8)</sub> = 340 / 714 / 350µA , I<sub>weather monitoring mode</sub> = 0.16µA | 2ms | <1s | I<sub>DD SB (1V8-3V6)</sub> = 0.2 - 0.5µA |
| DHT22  | I<sub>measuring (3V3)</sub> = 1mA | 1s | >2s | I<sub>stand-by (3V3)</sub> = 40µA |

*I<sub>Q</sub> = [Quiescent current](https://forum.digikey.com/t/what-is-quiescent-current-and-why-is-it-important/3894)*

I<sub>max. totaal</sub> = 6mA + (250µA * 2) + 54mA + 80mA + 714µA + 1mA

__I<sub>max. totaal</sub> = 142.214 mA__

---

#### Notes from the CCS811 datasheet

> Modes of Operation
The CCS811 has 5 modes of operation as follows
- Mode 0: Idle, low current mode
- Mode 1: Constant power mode, IAQ measurement every
second / 1 seconds
- Mode 2: Pulse heating mode IAQ measurement every 10
seconds
- Mode 3: Low power pulse heating mode IAQ
measurement every 60 seconds
- Mode 4: Constant power mode, sensor measurement
every 250ms

> In Modes 1, 2, 3, the equivalent CO2 concentration (ppm) and
eTVOC concentration (ppb) are calculated for every sample.
- Mode 1 reacts fastest to gas presence, but has a higher
operating current
- Mode 3 reacts more slowly to gas presence but has the
lowest average operating current.

> When a sensor operating mode is changed to a new mode with a
lower sample rate (e.g. from Mode 1 to Mode 3), it should be
placed in Mode 0 (Idle) for at least 10 minutes before enabling
the new mode. When a sensor operating mode is changed to a
new mode with a higher sample rate (e.g. from Mode 3 to Mode
1), there is no requirement to wait before enabling the new
mode.

> Mode 4 is intended for systems where an external host system
wants to run an algorithm with raw data and this mode provides
new sample data every 250ms. Mode 4 is also recommended
for end-of-line production test to save test time. For additional
information please refer to application note ScioSense
AN000373: CCS811 Factory test procedure.

---
