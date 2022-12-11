# Documentatie SAMDaaNo21 Programmatie

Dit is een korte handleiding om op weg te geraken met het programmeren van de SAMDaaNo21 (en andere SAMD chips). Deze handleiding gebruikt OpenOCD en gcc-arm-embedded in plaats van Atmel Studios. Atmel Studios maakt gebruik van dezelfde tools, toch werkt Atmel Studios enkel op Windows. Dit is geen optie aangezien er 3 operating systemen gebruikt worden in ons team (Windows, Mac OS, Linux Mint21). Het gebruik van open source tools zoals OpenOCD en gcc-arm-embedded maakt het een stuk makkelijker om samen de SAMDaaNo21 te programmeren.

Het is ook mogelijk de SAMDaaNo21 te programmeren zonder Atmel ICE. Dit kan met een RaspberryPI.

## Installatie

#### Mac OS

Om verder te kunnen is [Brew.sh](https://brew.sh/) nodig. Dit is een cli tool gelijkaardig aan apt-get op linux.

---

`brew install openocd --cask`

`brew install gcc-arm-embedded`

OpenOCD is een geweldige debug tool die met een groot bereik van microcontrollers werkt. Documentatie van OpenOCD is [hier](https://openocd.org/pages/documentation.html) te vinden. OpenOCD is ook verantwoordelijk voor het programmeren van de chip (de C code moet je uiteraard zelf nog schrijven).

gcc-arm-embedded is wat de C code compileert naar een binary file.

---

tijdens dat brew openocd aan het installeren is moet je een file aanmaken.

`touch openocd.cfg`

in deze file zet je het volgende:

```editorconfig
# Atmel-ICE JTAG/SWD in-circuit debugger.
interface cmsis-dap

# Chip info
set CHIPNAME at91samd21g16
source [find target/at91samdXX.cfg]
```

Als je een andere chip dan de SAMD21g16b gebruikt dan moet dit aangepast worden in de config file.

---

#### Windows

#### Linux

#### Raspberry Pi

## Verbinden

#### Atmel ICE

Op de user guide van de Atmel Ice ([hier te vinden](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-ICE_UserGuide.pdf)) is een beschrijving van de pinout van de Atmel Ice. Deze is te vinden op pagina 22 onderaan in een tabel. De verbindingen met de SAMDaaNo21 zijn de volgende:

| Atmel Ice (SAM Port) | SAMDaaNo21 |
| -------------------- | ---------- |
| SWDCLK               | SWCLK      |
| SWDIO                | SWDIO      |
| nSRST                | RESET      |
| VTG                  | 3V3        |
| GND                  | GND        |

#### Raspberry Pi

## Compileren

#### Mac OS

Om op Mac OS een `.C` file te compileren naar een binaire file die geprogrammeerd kan worden op de SAMDaaNo21 moet er eerst een Makefile aangemaakt worden. 

`touch Makefile`

Zet de volgende code in de Makefile:

```makefile
# vervang hier samd21g16b_flash.ld en 
# __SAMD21G16B__ door de juiste chip als er 
# een andere chip gebruikt wordt.
LDSCRIPT = samd21g16b_flash.ld
PTYPE=__SAMD21G16B__

CC=arm-none-eabi-gcc
LD=arm-none-eabi-gcc
AR=arm-none-eabi-ar
AS=arm-none-eabi-as

ELF=$(notdir $(CURDIR)).elf
# vervang hier ./xdk-asf-3.52.0 door
# de juiste path naar ASF3.
# Let op. Dit kan een andere versie zijn!
ASF_ROOT=./xdk-asf-3.52.0

INCLUDES= \
        sam0/utils/cmsis/samd21/include \
        sam0/utils/cmsis/samd21/source \
        thirdparty/CMSIS/Include \
        thirdparty/CMSIS/Lib/GCC 

OBJS = startup_samd21.o main.o 

LDFLAGS+= -T$(LDSCRIPT) -mthumb -mcpu=cortex-m0 -Wl,--gc-sections
CFLAGS+= -mcpu=cortex-m0 -mthumb -g
CFLAGS+= $(INCLUDES:%=-I $(ASF_ROOT)/%) -I .
CFLAGS+= -D$(PTYPE)
CFLAGS+=-pipe -Wall -Wstrict-prototypes -Wmissing-prototypes -Werror-implicit-function-declaration \
-Wpointer-arith -std=gnu99 -fno-strict-aliasing -ffunction-sections -fdata-sections \
-Wchar-subscripts -Wcomment -Wformat=2 -Wimplicit-int -Wmain -Wparentheses -Wsequence-point \
-Wreturn-type -Wswitch -Wtrigraphs -Wunused -Wuninitialized -Wunknown-pragmas -Wfloat-equal \
-Wundef -Wshadow -Wbad-function-cast -Wwrite-strings -Wsign-compare -Waggregate-return \
-Wmissing-declarations -Wformat -Wmissing-format-attribute -Wno-deprecated-declarations \
-Wpacked -Wredundant-decls -Wnested-externs -Wlong-long -Wunreachable-code -Wcast-align \
--param max-inline-insns-single=500

$(ELF):    $(OBJS)
        $(LD) $(LDFLAGS) -o $@ $(OBJS) $(LDLIBS)

# compile and generate dependency info

%.o:    %.c
        $(CC) -c $(CFLAGS) $< -o $@
        $(CC) -MM $(CFLAGS) $< > $*.d

%.o:    %.s
        $(AS) $< -o $@

info:       
        @echo CFLAGS=$(CFLAGS)
        @echo OBJS=$(OBJS)

clean:
        rm -f $(OBJS) $(OBJS:.o=.d) $(ELF) $(CLEANOTHER)

debug:    $(ELF)
        arm-none-eabi-gdb -iex "target extended-remote localhost:3333" $(ELF)

-include    $(OBJS:.o=.d)
```

Vervolgens moet ASF (Advanced Software Framework) geïnstalleerd worden. ASF is gelijkaardig aan de Arduino Core, maar dan ontwikkeld door Atmel en gemaakt voor onder andere SAMD chips.

Download en unzip [hier](https://www.microchip.com/en-us/tools-resources/develop/libraries/advanced-software-framework#) ASF3. Hoewel er `Windows (x86/x64)` staat werkt deze ook op Mac OS.

Zet dan de unzipped ASF3 folder in je projectfolder. Er zijn een aantal files die nodig zijn uit deze framework. Deze kan je best ook kopieren naar je projectfolder. Met het commando `cp` is dit simpel.

`VERVANG_DIT_DOOR_ASF3_FOLDER/sam0/utils/cmsis/samd21/source/gcc/startup_samd21.c`

`VERVANG_DIT_DOOR_ASF3_FOLDER/sam0/utils/linker_scripts/samd21/gcc/samd21g16b_flash.ld`

Maak nu een `main.c` file. Hierin komt de `.C` code voor de SAMDaaNo21. Om te testen of dat compileren goed werkt is het mogelijk om het volgende blinky scriptje toe te voegen aan `main.c`. Verbind dan een LED aan PA02.

```c
#include <samd21.h>

static void delay(int n)
{
    int i;

    for (;n >0; n--)
    {
        for (i=0;i<100;i++)
            __asm("nop");
    }
}

int main(void)
{
    REG_PORT_DIR0 |= (1<<2);
    while (1)
    {
        REG_PORT_OUT0 &= ~(1<<2);
        delay(500);
        REG_PORT_OUT0 |= (1<<2);
        delay(500);
    }
}
```

Om nu deze `main.c` te compileren hoef je enkel nog een heel simpel commando uit te voeren:

`make`

#### Windows

#### Linux

#### Raspberry Pi

## Programmeren

Als OpenOCD en gcc-arm-embedded goed geïnstalleerd zijn dan zou het programmeren van de SAMDaaNo21 overal hetzelfde moeten werken.

Open een terminal venster, navigeer naar je projectfolder en voer daar het volgende commando in uit:

`openocd`

Open nu een tweede terminal venster, alle volgende commando's zullen uitgevoerd worden in dit tweede terminal venster

`telnet 127.0.0.1 4444`

> Als je een error krijgt dat telnet niet geïnstalleerd is dan kan je dat installeren met het volgende commando

> `sudo port install inetutils`

> Daarna is het mogelijk `telnet` te vervangen met `gtelnet`.

Eens deze opstelling behaald is kan de chip geprogrammeerd worden door het stappenplan hieronder te volgen

1. `init`

2. `targets`

3. `reset halt`

4. `at91samd21 bootloader 0`

5. `flash write_image [path naar de .elf file dat er gegenereerd is]`
   
   - Error bij dit commando?
     
     - `at91samd21 bootloader 0`
     
     - `at91samd21 chip-erase`
     
     - `reset`
     
     - druk op de reset knop van de SAMDaaNo21 en begin opnieuw vanaf stap 1

6. `flash verify_image [path naar de .elf file dat er gegenereerd is]`
   
   - Error bij dit commando?
     
     - `at91samd21 bootloader 0`
     
     - `at91samd21 chip-erase`
     
     - `reset`
     
     - druk op de reset knop van de SAMDaaNo21 en begin opnieuw vanaf stap 1

7. `at91samd21 bootloader 8192`

8. `reset`

9. druk op de reset knop van de SAMDaaNo21

Normaal gezien is nu de chip correct geprogrammeerd. Om na te kijken of dat dit ook werkt door met `targets` te kijken of er bij status `running` staat.
