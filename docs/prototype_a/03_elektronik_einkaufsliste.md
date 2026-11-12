# Prototyp A – Schritt 2: Elektronik und Einkaufsliste

Stand 2026-11-12, **aktualisiert:** Der Audioverstärker PAM8302A ist nicht lieferbar. Ersatz ist der H-Brücken-Treiber **DRV8833**, angesteuert mit PWM vom Pico wie ein filterloser Klasse-D-Verstärker. Antrieb: Tang Band W1-2121S mit Vorwiderstand **18 Ω** (auf 5 V Fehlerspannung ausgelegt, Schritt 1b). Preise sind Schätzungen (G) in CHF. Die Bezugsquellen sind Beispiele (Schweiz: Bastelgarage, Distrelec, Mouser CH, Digitec/Galaxus; EU: Reichelt, Soundimports). Artikelnummern und Lieferbarkeit bitte selbst prüfen.

## 1. Aufbau

```mermaid
flowchart LR
  PSU["Netzteil 5 V fest<br/>(ohne USB-PD)"] --> SW["Schalter + Polyfuse"]
  SW --> PICO["Raspberry Pi Pico 2<br/>Signal, Messung, Watchdog"]
  SW --> AMP["H-Brücke DRV8833<br/>(nSLEEP: Standard AUS)"]
  PICO -- "2 × PWM, 3-stufig<br/>(Signal)" --> AMP
  PICO -- "Freigabe nSLEEP" --> AMP
  AMP --> INA["Strommessung INA219<br/>(in Reihe)"] --> RS["Vorwiderstand 18 Ω / 3 W"] --> SPK["Tang Band W1-2121S"]
  SEN["Drucksensor MPXV7007DP<br/>±7 kPa analog"] -- "Teiler 2/3" --> PICO
  SEN --> CMP["Fensterkomparator LM393<br/>±4 kPa"]
  CMP -- "zieht nSLEEP auf LOW" --> AMP
  NTC["NTC am Magnet"] --> PICO
```

**Sicherheitsfunktionen in Hardware** (IDs aus `docs/pressure_actuator_concepts.md`, Abschnitt 7):

| Funktion | Umsetzung | Anforderung |
|---|---|---|
| Druckbegrenzung, auch bei Elektronikfehler | **Vorwiderstand 18 Ω** an fester 5-V-Versorgung. Auch wenn die H-Brücke dauerhaft die volle Spannung ausgibt (PWM hängt bei 100 %), ist der Druck im Dichtfall ≤ 3,6 kPa (B aus G) | S1 |
| Gleichstromfehler | Fehlerstrom nur 0,23 A, Spule 0,19 W, Widerstand 1,0 W (B) → thermisch unkritisch. Erkennung über INA219 (Gleichanteil des Stroms) → Firmware schaltet ab | S1, S5 |
| Unabhängiger Überdruck-Abbruch | **LM393-Fensterkomparator** direkt am Sensorausgang, Schwellen ±4 kPa (1,357 V / 3,643 V am Sensor, B). Zieht **nSLEEP** der H-Brücke ohne Mikrocontroller auf LOW | S10, S11 |
| Sicherer Startzustand | **nSLEEP** der H-Brücke ist ohne aktive Freigabe LOW (Pull-down), Ausgänge hochohmig. Mikrocontroller aus, im Reset oder abgestürzt → Antrieb aus | S6, S11 |
| Treiberfehler | DRV8833 hat eingebaute Überstrom- und Übertemperaturabschaltung | S5 |
| Feste Versorgung | Netzteil mit fester Ausgangsspannung 5 V, **kein USB-PD**, keine Powerbank | S4 |
| Überstrom | Polyfuse 0,75 A (Halte-) im 5-V-Eingang | S4 |
| Temperatur | NTC 10 kΩ am Magnet des Lautsprechers, Abschaltung > 60 °C in Firmware | S5 |
| Watchdog | Hardware-Watchdog des Pico | S11 |
| Not-Aus | Kippschalter in der 5-V-Zuleitung | S6 |

## 2. Einkaufsliste

### Pflicht

