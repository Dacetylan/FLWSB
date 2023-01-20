# Weerstation

## Reverse Engineering Onderzoek

### Introductie

Om snel aan bruikbare data te geraken maken we gebruik van een bestaand draadloos weerstation.
Dit is de [Alecto WS-4800](https://alectohome.nl/products/alecto-ws-4800-professioneel-weerstation-met-draadloze-buitensensor-wit) wat eigenlijk een Nederlandse rebranding is van de [Bresser 5-in-1 New](https://www.bresser.de/nl/bresser-bresser-3/Weercenters/BRESSER-Weather-Center-5-in-1-wit.html).
Deze werkt aan de hand van 868MHz waarmee de data van de buitensensoren naar de scherm module worden gestuurd.
Deze zending kan onderschept worden en zo kan de data naar de backend gestuurd worden waar de data wordt bijgehouden in een database.

![Weerstation Alecto WS-4800](./assets/weerstation-alecto-WS-4800.png ':size=300') ![Weerstation Bresser 5-in-1](./assets/weerstation-bresser-5in1.jpg ':size=300')

*fig. 1, Alecto WS-4800 weerstation*; *fig. 2, Bresser 5-in-1 (New) weerstation*

### Op voorhand:

- In het hoofdstuk Data Formatting onder [Data Overzicht](./data-formatting/data-overzicht.md) staat er in detail beschreven welke data er wordt verzameld door het weerstation.

- Er is een [bestaand project](https://www.skyon.be/maak-je-weerstation-geconnecteerd-en-slim/) met hetzelfde weerstation. Dit wordt gebruikt als referentie.

### Hands on:

#### Weerstation opbouwen en uittesten

We krijgen data binnen van het weerstation op de GUI dat meekwam met het weerstation.

#### [Dit project](https://www.skyon.be/maak-je-weerstation-geconnecteerd-en-slim/) volgen stap voor stap

We hebben het commando hieronder uitgevoerd. We hebben de parameters ingevuld met onze eigen mqtt server.

```
/usr/local/bin/rtl_433 -R 119 -f 868M -s 1024k -F mqtt://<mqtt_server_ip> 1883 retain 0 devices rtl_433[/id]
```

rtl_433 is een open-source project op GitHub dat het demoduleren en decoderen van radiosignalen van een groot bereik van weerstations mogelijk maakt. Toen wij het commando hierboven uitvoerde was er geen zichtbare data binnen gekomen op onze MQTT server. Wij hebben ook een aantal varianten geprobeerd.

1. Misschien werkt MQTT niet
   
   We hebben MQTT getest door testdata door te sturen, dit werkt. We hebben ook het commando uitgevoerd met de terminal als output in plaats van MQTT. **Nog steeds geen data**.

2. Misschien is de sample rate verkeerd
   
   We hebben het commando uitgevoerd met verschillende sample rates. **Nog steeds geen data**.

3. Misschien is de frequentie verkeerd
   
   We hebben het commando uitgevoerd met verschillende frequenties rond 868MHz. **Nog steeds geen data**.

4. Mischien gebruiken we een verkeerd algoritme
   
   We hebben naar de lijst van algoritmes gekeken op de GitHub van rtl_433. Met CTRL+F hebben we gezocht naar "Bresser"
   
   1. [52]  Bresser Thermo-/Hygro-Sensor 3CH
   
   2. [119]  Bresser Weather Center 5-in-1
   
   3. [172]  Bresser Weather Center 6-in-1, [...]
   
   4. [173]  Bresser Weather Center 7-in-1

Zoals eerder besproken is onze weerstation een variant op de Bresser Weather Center 5-in-1. Tussen de lijst van algoritmes staat er maar 1 die overeenkomt met de 5-in-1. Het algoritme dat we gebruiken in het commando hierboven klopt dus. **Nog steeds geen data**.

Later zullen we nog ontdekken waarom dat we geen data ontvangen.

#### Met een HackRF proberen onderscheppen

Met behulpt van GQRX is ontdekt dat het weerstation werkt op 868.3MHz met FM modulatie. Dit is te zien aan de twee pieken in *fig 3*. Dit is niet onlogisch. 863MHz tot 870MHz is binnen Europa vrij te gebruiken, daarom dat veel consumer technology gebruik maakt van deze frequenties. 

Eens er geweten is wat de centerfrequentie is kan het signaal vervolgens gedemoduleerd worden. Om het signaal succesvol te demoduleren is er eerst gekeken naar bestaande projecten. [Dit](https://github.com/andreafabrizi/BresserWeatherCenter) project van andreafabrizi is daar een voorbeeld van. 

Tijdens het volgen van dat project werden er een aantal opmerkelijkheden ontdekt:

1. In dat project staat dat er AM modulatie gebruikt wordt.

2. Wij hebben geobserveerd dat er FM modulatie aanwezig is.

3. In een [tweede project](https://github.com/merbanan/rtl_433/blob/master/src/devices/bresser_5in1.c) dat gebruik maakt van andreafabrizi's project wordt vermeld dat het weerstation gebuik maakt van "FSK-PCM" modulatie.

Wij hebben dus nu twee bronnen die iets compleet verschillend zeggen plus onze eigen observatie van FM modulatie op het signaal. Opmerkelijk.

Voor de volgende stap is er besloten om dit FM signaal te proberen demoduleren. Aangezien we een FM signaal observeren zullen we deze ook demoduleren als FM signaal. De projecten die eerder vermeld werden zullen wij gebruiken tijdens het decoderen van het signaal, aangezien dat dit is waar de focus op ligt bij die projecten.

![GQRX spectrum analyse](./assets/GQRX-spectrum-analyse.png)

*fig. 3, GQRX spectrum analyse*

![WFM gedemoduleerd signaal](./assets/WFM-gedemoduleerd-signaal.png)

*fig 4, WFM gedemoduleerd signaal*

In *fig 3* is te zien hoe dat een spectrum analyse eruit ziet. Het is heel duidelijk dat er twee pieken zijn rond de centerfrequentie (868.3MHz). Binnen GQRX is een functie om een FM signaal te demoduleren. Door dit toe te passen hebben wij ontdekt dat het geen FM signaal is maar een WFM signaal. Na de demodulatie door gebruik te maken van GQRX is het signaal zichtbaar op *fig 4*.

Merk op: in het project van andreafabrizi staat een heel gelijkaardige foto. Het signaal dat daar gedemoduleerd is ziet er heel gelijkaardig uit. Een preamble met dan de data die erna komt. Dit is goed nieuws en betekent dat we mogelijks toch gebruik kunnen maken van de twee projecten op GitHub.

Voor dat we dit signaal kunnen decoderen moeten we het wel kunnen demoduleren met GNURadio  Companion. De reden hiervoor is dat GRC een python file genereerd dat op eender welk systeem uitgevoerd kan worden. Dit is natuurlijk handiger om op te schalen dan een grafisch programma.

Dit bleek veel moeilijker dan verwacht. We hebben besloten om eens te kijken wat er binnenin het weerstation gebeurt om ook een  plan B te onderzoeken.

#### Weerstation open maken

We hebben het weerstation open gemaakt om zo toch al een alternatief te onderzoeken voor als de data niet makkelijk onderschept kan worden met een SDR.

![Overzicht weerstation onderdelen](./assets/weerstation-overzicht-kleuren.png)

*fig 5, Overzicht weerstation onderdelen*

Op de bovenstaande foto heb ik een aantal onderdelen een kleur gegeven.

- **Rood**: Dit onderdeeel meet de hoeveelheid regen dat gevallen is

- **Blauw**: In dit onderdeel zitten de PCB's die verantwoordelijk zijn voor het bewerken en versturen van de data vanuit de sensoren

- **Groen**: Dit onderdeel is verantwoordelijk voor de metingen rond vochtigheid en temperatuur

- **Paars**: Dit is een anemometer. Hier wordt de windsnelheid en richting gemeten.

![Weerstation binnenkant](./assets/weerstation-binnenkant.png)

*fig 6, Weerstation binnenkant*

![Regenmeter foto 1](./assets/weerstation-regenmeter-1.png)

*fig 7, Regenmeter binnenkant foto 1*

![Regenmeter foto 2](./assets/weerstation-regenmeter-2.png)

*fig 8, Regenmeter binnenkant foto 2*

##### Regenmeter

De regenmeter werkt met een simpel principe. Als het lepeltje opgevuld is dan kantelt het en valt al het water eruit. Door deze kantelbeweging kan een magnetische sensor een magneet detecteren en dus detecteren dat er een bepaalde hoeveelheid regen gevallen is (deze hoeveelheid is de inhoud van het lepeltje)

##### PCB

![PCB van weerstation](./assets/weerstation-pcb.png)

*fig 9, PCB van weerstation*

Op de PCB van het weerstation is niet veel te zien. Het is duidelijk waar de antenne is en waar de data van de sensoren binnekomt. Het is niet duidelijk welke microcontroller er gebruikt wordt omdat deze gecoat zijn met een zwarte beschermende laag.

##### Anemometer

![Windrichting binnenkant foto 1](./assets/weerstation-windrichting-1.png)

*fig 10, Windrichting binnenkant foto 1*

![Windrichting binnenkant foto 2](./assets/weerstation-windrichting-2.png)

*fig 11, Windrichting binnenkant foto 2*

De windrichting wordt op een interessante manier gelezen. Er is een cirkelvormige array van IR receivers. Deze passen in een vorm waar een gat in zit. Afhankelijk van de positie van deze vorm zullen er enkel 1 of 2 IR receivers tegelijk werken. Daaruit kan je afleiden in welke orientatie dat de wind zit.

![Anemometer](./assets/weerstation-anemometer.png)

*fig 12, Anemometer*

Dit is een soort van magnetische sensor dat gebruikt wordt om de de windsnelheid te meten. Het werkt gelijkaardig aan de werking van een speedometer op een fiets.

@reboot rtl_433 -f 868.3MHz -R 172 -F "mqtt://167.71.75.179:1883, user=bavo, pass=s120267, retain=0,events=weatherStation" -M time:unix:utc:tz:iso:usec -F kv

#### RTL_433

Om te onderzoeken hoe dat de gedemoduleerde data gedecodeert kon worden werden de C-files op de GitHub van RTL_433 geraadpleegd. RTL_433 is zoals eerder vermeld een open-source project op GitHub dat zich bezig houdt met het demoduleren en decoderen van radiosignalen op de ISM band. Onder andere ook weerstations zoals die van ons.

Er werd gebruik gemaakt van de zoekfunctie op GitHub om alle files te doorzoeken naar zoektermen. Zo werd er gezocht op "5-in-1" om alle files te vinden die zich bezig houden met het decoderen, demoduleren, en documenteren van de Bresser 5-in-1.

Toen werd er ontdekt dat in de C-file die zich bezig houdt met de Bresser 6-in-1 het volgende staat:

```md
Decoder for Bresser Weather Center 6-in-1.
- also Bresser Weather Center 7-in-1 indoor sensor.
- also Bresser new 5-in-1 sensors.
- also Froggit WH6000 sensors.
- also rebranded as Ventus C8488A (W835)
- also Bresser 3-in-1 Professional Wind Gauge / Anemometer, PN 7002531
- also Bresser soil temperature and moisture meter, PN 7009972
- also Bresser Thermo-/Hygro-Sensor 7 Channel 868 MHz, PN 7009999

```

Het algoritme voor de Bresser 6-in-1 werkt ook met de nieuwe Bresser 5-in-1. Opmerkelijk.

Dit werd uiteraard meteen getest. **Nu ontvangen we data van het weerstation**. De volgende stap is om deze data ook inneens binnen te halen op de backend via MQTT. Daarvoor moet wel de data een timestamp krijgen om te werken met influxDB. Dan moet er nog voor gezorgd worden dat dit commando altijd runt, ook bij startup van de raspberry pi. Met deze aanpassing ziet het commando er alst volgt uit.

`rtl_433 -f 868.3MHz -R 172 -F "mqtt://167.71.75.179:1883, user=bavo, pass=s120267, retain=0,events=weatherStation" -M time:unix:utc:tz:iso:usec -F kv`

Dit commando wordt dan in een crontab gezet met de `@reboot` functie zodat deze opstart samen met de raspberry pi.
