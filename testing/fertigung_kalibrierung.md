# Fertigungskalibrierung H2S (Protokollvorlage)

Ausfüllen gemäss `manufacturing/process_limits.md`, Abschnitt 5. Gemessene Werte danach in `cad/mechlib/fab.py` eintragen und `python cad/build_all.py` ausführen.

| Datum | Firmware | Material / Charge | Coupon | Messwerte | Ergebnis → Parameter | Person |
|---|---|---|---|---|---|---|
| | | Pappel 3 mm / … | M00-P04 Matrix | bestandene Sätze: … | Laser-Satz 3 mm: …% / … mm/s | |
| | | Pappel 4 mm / … | M00-P04 Matrix | | PLY4 frei? ja/nein | |
| | | Pappel 3 mm / … | M00-P01 Kerf-Kamm | Finger 1–9: … | KERF = … mm | |
| | | Pappel 3 mm / … | M00-P02/P03 | passender Schlitz: … | SLOT_CLR = … mm | |
| | | PETG / … | M00-P05 | 608 hält in Ø …; Welle dreht in Ø … | PRESS_608 = …, HOLE_COMP = … | |
| | | CARD05 / … | M00-P06 | Druck … gf, Ø3 sauber? | Plotterdruck CARD05 = … gf | |
| | | PET019 / … | M00-P06 | | Plotterdruck PET019 = … gf, frei? | |
| | | GASKET05 / … | M00-P06 | | frei? | |
| | | SIL05 / … | M00-P06 | | frei? | |

Status: **nicht durchgeführt** – keine Fertigungsfreigabe.
