!WARNING!
The program only works on Windows 10 and Windows 11 operating systems.

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
