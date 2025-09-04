# Infos

## Sim Modul

Typ: `Sim800L`

Sim Pin: `9305`

[Hier](https://github.com/TheEinfachFelix/CampPhone/blob/main/src/CampPhoneDemo/src/main.cpp) ist noch ein Beispiel, welches alles macht.

[Hier](https://github.com/vittorioexp/Sim800L-Arduino-Library-revised/tree/217d1ea3e46220ec850687141b6a5c5a0835088e) ist ein Link zu der Bibliothek.

### Sonstiges

- Nimm die Antenne vom LORA-Modul (habe vergessen, die passende mit zu nehmen. Aber die Frequenzen sind nah genug beieinander).
- In meinen Versuchen ist das Modul öfter mal beim Testen gestorben. Ich glaube, das Problem habe ich mit dem Spannungsteiler gelöst.
- Es gibt auch noch genug andere Bibliotheken.
- [Hier](https://www.makerhero.com/img/files/download/Datasheet_SIM800L.pdf) ist das Datenblatt (schaut mal hier `4.3. Power Saving Mode`).
- Zum Betreiben wird der Akku gebraucht.

## GPS Modul

Typ: `GY-NEO6MV2`

Beispielcode habe ich in der `GPS Code.cpp`.

## Funktionale Anforderungen

Der ESP soll alle X Minuten das machen:

1. GSM-Modul aus dem Schlaf holen.
2. GPS auslesen.
3. Warten, bis das GSM bereit ist.
4. Wenn es Fehler gibt, diese versuchen zu lösen (Neuversuchen und Neustart).
5. GPS-Daten per SMS versenden.
6. GSM-Modul schlafen legen.

### Erweiterungen

- Der ESP und/oder GPS soll auch schlafen.
- Es sollen auch die Sensordaten des anderen ESPs versendet werden.

## Nichtfunktionale Anforderungen

- Keine Magic Values.
- Sinnvolle Namen für Variablen.
- Den Code sinnvoll in Funktionen aufteilen (z. B.: `setupGPS()`, `getGPSdata()` usw.).
