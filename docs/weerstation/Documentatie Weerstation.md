# Documentatie Weerstation

### Onderzoek

#### Op voorhand:

- In het hoofdstuk Data Formatting, onder metingen staat er in detail beschreven hoe dat er onderzoek werd gevoerd naar de waarop het weerstation data doorstuurt.

- Er is een [bestaand project](https://www.skyon.be/maak-je-weerstation-geconnecteerd-en-slim/) met hetzelfde weerstation. Dit wordt gebruikt als referentie.

#### Hands on:

##### Weerstation opbouwen en uittesten

We krijgen data binnen van het weerstation op de GUI dat meekwam met het weerstation. 

##### [Dit project](https://www.skyon.be/maak-je-weerstation-geconnecteerd-en-slim/) volgen stap voor stap

We hebben het commando hieronder uitgevoerd. We hebben de parameters ingevuld met onze eigen mqtt server. Jammer genoeg zagen we geen data binnen komen op de mqtt server. 

```
/usr/local/bin/rtl_433 -R 119 -f 868M -s 1024k -F mqtt://<mqtt_server_ip> 1883 retain 0 devices rtl_433[/id]
```

We weten niet goed wat er mis gaat met de RTL-SDR. Hier moet meer mee gexperimenteerd worden.

##### Met een HackRF proberen onderscheppen

- Met behulpt van GQRX heb ik ontdekt dat het weerstation werkt op 868.3MHz

- Ik heb dan geprobeerd om dit signaal te demoduleren. Ik denk dat er veel ruis op zat of dat ik op een verkeerde manier de data heb opgenomen waardoor dat ik niet kon demoduleren tot een mooi signaal. 
  
  ![Screenshot 2022-10-28 at 12.38.06.png](./Screenshot%202022-10-28%20at%2012.38.06.png)
  
  *fig. 1, GQRX spectrum analyse*

##### Weerstation open maken

We hebben het weerstation open gemaakt om zo toch al een alternatief te onderzoeken voor als de data niet makkelijk onderschept kan worden met een SDR.

TODO: fotos en uitleg fotos toevoegen
