# Toekomstige Iteraties

## Mogelijk verbeteringen en uitbreidingen

In dit onderdeel wordt er bekeken wat er nog kan komen aan verbeteringen en uitbreidingen in volgende iteraties van het project.

### SAMDaaNo21

- Mounting holes / inkepingen - Nano Every stijl
- Impedantie antenne baan
- Geen LED aanwezig
- Fout op silkscreen
- Fout met verbinding LoRaWAN module (RX/TX)

### Arduino Core

- Instellingen via ‘Tools’ menu
- Releases te installeren via Board Manager

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