| # | Teil | Spezifikation | Stk | CHF (G) | Zweck / Hinweis |
|---|---|---|---|---|---|
| E1 | **Netzteil 5 V** | Steckernetzteil 5 V DC, 2–3 A, **fester Ausgang, ohne USB-PD**, CE, Hohlstecker 5,5/2,1 (z. B. Mean Well GST18E05-P1J o. ä.) | 1 | 12–20 | S4 |
| E2 | Hohlstecker-Einbaubuchse 5,5/2,1 | passend zu E1 | 1 | 1–2 | |
| E3 | **Mikrocontroller** | Raspberry Pi Pico 2 (RP2350) oder Pico (RP2040), mit Stiftleisten | 1 | 5–8 | ADC 12 bit, PWM, Watchdog, USB-Logging |
| E4 | **H-Brücken-Treiber** | **DRV8833**-Modul (2 Kanäle, 2,7–10,8 V, 1,5 A, Pin **nSLEEP** herausgeführt), z. B. Pololu 2130 oder baugleiche Module | 2 | 3–8 je | 1 Ersatz. Gleichstromgekoppelt bis 0 Hz, kein Tiefpass nötig |
| E5 | **Drucksensor** | **NXP MPXV7007DP**: Differenzdruck ±7 kPa, analog 0,5–4,5 V, 5 V, Ansprechzeit ≈ 1 ms, zwei Schlauchanschlüsse | 1 | 15–25 | S8, S9. Überlastdruck im Datenblatt prüfen (soll ≥ 16 kPa) |
| E6 | **Strommessung** | INA219-Modul (I²C, Shunt 0,1 Ω, ±3,2 A) | 1 | 4–7 | Gleichstrom-Erkennung, Plausibilisierung (S9) |
| E7 | **Komparator** | LM393 (DIP-8) | 2 | 1 | Hardware-Abbruch ±4 kPa (S10) |
| E8 | Trimmpotentiometer | 10 kΩ, Spindeltrimmer | 2 | 2 | Schwellen ±4 kPa einstellen |
| E9 | Widerstand Pull-down nSLEEP | 10 kΩ (im Sortiment E14) | – | – | sicherer Startzustand (S6) |
| E11 | **Polyfuse** | 0,75 A Halte-, ≈ 1,5 A Auslösestrom | 2 | 1 | S4 |
| E12 | **NTC** | 10 kΩ, B = 3950, mit Anschlussdrähten | 2 | 1 | Magnettemperatur (S5) |
| E13 | Kippschalter | 2-polig, ≥ 2 A | 1 | 2 | Not-Aus |
| E14 | Widerstandssortiment | 1/4 W, E12 | 1 | 5 | Teiler (10 k/20 k), Pull-ups/-downs |
| E15 | Kondensatoren | Elko 100 µF/16 V ×4, Keramik 100 nF ×10 | – | 3 | Abblockung (H-Brücke: 100 µF direkt an VM) |
| E16 | Lochrasterplatine | 100 × 160 mm, Streifenraster oder Punkt | 1 | 4 | |
| E17 | Anschlussklemmen | Schraubklemmen 2-polig RM 5,08 | 6 | 3 | Lautsprecher, Versorgung |
| E18 | Silikonschlauch | ID 3 mm, AD 5 mm, 1 m (passend zu den Sensorstutzen) | 1 | 3 | Sensoranschluss; Volumen zu V0 rechnen |
| E19 | USB-Kabel | passend zum Pico (Micro-USB bzw. USB-C) | 1 | 3 | Programmieren, Messdaten |
| — | **Vorwiderstand 18 Ω, ≥ 3 W** | aus Schritt 1b | – | – | S1 |

**Summe Pflicht: ≈ CHF 70–105**

### Empfohlen

| # | Teil | Spezifikation | Stk | CHF (G) | Zweck |
|---|---|---|---|---|---|
| O1 | OLED-Anzeige | 0,96", SSD1306, I²C | 1 | 4–6 | Druck, Frequenz, Status ohne PC |
| O2 | Drehgeber | KY-040 o. ä. mit Taster | 1 | 2–3 | Frequenz und Amplitude einstellen |
| O3 | Steckbrett + Kabel | 830 Kontakte, Jumper-Set | 1 | 6–8 | Vorversuche vor dem Löten |
| O4 | Zweiter Drucksensor | MPXV7007DP | 1 | 15–25 | Vergleichsmessung, Ersatz |

### Nicht in dieser Liste (folgt in Schritt 3, Mechanik und Pneumatik)

- Passives Zweiwege-Überdruckventil (S1b, Lippen- oder Schirmventil)
- Entlüftungskapillare Ø0,2 mm (z. B. Dosiernadel)
- Membranfolie, Schrauben, Kleber für den Stössel

## 3. Nach Eintreffen prüfen

1. **Netzteil:** Leerlaufspannung messen (4,9–5,3 V).
2. **Drucksensor:** Datenblatt kontrollieren:
   - Überlastdruck ≥ 16 kPa (sonst anderen Sensor wählen, S9)
   - Nullpunkt bei offenen Anschlüssen ≈ 2,5 V
3. **H-Brücke, nSLEEP:** Messen, ob das Modul nSLEEP intern auf HIGH zieht (manche Module tun das, damit der Motor ohne Beschaltung läuft). Wenn ja, den Pull-up-Widerstand auf dem Modul entfernen oder den Pin über eine Leiterbahn-Trennung freilegen. **Ohne Freigabe muss nSLEEP LOW sein** (S6). Der LM393 hat einen Open-Collector-Ausgang und zieht sicher auf LOW. Die Freigabe vom Pico läuft über einen 10-kΩ-Serienwiderstand, damit der Komparator sie immer überstimmt.
4. **Ausgang ist eine Brücke:** Nie einen Ausgang gegen GND messen oder verbinden. Der INA219 sitzt in Reihe zwischen Ausgang AOUT1 und Vorwiderstand (Gleichtaktbereich 0–26 V, passt).
5. **Komparatorschwellen** mit einer Spritze am Sensor einstellen: Abschaltung bei +4 kPa und −4 kPa (Kontrolle: U-Rohr, 408 mm Wassersäule).

## 4. Berechnungsgrundlagen (B)

| Grösse | Wert |
|---|---|
| Gleichstrom-Fehler (5 V, 18 Ω): Strom / Spulenleistung / Widerstandsleistung | 0,23 A / 0,19 W / 1,0 W |
| Druck im Dichtfall max. / mit Leck (0,3 mm Hub) | 3,6 kPa / 2,0 kPa (B aus Datenblatt G) |
| PWM | 3-stufig (beide Brückenzweige mittensymmetrisch gegenläufig), ≥ 40 kHz, Sinus aus Tabelle mit 10 kHz Stützrate → im Leerlauf kein Strom |
| Sensor-Empfindlichkeit MPXV7007DP | 286 mV/kPa (0,5–4,5 V für ±7 kPa) |
| Schwellen ±4 kPa am Sensor | 1,357 V / 3,643 V |
| ADC-Bereich nach Teiler 2/3 | 0,33–3,00 V (≤ 3,3 V Pico) |
| Abtastrate Druck | 10 kHz geplant (Pico-ADC bis 500 kS/s) |
| Stromaufnahme gesamt | < 0,5 A (Pico 30 mA, Sensor 10 mA, Brücke ≤ 0,25 A) |
