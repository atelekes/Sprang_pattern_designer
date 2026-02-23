!FIGYELEM!
A program csak Windows 10 és Windows 11 operációs rendszeren működik.

A program futtatásához elegendő duplán rákattintani a start.bat fájlra.
A program indításakor teljesen normális, hogy egy fekete ablak megjelenik.
Pár másodpercen belül maga a program is megnyílik.
A program automatikusan teljes képernyős módban indul.

Kezelés / irányítás:
- Azok a szövegek, amelyekkel interaktálni lehet, mindig kerettel vannak jelölve.
- A Rajzolás menüben:
  - A mintaelemek kiválasztásához az 1, 2, 3, 4, 5, 6 billentyűk használhatók.
    Ilyenkor a  program automatikusan a rács kurzorhoz legközelebbi négyzetéhez illeszti az mintaelemet.
    A hely fixálásához kattintson a bal egérgombbal.
  - Már elhelyezett mintaelem eltávolításához kattintson rá a bal egérgombbal.
  - Már elhelyezett mintaelem mozgatásához kattintson rá a jobb egérgombbal,
    majd az új pozíció rögzítéséhez kattintson ismét a bal egérgombbal.

  - A mintaelemek típusát (Z vagy S) a Q billenytű lenyomásával lehet változtatni
    a kijelölt mintaelemen (amelyik fölött van a kurzor, ekkor picit világosabb is a színe).
  - A rács típusát (Z vagy S) az ALT billenytű lenyomásábal lehet változtatni a kijelölt rácspontot.

  - Az egérgörgővel fel és le mozgathatja a mintát.
  - Shift + görgetés: oldalirányba mozgathatja mozgatás a mintát.
  - A görgő folyamatos lenyomásával a teljes minta mozgatható (olcsóbb egereknél nem mindig működik).
  - Ctrl + görgetés: nagyítás és kicsinyítés.
  - A nyilak segítségével csak a mintaelemeket tudja mozgatni a rácson.

  - A mentéshez használhatja a Mentés gombot, vagy az F9-es gombot
  - A minta képként való mentéséhez használja a Képernyőkép gombot vagy az F10-es gombot.
    Képernyőkép készítésekor csak abból a részből készül kép, amelyik a képernyőn is látszódik, a menüsáv nem jelenik meg a képen.
  - Az menüsáv az F11-es gomb megnyomásával eltüntethető.
  - A mintában lévő lyukakat (álló egyenes fekete sávok) az F12-es gombal tüntethető el.

  - A sorok és oszlopok számát úgy módosíthatja, hogy, az ezt jezlő szöveg (bekeretezett) fölé viszi a kurzort, 
    majd a görgő segítségével beállítja a kívánt értéket.

  - A mentett minták bármikor betölthetők és tovább szerkeszthetők a Megnyitás menüpontban.
  - FIGYELEM! Nincs automatikus mentés.
  - A nem mentett módosítások elvesznek a program bezárásakor vagy új minta megnyitásakor.

Technikai részletek:
 - Embedded Python 3.13.5 verziót használ
 - A fő program Pygame Community Edition-ben készült
 - A megnyitás és mentés funkció Tkinterrel van megvalósítva
 - Ezek mellett még a NumPy könyvtárat használja
