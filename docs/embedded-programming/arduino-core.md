# Embedded Programming

## Arduino core

SAMDaaNo21 toevoegen aan de Arduino IDE.


Om de SAMDaaNo21 werkende te krijgen met een IDE zoals die van Arduino moeten we eerst een compatibele bootloader op de MCU hebben staan. Wij maken gebruik van de ATSAMD21G16B en spijtig genoeg zijn hier geen kant-en-klare bootloaders voor. Omdat we de printplaat zelf hebben ontworpen zijn er uiteraard ook geen volledig compatibele configuraties beschikbaar.

Het toevoegen voor ondersteuning verloopt in een aantal stappen:

- Bootloader voor de [ATSAMD21G16B](https://www.microchip.com/en-us/product/ATSAMD21G16) vinden
- Bootloader flashen
- Een Arduino variant toevoegen voor de SAMDaaNo21
  - Linker script aanpassen
  - OpenOCD script aanpassen
  - Pinout en functies definiëren

Bij deze stappen hebben we ons gebaseerd op de Arduino Zero. Deze heeft echter een ATSAMD21G18A, dat is een variant met meer geheugen.

Alle nodige broncode is te verkrijgen van de [ArduinoCore-samd](https://github.com/arduino/ArduinoCore-samd) GitHub repository. ([Onze fork specifiek voor de SAMDaaNo21](https://github.com/DaanDekoningKrekels/ArduinoCore-samd))

Belangrijke mappen en bestanden:

| Naam         | Beschrijving                                                 |
| ------------ | ------------------------------------------------------------ |
| bootloaders/ | Map met broncode voor alle type Arduino's.                   |
| variants/    | Map met broncode voor alle verschillende varianten van Arduino's om compatibel te zijn met de Arduino bibliotheken. |
| boards.txt   | Bestand met definities en instellingen voor Arduino borden weer te geven in de Arduino IDE onder `tools`-> `board: xxx` |



## Bootloader

### Adafruit UF-2

Eerst leek het ons interessant om de Adafruit bootloader aan te passen aan de SAMDaaNo21. Die maakt het gemakkelijk om met de Arduino IDE te werken maar ook om met CircuitPython.

https://github.com/DaanDekoningKrekels/uf2-samdx1

https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/uf2-bootloader-details

De UF2 bootloader van Adafruit is BOSSA compatible, wat wil zeggen dat deze ook werkt met de Arduino IDE. Spijtig genoeg is het ons niet gelukt om een werkende versie van deze bootloader te compileren.

### Arduino Core voor SAMD21 CPU

Hiervoor speelt alles zich af in de [./bootloaders/](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/tree/master/bootloaders) folder van de GitHub repo.

Folder van de Arduino Zero `zero/` gedupliceerd en hernoemd naar `samdaano21/`.

Belangrijke bestanden:

| Naam                           | Beschrijving                                                 |
| ------------------------------ | ------------------------------------------------------------ |
| Makefile                       | Beschrijft alle instellingen voor de compiler.               |
| board_definitions.h            | Lijst de verschillende borden op.                            |
| board_definitions_samdaano21.h | Bestand gebaseerd op board_definitions_zero.h, specifiek voor de SAMDaaNo21. Bevat instellingen voor de bootloader zoals USB VID, PID en CPU frequentie. |
| bootloader_samd21x16.ld        | Bestand gebaseerd op bootloader_samd21x18.ld, is een linker script waar onder andere de geheugen regios in worden beschreven. |


#### Board definitions

We dupliceren `board_definitions_zero.h` en hernoemen de kopie naar `board_definitions_samdaano21.h`. 

In dit bestand passen we enkel de USB instellingen aan en het BOOT_DOUBLE_TAP_ADDRESS. Dat adres is afhankelijk van de hoeveelheid ram. Op het moment dat er dubbel gedrukt wordt op de RESET knop, zal de bootloader in de laatste 4 bytes van het geheugen uitvoeren. Het adres is dus de totale RAM - 4 bytes. $8\text{kb} - 4\text{b} = 0\text{x}2000 - 0\text{x}4 = 0\text{x}1FFC$

`board_definitions_samdaano21.h`

```c
[...]
/*
 * USB device definitions
 */
#define STRING_PRODUCT "SAMDaaNo21"
#define USB_VID_HIGH   0x03     // Atmel
#define USB_VID_LOW    0xEB
#define USB_PID_HIGH   0x24     // Generic HID device
#define USB_PID_LOW    0x02
/*
 * If BOOT_DOUBLE_TAP_ADDRESS is defined the bootloader is started by
 * quickly tapping two times on the reset button.
 * BOOT_DOUBLE_TAP_ADDRESS must point to a free SRAM cell that must not
 * be touched from the loaded application.
 */
//#define BOOT_DOUBLE_TAP_ADDRESS           (0x20007FFCul)
// https://forum.arduino.cc/t/how-to-upload-arduino-bootloader-to-a-custom-samd21-usig-jlink-mini/906434/13
#define BOOT_DOUBLE_TAP_ADDRESS           (0x20001FFCul) // 8kb ram - 4 bytes = 10x8188 0x1FFC
#define BOOT_DOUBLE_TAP_DATA              (*((volatile uint32_t *) BOOT_DOUBLE_TAP_ADDRESS))
[...]
```

`board_definitions.h` moet nu aangepast worden om ons nieuwe bestand te kunnen includen.

Pas het volgende aan:

`board_definitions.h`

```c
#if defined(BOARD_ID_samdaano21)
  #include "board_definitions_samdaano21.h"
#elif defined(BOARD_ID_arduino_zero)
  #include "board_definitions_arduino_zero.h"
[...]
```



#### Linker script

Referentie: https://forum.arduino.cc/t/how-to-upload-arduino-bootloader-to-a-custom-samd21-usig-jlink-mini/906434/11

Zeer goede documentatie: https://blog.thea.codes/the-most-thoroughly-commented-linker-script/

`bootloader_samd21x18.ld` -> `bootloader_samd21x16.ld `

Dit is het linker script. Daarin is enkel de memory mapping aangepast. De ATSAMD21x18 versie heeft 256kb flash en 32kb SRAM. De ATSAMD21x16 heeft 64kb flash en 8kb SRAM. Deze waardes zijn hexadecimaal in het linker script geplaatst.

`bootloader_samd21x16.ld`

```c
MEMORY
{
  FLASH (rx) : ORIGIN = 0x00000000, LENGTH = 0x2000 /* First 8KB used by bootloader */
  RAM (rwx) : ORIGIN = 0x20000000, LENGTH = 0x00002000-0x0400 /* last 4 bytes used by bootloader to keep data between resets, but reserves 1024 bytes for sketches to have same possibility */
}
```

#### Makefile

De makefile geeft de compiler de juiste instructies om de bootloader te kunnen samenstellen. Hier passen we het BOARD_ID aan, de verwijzing naar het LD_SCRIPT en veranderen bij compiler options de MCU van G18A naar G16A.

`Makefile`

```makefile
[...]
# Boards definitions
BOARD_ID?=samdaano21
[...]
CFLAGS_EXTRA=-D__SAMD21G16A__ -DBOARD_ID_$(BOARD_ID) -D$(SAM_BA_INTERFACES)
[...]
LD_SCRIPT=bootloader_samd21x16.ld
[...]
```

#### Compileren

Met het commando `make clean all` kan de gehele bootloader gecompileerd worden.

Er zal een `samd21_sam_ba.hex` en een `samd21_sam_ba.bin` bestand aangemaakt worden.


#### Problemen

Het had fijn geweest moest het werk geloond hebben, maar deze bootloader hebben we niet werkende gekregen. Het lukte niet om via de Arduino IDE code te uploaden naar de SAMDaaNo21. Via een programmer lukte het echter wel om bootloader + code te draaien.

Als alternatief zijn we terechtgekomen bij de standaard bootloader die Microchip aanbiedt voor hun SAMD lijn, de SAM-BA bootloader. 

SAM-BA maakt het mogelijk om via USB te communiceren met een AT SAM microcontroller. Op deze manier is er geen externe programmer nodig!

Wetende dat deze bootloader bestaat, is het enkel nog zoeken naar de download link... Alle verwijzingen in de volgende PDF's zien er als volgt uit:

>The user guide comes with the SAM-BA package available on www.atmel.com.

Enkele links over SAM-BA (SAM Boot Assist):

-  [AN_42438 - AT09423: SAM-BA Overview and Customization Process (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42438-SAM-BA-Overview-and-Customization-Process_ApplicationNote_AT09423.pdf) 
-  [AN_42366 - AT07175: SAM-BA Bootloader for SAM D21 (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42366-SAM-BA-Bootloader-for-SAM-D21_ApplicationNote_AT07175.pdf)
-  [AN_42728 - AT15004:Using SAM-BA for Linux on SAM Devices (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42728-Using-SAM-BA-for-Linux-on-SMART-ARM-based-Microcontrollers_ApplicationNotes_AT15004.pdf) 
-  [SAM-BA Monitor for ROMless Cortex M Devices - SAM-BA® Monitor for ROMless Cortex Devices Application Note (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/00002565A.pdf) 
-  [How to Customize ASFv3 SAM-BA Bootloader on Cortex- (PDF)](https://ww1.microchip.com/downloads/en/DeviceDoc/How-to-Customize-ASFv3-SAM-BA-Bootloade-on-Cortex-M0-Microcontrollers-DS90003190A.pdf) 
-  [Where can I download the official ATSAM D21 bootloader and how to burn it??](https://www.avrfreaks.net/s/topic/a5C3l000000Uiu3EAC/t185718)
-  [SAM-BA Bootloader for SAMD21G15B](https://www.avrfreaks.net/s/topic/a5C3l000000Uf3qEAC/t170949)
-  [SAM-BA Bootloader! (ZIP)](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42366-SAM-BA-Bootloader-for-SAM-D21_ApplicationNote_AT07175.zip)

De laatste link gaat rechtstreeks naar de download van de bootloader. De inhoud zit er als volgt uit:

```
.
├── LED_Toggle_0x1000.bin
├── LED_Toggle_0x2000.bin
├── load sam-ba
│   ├── samd21e15a
│   ├── samd21e16a
│   ├── samd21e17a
│   ├── samd21e18a
│   ├── samd21g15a
│   ├── samd21g16a
│   │   ├── samd21_sam_ba_both_interfaces.hex
│   │   ├── samd21_sam_ba_uart.hex
│   │   └── samd21_sam_ba_usbcdc.hex
│   ├── samd21g17a
│   ├── samd21g18a
│   ├── samd21j15a
│   ├── samd21j16a
│   ├── samd21j17a
│   └── samd21j18a
└── sam-ba_monitor.zip
```

Enkel de bootloader `samd21_sam_ba_both_interfaces.hex` in de map `samd21g16a` is voor ons van toepassing. Met deze bootloader werkt uploaden vanaf de Arduino IDE!

Hoe je deze bootloader kan flashen kan je [hier](bootloader-flashen.md) lezen.

Een belangrijke kanttekening: De Arduino IDE gebruikt de programmerings-tool [BOSSA](https://github.com/shumatech/BOSSA) om binaries naar een SAM-BA apparaat te sturen. Deze tool ondersteunt standaard de ATSAMD21G16 **niet**. Om die reden moet een [aangepaste versie van BOSSA](https://github.com/mattairtech/BOSSA) gebruikt worden, namelijk deze van Justin Mattair (mattairtech).

Nu we een bootloader hebben, moet deze naar de SAMDaaNo21 geschreven worden. Zie documentatie.

## Arduino variant

Wanneer de bootloader op de SAMDaaNo21 straat en je sluit de USB-poort aan, zal je onder `tools`-> `port` een apparaat zien staan!

We kunnen echter nog niets programmeren naar de SAMDaano21 omdat de Arduino IDE niet weet hoe het apparaat werkt. In de volgende stappen voegen we een Arduino variant toe aan de IDE.

Hiervoor speelt het meeste zich af in de ./variants/ folder van de GitHub repo, `boards.txt` passen we ook aan.

| Naam                                           | Beschrijving                                                 |
| ---------------------------------------------- | ------------------------------------------------------------ |
| boards.txt                                     | Bestand met definities en instellingen voor Arduino borden weer te geven in de Arduino IDE onder `tools`-> `board: xxx` |
| variants/samdaano21/                           |                                                              |
| variant.h                                      | Bestand waar alle pin-namen die via de Arduino IDE aanspreekbaar zijn worden gedefinieerd. |
| variant.cpp                                    | Bestand waar alle beschikbare pinnen en hun functies in één array worden samengebracht. |
| openocd_scripts/samdaano21.cfg                 | OpenOCD script om te communiceren met de MCU.                |
| linker_scripts/gcc/flash_with_bootloader.ld    | Linker script dat wederom de geheugen regio's weergeeft, ditmaal met een offset van 8kb om de bootloader niet te overschrijven. |
| linker_scripts/gcc/flash_without_bootloader.ld | Linker script dat wederom de geheugen regio's weergeeft.     |

### variant.cpp en variant.h

In het `variant.cpp` bestand zit een grote array waarin iedere bruikbare pin definitie wordt bijgehouden. De opties voor individuele pinnen zijn gedefinieerd in `WVariant.h`, dat bestand kan je vinden in de core folder.

Per pin op de SAMDaaNo21 zijn er functies die toegewezen worden. Om de juiste functies toe te wijzen aan de pinnen refereer je naar de [datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-D21DA1-Family-Data-Sheet-DS40001882G.pdf) hoofdstuk 7 I/O Multiplexing and Considerations. Mogelijke functies:

[`WVariant.h`](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/cores/arduino/WVariant.h#L201)

```cpp
/* Types used for the table below */
typedef struct _PinDescription
{
  EPortType       ulPort ;
  uint32_t        ulPin ;
  EPioType        ulPinType ;
  uint32_t        ulPinAttribute ;
  EAnalogChannel  ulADCChannelNumber ; /* ADC Channel number in the SAM device */
  EPWMChannel     ulPWMChannel ;
  ETCChannel      ulTCChannel ;
  EExt_Interrupts ulExtInt ;
} PinDescription ;
```

Deze functies worden in [`variant.cpp`](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/variants/samdaano21/variant.cpp) op volgende manier weergegeven:

```cpp
{ PORTA,  2, PIO_ANALOG, PIN_ATTR_ANALOG, ADC_Channel0, NOT_ON_PWM, NOT_ON_TIMER, EXTERNAL_INT_2 }, // ADC/AIN[0]
```

PA02 is dus een analoge pin die gebruik maakt van ADC:0. Er is geen PWM mogelijkheid en geen timer, wel een externe interrupt EXTINT:2.

Bovenstaande lijn code staat op index 0 van de `g_APinDescription` array. In [`variant.h`](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/variants/samdaano21/variant.h) moet de pin daar nog worden ingesteld als analoge pin.

[`variant.h`](https://github.com/DaanDekoningKrekels/ArduinoCore-samd/blob/master/variants/samdaano21/variant.h)

```cpp
/*
 * Analog pins
 */
#define PIN_A0               (0ul)
#define PIN_A1               (1ul)
#define PIN_A2               (2ul)
#define PIN_A3               (3ul)
#define PIN_A4               (6ul)
#define PIN_A5               (14ul)
#define PIN_DAC0             (26ul)

static const uint8_t A0  = PIN_A0;
static const uint8_t A1  = PIN_A1;
static const uint8_t A2  = PIN_A2;
static const uint8_t A3  = PIN_A3;
static const uint8_t A4  = PIN_A4;
static const uint8_t A5  = PIN_A5;
static const uint8_t DAC0 = PIN_DAC0;
#define ADC_RESOLUTION		12
```

Op deze manier worden de pinnen gedefinieerd voor Arduino code. Nu kan er gebruik gemaakt worden van `A0` in de code om een analoge pin uit te lezen.

Om gebruik van de SAMDaaNo21 gemakkelijker te maken zijn alle pinnen die omschreven zijn op de slikscreen (PCB zelf) ook voorgedefinieerd.

**Let op dat `PA07` op de slikscreen staat aangegeven als `PA09`. Dit is een fout die in versie 2 zal worden rechtgezet.**

```cpp
#define PA02        (0ul)
#define PA03        (1ul)
#define PB08        (2ul)
#define PB09        (3ul)
#define PA04        (4ul)
#define PA05        (5ul)
#define S0TX        (4ul) // TX SERCOM0 UART
#define S0RX        (5ul) // RX
#define PA06        (6ul)
#define PA07        (7ul)
#define PA08        (8ul)
#define PA09        (9ul)
#define S2TX        (8ul) // TX SECOM 2 UART
#define S2RX        (9ul) // RX
#define PA10        (10ul)
#define PA11        (11ul)
#define PA12        (12ul)
#define PA13        (13ul)
#define S4SDA       (12ul) // SDA SERCOM 4 I2C
#define S4SCL       (13ul) // SCL

// Andere kant
#define PB03        (14ul)
#define PB22        (15ul)
#define PA23        (16ul)
#define PA22        (17ul)
#define S5RX        (16ul) // RX SERCOM 5 UART
#define S5TX        (17ul) // TX
#define PA21        (18ul)
#define PA20        (19ul)
#define PA19        (20ul)
#define PA18        (21ul)
#define PA17        (22ul)
#define PA16        (23ul)
#define S3SS        (20ul) // SS SERCOM 3 SPI
#define S3MISO      (21ul) // MISO
#define S3SCK       (22ul) // SCK
#define S3MOSI      (23ul) // MOSI
#define PA15        (24ul)
#define PA14        (25ul)
```

Ook de SERCOM poorten zijn in dit bestand geformuleerd.





## Bronnen

- S. (2016, 30 juli). Porting Arduino Zero to another samd21g variant. Arduino Forum. https://forum.arduino.cc/t/porting-arduino-zero-to-another-samd21g-variant/400138/3
- Instructables. (2019, 15 mei). Arduino IDE: Creating Custom Boards. https://www.instructables.com/Arduino-IDE-Creating-Custom-Boards/
- Docs: How the variant system works on Arduino Zero boards | Details | Hackaday.io. (z.d.). https://hackaday.io/project/8007-hack/log/41354-docs-how-the-variant-system-works-on-arduino-zero-boards
- Smart | Connected | Secure | Microchip Technology. (z.d.). https://www.microchip.com/
- H. (2021, 18 september). How to upload arduino bootloader to a custom samd21 usig Jlink mini. Arduino Forum. https://forum.arduino.cc/t/how-to-upload-arduino-bootloader-to-a-custom-samd21-usig-jlink-mini/906434/11
- Adafruit Feather M4 Express. (2018, 11 juli). Adafruit Learning System. https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/uf2-bootloader-details

