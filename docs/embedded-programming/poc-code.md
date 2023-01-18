# Embedded Programming

Het programmeren van de SAMDaaNo21 kan gelukkig heel gemakkelijk door gebruik te maken van de Arduino IDE.

## Voorbeeldcode

We hebben verschillende "[Example Sketches](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/tree/master/libraries/SAMDaaNo21/examples)" gemaakt die het duidelijk weergeven hoe je kan werken met de SAMDaaNo21 en hoe je de werking kan nagaan.

1. Stel de SAMDaaNo21 (Native USB Port) in als actief board. Via `Tools` -> `Board` -> `FLWSB ...` -> `SAMDaaNo21 (Native USB Port)`. 
2. Selecteer een van de voorbeelden via: `File` -> `Examples` -> `SAMDaaNo21` -> `...`.


### SAMDaaNo21 UART test

[Broncode](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/libraries/SAMDaaNo21/examples/SAMDaaNo21-UART-test/SAMDaaNo21-UART-test.ino)

Deze code kan gebruikt worden om alle toegankelijke UART-interfaces die de SAMDaaNo21 kan aanbieden te testen.

Iedere kwart seconde zal er naar een andere UART een bericht worden verzonden.

`SerialUSB` is een alias van `Serial`.

`SerialLoRa` is een alias van `Serial2`.

Je kan in principe kiezen welke je gebruikt of ze door elkaar gebruiken.


### SAMDaaNo21 Wire master writer

[Broncode](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/libraries/SAMDaaNo21/examples/SAMDaaNo21-master_writer/SAMDaaNo21-master_writer.ino)

Deze code kan gebruikt worden om de I2C verbinding van de SAMDaaNo21 te testen.

Sluit een oscilloscoop aan en zet het trigger type op I2C of gebruik een andere MCU om de berichten te ontvangen. 

De SerialUSB is in gebruik voor extra informatie over het verloop van de code.

Het signaal is aanwezig op de S4CDA en S4SCL pinnen. 
Een pull-up weerstand is aanwezig aan de onderkant van de printplaat.

### SAMDaaNo21 LoRa Module Serial Passthrough

[Broncode](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/tree/master/libraries/SAMDaaNo21/examples/SAMDaaNo21-LoRa-Module-Serial-passthrough)

Deze code kan gebruikt worden om via de computer commando's te sturen naar de RN2483 LoRaWAN module.

Alles dat `SerialUSB` ontvangt wordt doorgestuurd naar `SerialLoRa`.

Alles dat `SerialLoRa` ontvangt wordt doorgestuurd naar `SerialUSB`.

### BME280 Wire LoRa formatting

[Broncode](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/libraries/SAMDaaNo21/examples/BME280-Wire-LoRa-formatting/BME280-Wire-LoRa-formatting.ino)

Gebruikte bibliotheek: https://github.com/adafruit/Adafruit_BME280_Library

Deze code toont de werking van een BME280 en zet de temperatuur, luchtvochtigheid en luchtdruk om naar een array om gemakkelijk door te sturen via LoRaWAN. 


### BME280 LoRa SIS

[Broncode](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/libraries/SAMDaaNo21/examples/BME280-LoRa-SIS/BME280-LoRa-SIS.ino)

Bibliotheek 1: https://github.com/jpmeijers/RN2483-Arduino-Library
Bibliotheek 2: https://github.com/adafruit/Adafruit_BME280_Library

Deze code toont de werking van een BME280 en LoRaWAN. Het zet de temperatuur, luchtvochtigheid en luchtdruk om naar een array en verstuurt deze data via LoRaWAN.  


