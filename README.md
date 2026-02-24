# Sprang_pattern_designer
Create your own sprang pattern quickly and easily.
This program is currently under development. 
I welcome user feedback and suggestions for improving the program.
If you find a bug, please report it so I can fix it.

Készítsd el a saját sprang mintádat gyorsan és egyszerűen.
A program fejlesztés alatt áll.
Ha rendellenes működést tapasztalsz, kérlek oszd meg, hogy tudjam javítani.
Szívesen fogadom a felhasználói visszajelzéseket és javaslatokat a program fejlesztésére.


- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

[Click here to download the latest version! / Kattints ide a legfrissebb verzió letöltéséhez!](https://github.com/atelekes/Sprang_pattern_designer/releases/latest/download/Sprang_designer_V2.0.zip)

For Mac users:
1. [Download Python (programming language which the program uses) ](https://www.python.org/downloads/release/python-3135/)
2. Afrer installation open termianal and paste in this: python3 -m pip install numpy, pygame-ce
3. [Download the Mac version of the program](https://github.com/atelekes/Sprang_pattern_designer/releases/latest/download/Sprang.designer_V2.0_macOS.zip)
4. To run the program, double click on the main_for_macOS.pyw file

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

To run the program, simply double-click the start.bat file.
When starting the program, it is completely normal for a black window to appear.
Within a few seconds, the program itself will open.
The program starts automatically in full-screen mode.

Controls / navigation:
- Texts that can be interacted with are always marked with a border.
- In the Drawing menu:
  - To select pattern elements, use the 1, 2, 3, 4, 5, 6 keys.
    The program automatically snaps the pattern element to the grid square closest to the cursor.
    To fix the position, click with the left mouse button.
  - To remove an already placed pattern element, click on it with the left mouse button.
  - To move an already placed pattern element, click on it with the right mouse button,
    then click again with the left mouse button to fix the new position.

  - The type of pattern element (Z or S) can be changed by pressing the Q key
    on the selected pattern element (the one under the cursor, which appears slightly brighter).
  - The grid type (Z or S) can be changed by pressing the ALT key on the selected grid point.

  - Use the mouse wheel to move the pattern up and down.
  - Shift + scroll: move the pattern sideways.
  - Holding down the mouse wheel allows moving the entire pattern (may not work with cheaper mice).
  - Ctrl + scroll: zoom in and out.
  - Using the arrow keys, only the pattern elements can be moved on the grid.

  - To save, use the Save button or the F9 key.
  - To save the pattern as an image, use the Screenshot button or the F10 key.
    When taking a screenshot, only the visible part of the screen is captured; the menu bar does not appear in the image.
  - The menu bar can be hidden by pressing the F11 key.
  - The holes in the pattern (vertical straight black bars) can be removed with the F12 key.

  - You can change the number of rows and columns by moving the cursor over the corresponding (bordered) text,
    then using the mouse wheel to set the desired value.

  - Saved patterns can be loaded and further edited at any time via the Open menu.
  - WARNING! There is no automatic saving.
  - Unsaved changes will be lost when closing the program or opening a new pattern.

Technical details:
 - Uses Embedded Python version 3.13.5
 - The main program was created using Pygame Community Edition
 - The open and save functions are implemented using Tkinter
 - In addition, the NumPy library is used

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Zum Starten des Programms genügt ein Doppelklick auf die Datei start.bat.
Beim Start des Programms ist es völlig normal, dass ein schwarzes Fenster erscheint.
Innerhalb weniger Sekunden öffnet sich das eigentliche Programm.
Das Programm startet automatisch im Vollbildmodus.

Bedienung / Steuerung:
- Texte, mit denen interagiert werden kann, sind immer durch einen Rahmen gekennzeichnet.
- Im Menü Zeichnen:
  - Zur Auswahl der Musterelemente können die Tasten 1, 2, 3, 4, 5, 6 verwendet werden.
    Dabei richtet das Programm das Musterelement automatisch am nächstgelegenen Rasterfeld zum Cursor aus.
    Zum Fixieren der Position klicken Sie mit der linken Maustaste.
  - Zum Entfernen eines bereits platzierten Musterelements klicken Sie mit der linken Maustaste darauf.
  - Zum Verschieben eines bereits platzierten Musterelements klicken Sie mit der rechten Maustaste darauf,
    und anschließend mit der linken Maustaste, um die neue Position zu fixieren.

  - Der Typ des Musterelements (Z oder S) kann durch Drücken der Taste Q
    beim ausgewählten Musterelement geändert werden (das Element unter dem Cursor ist dabei etwas heller).
  - Der Rastertyp (Z oder S) kann durch Drücken der ALT-Taste am ausgewählten Rasterpunkt geändert werden.

  - Mit dem Mausrad können Sie das Muster nach oben und unten verschieben.
  - Shift + Scrollen: seitliches Verschieben des Musters.
  - Durch Gedrückthalten des Mausrads kann das gesamte Muster verschoben werden
    (funktioniert bei günstigeren Mäusen nicht immer).
  - Ctrl + Scrollen: Vergrößern und Verkleinern.
  - Mit den Pfeiltasten können nur die Musterelemente im Raster bewegt werden.

  - Zum Speichern verwenden Sie die Schaltfläche Speichern oder die Taste F9.
  - Zum Speichern des Musters als Bild verwenden Sie die Schaltfläche Screenshot oder die Taste F10.
    Beim Erstellen eines Screenshots wird nur der sichtbare Bereich gespeichert, die Menüleiste erscheint nicht im Bild.
  - Die Menüleiste kann mit der Taste F11 ausgeblendet werden.
  - Die Löcher im Muster (senkrechte schwarze Balken) können mit der Taste F12 entfernt werden.

  - Die Anzahl der Zeilen und Spalten kann geändert werden, indem Sie den Cursor über den entsprechenden
    (umrahmten) Text bewegen und den gewünschten Wert mit dem Mausrad einstellen.

  - Gespeicherte Muster können jederzeit über den Menüpunkt Öffnen geladen und weiterbearbeitet werden.
  - ACHTUNG! Es gibt keine automatische Speicherung.
  - Nicht gespeicherte Änderungen gehen beim Schließen des Programms oder beim Öffnen eines neuen Musters verloren.

Technische Details:
 - Verwendet Embedded Python Version 3.13.5
 - Das Hauptprogramm wurde mit der Pygame Community Edition erstellt
 - Die Öffnen- und Speichern-Funktionen sind mit Tkinter umgesetzt
 - Zusätzlich wird die NumPy-Bibliothek verwendet

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Para ejecutar el programa, basta con hacer doble clic en el archivo start.bat.
Al iniciar el programa, es completamente normal que aparezca una ventana negra.
En unos segundos, el programa se abrirá.
El programa se inicia automáticamente en modo de pantalla completa.

Control / manejo:
- Los textos con los que se puede interactuar siempre están marcados con un borde.
- En el menú Dibujo:
  - Para seleccionar los elementos del patrón, se pueden usar las teclas 1, 2, 3, 4, 5, 6.
    El programa ajusta automáticamente el elemento del patrón al cuadrado de la cuadrícula más cercano al cursor.
    Para fijar la posición, haga clic con el botón izquierdo del ratón.
  - Para eliminar un elemento del patrón ya colocado, haga clic sobre él con el botón izquierdo del ratón.
  - Para mover un elemento del patrón ya colocado, haga clic sobre él con el botón derecho del ratón,
    y luego haga clic con el botón izquierdo para fijar la nueva posición.

  - El tipo de elemento del patrón (Z o S) se puede cambiar presionando la tecla Q
    en el elemento del patrón seleccionado (el que está bajo el cursor, que aparece ligeramente más claro).
  - El tipo de cuadrícula (Z o S) se puede cambiar presionando la tecla ALT en el punto de la cuadrícula seleccionado.

  - Con la rueda del ratón puede mover el patrón hacia arriba y hacia abajo.
  - Shift + desplazamiento: mover el patrón lateralmente.
  - Manteniendo presionada la rueda del ratón se puede mover todo el patrón
    (puede no funcionar siempre con ratones más económicos).
  - Ctrl + desplazamiento: acercar y alejar.
  - Con las flechas solo se pueden mover los elementos del patrón dentro de la cuadrícula.

  - Para guardar, use el botón Guardar o la tecla F9.
  - Para guardar el patrón como imagen, use el botón Captura de pantalla o la tecla F10.
    Al tomar una captura de pantalla, solo se guarda la parte visible de la pantalla; la barra de menú no aparece en la imagen.
  - La barra de menú se puede ocultar presionando la tecla F11.
  - Los agujeros del patrón (barras negras verticales) se pueden eliminar con la tecla F12.

  - El número de filas y columnas se puede modificar colocando el cursor sobre el texto correspondiente
    (marcado con un borde) y ajustando el valor deseado con la rueda del ratón.

  - Los patrones guardados se pueden cargar y seguir editando en cualquier momento desde el menú Abrir.
  - ¡ADVERTENCIA! No hay guardado automático.
  - Los cambios no guardados se perderán al cerrar el programa o al abrir un nuevo patrón.

Detalles técnicos:
 - Utiliza Embedded Python versión 3.13.5
 - El programa principal fue creado con Pygame Community Edition
 - Las funciones de abrir y guardar están implementadas con Tkinter
 - Además, se utiliza la biblioteca NumPy
