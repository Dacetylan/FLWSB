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

#### 3. BaaVend (backend met Node-RED, MongoDb en InfluxDb)

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
