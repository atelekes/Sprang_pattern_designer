# Sprang_pattern_designer
Készítsd el a saját sprang mintádat gyorsan és egyszerűen. / Create your own sprang pattern quickly and easily.
A program fejlesztés alatt áll. / This program is currently under development.
Ha rendellenes működést tapasztalsz, kérlek oszd meg, hogy tudjam javítani / If you find a bug, please report it so I can fix it.

Leírás/Description:

⚠️!FIGYELEM!
A program csak Windows 10 és Windows 11 operációs rendszeren működik.

A program futtatásához elegendő duplán rákattintani a start.bat fájlra.
A program indításakor teljesen normális, hogy egy fekete ablak egy pillanatra felvillan.
Pár másodpercen belül maga a program is megnyílik.
A program automatikusan teljes képernyős módban indul.

Kezelés / irányítás:
- Azok a szövegek, amelyekkel interaktálni lehet, mindig kerettel vannak jelölve.
- A Tervezés menüben:
  - A mintaelemek kiválasztásához az 1, 2, 3 billentyűk használhatók.
    A program automatikusan a rács kurzorhoz legközelebbi pontjához illeszti az elemet.
    A hely fixálásához kattintson a bal egérgombbal.
  - Már elhelyezett mintaelem eltávolításához kattintson rá a bal egérgombbal.
  - Már elhelyezett mintaelem mozgatásához kattintson rá a jobb egérgombbal,
    majd az új pozíció rögzítéséhez kattintson ismét a bal egérgombbal.
  - Az egérgörgővel fel és le mozgathatja a mintát.
  - Shift + görgetés: oldalirányú mozgatás.
  - Ctrl + görgetés: nagyítás és kicsinyítés.
  - A sorok és oszlopok számát úgy módosíthatja,
    hogy, az ezt jezlő szöveg fölé viszi a kurzort, majd a görgő segítségével beállítja a kívánt értéket.
- A Mentés gombra kattintva, a minta nevét megadva, majd az Enter billentyűt megnyomva
  a minta elmenthető a 'saves' mappába.
- A mentett minták bármikor betölthetők és tovább szerkeszthetők a Megnyitás menüpontban.
- ⚠️FIGYELEM! Nincs automatikus mentés.
  A nem mentett módosítások elvesznek a program bezárásakor
  vagy új minta megnyitásakor.

Technikai részletek:
- Embedded Python 3.13.5 verziót használ
- A fő program Pygame-ben készült
- A megnyitás funkció Tkinterrel van megvalósítva

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

⚠️ WARNING!
This program only works on Windows 10 and Windows 11.

To run the program, simply double-click the start.bat file.
It is completely normal for a black window to flash briefly when the program starts.
The program itself will open within a few seconds.
It automatically launches in full-screen mode.

Controls / Navigation:
- Texts that can be interacted with are always framed.
- In the Design menu:
  - To select pattern elements, use keys 1, 2, or 3.
    The program automatically snaps elements to the nearest grid point.
    Click the left mouse button to fix the element in place.
  - To remove an already placed element, click it with the left mouse button.
  - To move an already placed element, right-click it,
    then left-click again to fix it in the new position.
  - Use the mouse wheel to scroll the pattern up and down.
  - Shift + scroll: move the pattern sideways.
  - Ctrl + scroll: zoom in and out.
  - To change the number of rows and columns,
    hover the cursor over the corresponding label,
    then use the mouse wheel to set the desired value.
- Click the Save button, enter the pattern name, and press Enter
  to save the pattern in the 'saves' folder.
- Saved patterns can be loaded and edited at any time via the Open menu.
- ⚠️ WARNING! There is no automatic save.
  Unsaved changes will be lost if you close the program
  or open a new pattern.

Technical Details:
- Uses embedded Python 3.13.5
- Main program is written in Pygame
- Tkinter is used for the file opening functionality
