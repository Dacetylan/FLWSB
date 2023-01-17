# OpenOCD script voor SAM D21

In de repository met de ArduinoCore voor de SAMDaaNo21 is ook een script te vinden voor het flashen van de correcte bootloader.

Het OpenOCD script "`program-bootloader.cfg`", te vinden in deze directory bevat de nodige stappen om de correcte bootloader, afkomstig van MICROCHIP/ATMEL te flashen.

## Flashen

Voor het flashen heb je een aantal dingen nodig.
- OpenOCD (best deze van Arduino uit `/home/username/.arduino15/packages/arduino/tools/openocd/0.10.0-arduino7/bin/openocd`)
- Atmel-ICE om via SWD te programmeren
- SAMDaaNo21 met ATSAMD21G16 MCU

Stappen:
1. Sluit de SAMDaaNo21 aan op je computer via de Atmel-ICE zoals bij het hoofdstuk [SAMDaaNo21 Bare-Metal Programmatie](https://dacetylan.github.io/FLWSB/#/./embedded-programming/bare-metal?id=programmeren). 
2. Navigeer naar deze folder 
3. Voer dit commando uit: `openocd -f program-bootloader.cfg`.
   - Met de `-f` parameter selecteren we het aangepaste script als configuratiebestand.
4. De eerste keer treedt er waarschijnlijk een fout op, dan voer je het commando simpelweg opnieuw uit.

### Manueel

Wanner je het commando `openocd` zo uitvoert, zal het `openocd.cfg` script gebruikt worden. Dit script geeft enkel aan dat we via SWD willen programmeren naar een ATSAMD21G16 MCU en start een telnet interface.

Verder kan je de stappen volgen uit het hoofdstuk [SAMDaaNo21 Bare-Metal Programmatie](https://dacetylan.github.io/FLWSB/#/./embedded-programming/bare-metal?id=programmeren) of de commando's uit `program-bootloader.cfg` handmatig invoeren. 



## Bronnen

Enkele links over SAM-BA (SAM Boot Assist):

De laatste link gaat rechtstreeks naar de download van de bootloader. De bootloader is echter ook aanwezig in deze folder [`samd21_sam_ba.hex`](samd21_sam_ba.hex), [`bootloaders/samd21_sam_ba_both_interfaces.hex`](bootloaders/samd21_sam_ba_both_interfaces.hex).

-  [AN_42438 - AT09423: SAM-BA Overview and Customization Process (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42438-SAM-BA-Overview-and-Customization-Process_ApplicationNote_AT09423.pdf) 
-  [AN_42366 - AT07175: SAM-BA Bootloader for SAM D21 (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42366-SAM-BA-Bootloader-for-SAM-D21_ApplicationNote_AT07175.pdf)
-  [AN_42728 - AT15004:Using SAM-BA for Linux on SAM Devices (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42728-Using-SAM-BA-for-Linux-on-SMART-ARM-based-Microcontrollers_ApplicationNotes_AT15004.pdf) 
-  [SAM-BA Monitor for ROMless Cortex M Devices - SAM-BA® Monitor for ROMless Cortex Devices Application Note (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/00002565A.pdf) 
-  [How to Customize ASFv3 SAM-BA Bootloader on Cortex- (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/How-to-Customize-ASFv3-SAM-BA-Bootloade-on-Cortex-M0-Microcontrollers-DS90003190A.pdf) 
-  [Where can I download the official ATSAM D21 bootloader and how to burn it??](https://www.avrfreaks.net/s/topic/a5C3l000000Uiu3EAC/t185718)
-  [SAM-BA Bootloader for SAMD21G15B](https://www.avrfreaks.net/s/topic/a5C3l000000Uf3qEAC/t170949)
-  [SAM-BA Bootloader! (ZIP)](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42366-SAM-BA-Bootloader-for-SAM-D21_ApplicationNote_AT07175.zip)








OpenOCD Linux binary afkomstig uit `/home/username/.arduino15/packages/arduino/tools/openocd/0.10.0-arduino7/bin/openocd`



