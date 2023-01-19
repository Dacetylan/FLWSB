# Toekomstige Iteraties

## Mogelijke verbeteringen en uitbreidingen

In dit onderdeel wordt er bekeken wat er nog kan komen aan verbeteringen en uitbreidingen in volgende iteraties van het project.

### SAMDaaNo21

- Momenteel zijn er geen mounting holes aanwezig, dat vonden we nog niet prioritair.
  - Mouning holes of inkepingen aan de randen van de printplaat zijn dus nog mogelijk en kunnen ook zeker van pas komen.
  - Een printplaat in de stijl van de Arduino Nano Every lijkt ons ook interessant. Dan zouden er geen componenten op de onderkant kunnen staan en zorgen we voor rat-bites aan de zijkant van de printplaat. Op deze manier kan de PCB gebruikt worden als SMD-component.
- De impedantie van het pad naar de antenne-aansluiting is niet theoretisch berekend. Dit is iets waar in een volgende versie over kan worden nagedacht.
- Er is geen LED aanwezig.
- Op het silkscreen staat een fout, `PA07` staat op het silkscreen als `PA09`. 
- Het schema bevat een fout die de LoRaWAN module onbruikbaar maakt. RX en TX van de UART-verbinding moeten omgewisseld worden.


### Arduino Core

- In het `Tools` menu van de Arduino IDE kunnen nog instellingen worden toegevoegd zoals kloksnelheid.
- Echte release maken zodat de boards via de Board Manager geïnstalleerd worden zoals bij de ESP32.

### Connector Board en Behuizing

- Behuizing ontwerpen of aankopen dat geschikt is voor deployment in Tanzania en Ghana met zonnepanelen. Reeds onderzocht in hoofdstuk Enclosure/Behuizing.
- Connector Board PCB ontwerpen samen met behuizing.
- Eigen implementatie van de Solar Power Manager in het Connector Board zelf.

### Weerstations

- Analyse naar de correctheid van de verkregen data uit de gebruikte applicatie.
- Onderzoek naar hoe deze data juist/beter visualiseren.

### Backend

- SIS niet volledig geïmplementeerd geraakt. De ttn-sis-flwsb flow in Node-RED is onvolledig. Deze werkt nog niet 100% en doet nog geen conversies.
- MQTT topic van TTN veresit een specifiek device. Hierdoor is er een flow per device nodig. In de eerste iteratie van het Zanzibar project is er voor dit probleem een script ontwikkeld. Deze kan ook hier toegepast worden, mits aanpassingen.
- TLS/SSL beveiliging implementeren voor gebruik van HTTPS.
- Data persistentie met Docker niet optimaal. Verder onderzoeken. Vooral bij heropstart Node-RED zijn de credentials niet meer leesbaar waardoor authenticatie instellingen opnieuw moeten worden ingegeven, en gedoe met flow bestanden.
- Automatische backup functionaliteit voor InfluxDb. Mogelijk met ingebouwd commando mits TLS werkt.
- Weerstations pushen nu op de zoveel seconden data in twee verschillende vormen. Dit zorgt voor onnodige belasting en mogelijks foutieve data. De MQTT msg's kunnen in Node-RED over een bepaalde tijdspanne verzameld worden, zodat na een bepaalde periode, vb elk half uur, een gemiddelde kan berekend worden en een volledige push kan gebeuren naar de database, zonder *undefined* waarden.

### Frontend

- Uitbreiden SIS web form met tooltips en voorbeelden.
- Validatie van ingevoerde data in het SIS web form.
- Grafana dashboards opbouwen geschikt voor de te visualiseren data, vb. windroos voor windrichting.
