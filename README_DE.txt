!ACHTUNG!
Das Programm funktioniert nur unter den Betriebssystemen Windows 10 und Windows 11.

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