# Flexibiliteit

## Sensor Identification System (SIS)

### Principe

Om een modulair systeem te behouden en tegelijkertijd de hoeveelheid data die verzonden moet worden te beperken wordt er gewerkt met het Sensor Identification System (SIS). Dit koppelt een uniek sensor-id aan elke sensor die aangeeft over wat voor data het gaat en welke grote deze heeft. Zo hoeft het FLWSB-board enkel de data door te sturen waarover het daadwerkelijk beschikt. De backend weet vervolgens ook over wat voor data het gaat en kan deze correct verwerken en opslagen.

### Sensor-id

De sensor-id kan één of twee bytes zijn. Is de eerste bit een "1" dan bestaat het uit twee bytes. Is de eerste bit een "0" dan is er maar één byte gebruikt voor het sensor-id. Zo kan er eerst gewerkt worden met maar één byte, maar kan er ook voldoende uitgebreid worden indien nodig.

De in dit project ontwikkelde sensoren die met I²C werken worden reeds voorzien en kunnen automatisch herkend worden. Op de FLWSB-boards gebeurd dit aan de hand van hun I²C adres die voorgeprogrammeerd zijn. Voor andere I²C sensoren worden vrije sensor-id's voorzien om aan gekoppeld te worden.

De analoge sensoren, bijvoorbeeld via UART, worden herkend door op welke poort ze zijn aangesloten. Deze sensor-id's zijn dus gekoppeld aan de poort op het FLWSB-board en geven enkel deze poort aan. In de database moet voor een correcte werking aangegeven worden welke sensor op welke poort is aangesloten. Zo kan de backend uit de database opvragen over welke sensor het gaat.
Is dit niet aangegeven dan gaat de achterliggende data verloren.

Elke sensor-id geeft dus aan welke meting data er op volgt (grootheid en eenheid, bijvoorbeeld "temperatuur" in "°C"), het datatype en dus het aantal bytes, en eventuele omzetting die moet gebeuren bij het verwerken. Hierbij wordt rekening gehouden met sensoren die meerdere metingen uitvoeren, zoals bijvoorbeeld de Bosch Sensortec BME280. Eén enkel sensor-id kan dus gevolgd worden door data van meerdere metingen die door hun lengte in bytes onderscheid kunnen worden.


### Werking

#### 1. SIS Web Forms

Bij het deployen van de FLWSB-boards wordt het board ingegeven via het SIS Board Registration form.
Ook de hierop aangesloten sensoren worden gerigistreerd via het SIS Sensor Registration form.

![SIS Registration Web Forms.](./assets/node-red-dashboard-sis-forms.png 'Figuur 1: SIS Registration Web Forms.')

#### 2. FLWSB-board

Het FLWSB-board detecteert de sensoren door de I²C adressen te lezen en te meten of er iets op de analoge poorten aanwezig is.
De metingen worden verzameld en de data wordt, samen met de sensor-id's, geformatteerd naar een bitstream.
Waarna de bitstream wordt verzonden over LoRaWAN.

![FLWSB demo opstellig: overzicht, hoek.](./assets/flwsb-demo-overview-angle.jpg 'Figuur 2: FLWSB demo opstellig: overzicht, hoek..')

#### 3. TTN applicatie

De uitgestuurde bitstream wordt ontvangen door een TTN gateway en verwerkt door hun servers.
Hierbij wordt de data beschikbaar gemaakt via MQTT waarin de board-id, of eui, door de TTN applicatie wordt ingevoegd.

![TTN FLWSB applicatie overzicht.](./assets/ttn-flwsb-app-overview.png 'Figuur 3: TTN FLWSB applicatie overzicht.')

*Voor er iets ontvangen kan worden moet het FLWSB-board uiteraard eerst geregistreerd zijn, bij voorkeur door [Over-the-Air Activation (OTAA)](https://www.thethingsnetwork.org/docs/lorawan/addressing/#:~:text=Over%2Dthe%2DAir%20Activation%20(OTAA)%20is%20the%20preferred,are%20negotiated%20with%20the%20device.).*

*Het is mogelijk data reeds te formateren in de TTN applicatie aan de hand van de TTN Formatter. Met het SIS is dit echter niet mogelijk omdat het data vereist vanuit de database.*

![TTN FLWSB applicatie default payload formatter.](./assets/ttn-flwsb-app-payload-formatter.png 'Figuur 3: TTN FLWSB applicatie default payload formatter.')

#### 4. BaaVend (backend met Node-RED en InfluxDb)

In Node-RED is er een MQTT node aanwezig die gesubscribeerd is op het topic van het FLWSB-board, dit per node op de eui van in de TTN applicatie.
Van zodra de data door de TTN applicatie verwerkt is wordt deze beschikbaar en ontvangen als JSON in Node-RED.

Aan de hand van de FLWSB-board naam wordt de nodige SIS data opgevraagd uit de database.
De dataverwerking van de bitstream gebeurt in volgende herhalende stappen tot het einde van de data bereikt wordt:
 - Het sensor-id wordt gelezen en opgezocht.
 - De hoeveelheid bytes van de achterliggende data wordt bepaald en geformatteerd naar het juiste datatype.
 - De geformatteerde meting wordt in een JSON object gestructureerd volgens de bepaalde data structuur en de juiste tags worden toegekend (zie onderdeel [Data Structuur](./data-formatting/data-structuur.md)).

Eens volledig wordt het JSON object weggeschreven naar de database.

![Node-RED flow van TTN MQTT tot InfluxDb push.](./assets/node-red-flow-ttn-sis-flwsb.png 'Figuur 4: Node-RED flow van TTN MQTT tot InfluxDb push.')

---
