 # Flexible LoRaWAN Sensor Board SAMDaaNo21



![SAMDaaNo21](assets/SAMDaaNo21-pinout.svg)

[PDF versie van de pinout diagram](./assets/SAMDaaNo21-pinout.pdf ':ignore')

Het FLWSB Main Board is een microcontroller bord gebaseerd op de ATSAM D21 in de vormfactor vergelijkbaar met een Arduino Nano. Het moet gemakkelijk zijn om dit bord in een breadboard te prikken en zo testen uit te voeren of schakelingen te bouwen. Het elektrisch schema is [hier](../schematic/main-board) te vinden.



## KiCad bibliotheken

Het is handig om een printplaat te kunnen ontwikkelen waar de SAMDaaNo21 opgeprikt kan worden.

Om dit proces te vergemakkelijken is er een KiCad bibliotheek ontwikkeld, die bevat een symbol, footprint en 3D-model.

Het is aangeraden om bibliotheken die niet standaard in KiCad zitten mee in de projectmap te steken en te importeren als projectbibliotheek. Als je je projectmap dan deelt met derden zullen zij meteen beschikken over alle nodige bibliotheken.

Tutorial: [How to import into KiCad V6 & later?](https://support.snapeda.com/en/articles/5995733-how-to-import-into-kicad-v6-later)

[SAMDaaNo21 bibliotheek bestanden](https://github.com/Dacetylan/FLWSB/tree/SAMDaaNo21/src/printed-circuit-boards/FLWSB-SAMDaaNo21-KiCad-lib)

![LWSB-SAMDaaNo21-v1-symbol](assets/FLWSB-SAMDaaNo21-v1-symbol.svg 'SAMDaaNo21 symbol')
![LWSB-SAMDaaNo21-v1-footprint](assets/FLWSB-SAMDaaNo21-v1-footprint.svg 'SAMDaaNo21 footprint')

## Testpunten

Er zijn verschillende testpunten toegevoegd om op een gemakkelijke en toegankelijke manier verschillende parameters op het bord te kunnen meten.

Er is gekozen voor through hole testpunten zodat het gemakkelijk is om deze met een probe te meten. Alle testpunten zijn te vinden nabij de USB poort.

| Testpunt nummer | Verbinding                                                   |
| --------------- | ------------------------------------------------------------ |
| TP1             | VBUS: 5 V afkomstig van USB                                  |
| TP2             | VDD: 3,3 V gereguleerde spaning                              |
| TP3             | VIN: Ingangsspanning voordat het naar de lineaire regelaar gaat |



## LoRaWAN Module

De RN2483 zit mee op de printplaat en bevindt zich aan het uiteinde. Er kan een antenne aangesloten worden via een U.FL connector.  

[Productpagina connector](https://be.farnell.com/hirose-hrs/u-fl-r-smt-1-10/rf-coaxial-u-fl-straight-jack/dp/1688077)

## USB Interface & VIN

Het bordje kan voorzien worden van stroom via de USB-C poort. Een LDO (Low Dropout regelaar) zal de spanning afkomstig van de computer reguleren naar een stabiele 3,3 V.

De LDO is een LD1117S33 en ondersteunt een minimale ingangsspanning van 4,3 V en een maximale van 15 V. Dat kan worden aangelegd via de VIN pin. Er is een Schottky diode voorzien om ervoor te zorgen dat de spanning van VIN niet op de USB poort komt te staan.

*Let op dat je met een lineaire regelaar te maken hebt. Hoe hoger de ingangsspanning, hoe warmer de LDO zal worden!*

Het is ook mogelijk om de regelaar over te slaan en rechtstreeks 3,3 V te leveren via de 3V3 pin. Dit kan handig zijn bij een situatie waarin we zo zuinig mogelijk willen zijn en een efficiëntere 3,3 V regelaar gebruiken van een andere pcb. *Belangrijk is dat deze spanning niet te hard mag afwijken van 3,3 V!*


## RESET & DEBUG

Als er nog geen bootloader op de ATSAMD staat of als we een bare metal installatie gebruiken zullen we gebruik moeten maken van de program en debug header. Dat zijn de 3 pinnen centraal op de printplaat voor de LoRaWAN module. De pinout van links naar recht is: RESET, SWDIO, SWCLK. 

De ATSAMD maakt gebruik van Serial Wire Debugging (SWD), dat maakt het mogelijk om via fuses in te stellen, binaries in te laden en zelfs break-points aan je code toe te voegen.

## Input / Output

Dit zijn alle GPIO, SERCOM en power aansluitingen die via pinheaders naar buiten worden gebracht. De SERCOM poorten zijn alvast gedefinieerd zodat onder andere de pull-up weerstanden geplaatst kunnen worden. Alle andere poorten zijn voor algemeen gebruik. In de datasheet van de ATSAM D21 onder 7. I/O Multiplexing and Considerations kunnen alle verschillende mogelijkheden van deze aansluitingen gevonden worden (AC, ADC, DAC, PTC, DAC, IO, ...). 

PA12 en PA13 zijn onderdeel van de I²C bus en hebben al een pull-up weerstand van 4,7 K voorzien. *Bij het plaatsen van nog externe pull-up weerstanden zullen zij in parallel staan en zal de weerstandswaarde te laag worden.*



## Toekomstige verbeteringen

- Momenteel zijn er geen mounting holes aanwezig, dat vonden we momenteel nog niet prioritair.
  - Mouning holes of inkepingen aan de randen van de printplaat zijn dus nog mogelijk.
- De impedantie van het pad naar de antenne aansluiting is niet theoretisch berekend. dit is iets waar in een volgende versie over kan worden nagedacht
- Er is geen LED aanwezig

### Bill of Materials

[Open BOM in nieuw tablad.](/printed-circuit-boards/assets/ibom.html ':ignore')

[poc board bill of materials](./assets/ibom.html ':include :type=iframe width=100% height=1024px')

