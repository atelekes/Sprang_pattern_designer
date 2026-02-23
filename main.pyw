import pygame, sys, ctypes, math, os, json
import numpy as np
import tkinter as tk
from tkinter import filedialog


class Text:
    def __init__(self, text, x, y, color=(0, 0, 0), size=100, pos='center', border=0, callback=None, surface='screen'):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.pos = pos
        self.border = border
        self.callback = callback
        self.surface = surface

        self.original_color = self.color
        self.font = pygame.font.Font(None, self.size)
        self.surf = self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect(**{str(self.pos): (self.x, self.y)})

        self.hovered_color = (np.clip(self.original_color[0] + 100, 0, 255),
                              np.clip(self.original_color[1] + 100, 0, 255),
                              np.clip(self.original_color[2] + 100, 0, 255))

    def draw(self):
        if self.callback is not None:
            if self.surface == 'screen':
                mouse = mouse_pos
            else:
                mouse = (mouse_pos[0] - w + 165, mouse_pos[1])
            if self.rect.collidepoint(mouse):
                self.color = self.hovered_color
                self.surf = self.font.render(self.text, True, self.color)
                if pressed:
                    self.callback()
            else:
                self.color = self.original_color
                self.surf = self.font.render(self.text, True, self.color)
        if self.surface == 'screen':
            screen.blit(self.surf, self.rect)
            if self.border != 0:
                pygame.draw.rect(screen, self.color,(self.rect.left - 5 - self.border,
                                                     self.rect.top - 5 -self.border,
                                                     self.rect.width + 10 + self.border * 2,
                                                     self.rect.height + 10 + self.border * 2), width=self.border)
        else:
            tool_surf.blit(self.surf, self.rect)
            if self.border != 0:
                pygame.draw.rect(tool_surf, self.color, (self.rect.left - 5 - self.border,
                                                      self.rect.top - 5 - self.border,
                                                      self.rect.width + 10 + self.border * 2,
                                                      self.rect.height + 10 + self.border * 2), width=self.border)

    def update(self, new_text):
        global draw
        self.text = str(new_text)
        self.surf = self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect(**{str(self.pos): (self.x, self.y)})
        self.draw()
        draw = True



class GRect:
    def __init__(self, original_x, original_y, row, column, ser_num, stitch):
        self.original_x = original_x
        self.original_y = original_y
        self.row = row
        self.column = column
        self.ser_num = ser_num
        self.stitch = stitch # True = Z stitch, False = S stitch
        self.x = self.original_x
        self.y = self.original_y
        self.color = (100, 100, 100)
        self.is_highlighted = False
        if ((self.row % 2 == 0 and self.column % 2 == 1 and self.column != 0) or
                (self.row % 2 == 1 and self.column % 2 == 0 and self.column != 0)):
            self.drawer = True
        else:
            self.drawer = False

        if self.column == columns - 1:
            self.isRowText = True
            self.rowFont = pygame.font.Font(None, 20)
            self.rowNum = self.rowFont.render(str(self.row+1), True, self.color)
            self.rowNumRect = self.rowNum.get_rect(midleft=(self.x + bl_width + 5, self.y+(bl_height/2)))
        elif self.column == 0:
            self.isRowText = True
            self.rowFont = pygame.font.Font(None, 20)
            self.rowNum = self.rowFont.render(str(self.row+1), True, self.color)
            self.rowNumRect = self.rowNum.get_rect(midright=(self.x - 5, self.y + (bl_height / 2)))
        else:
            self.isRowText = False

        if self.row == rows - 1:
            self.isColText = True
            self.colFont = pygame.font.Font(None, 20)
            self.colNum = self.colFont.render(str(self.column + 1), True, self.color)
            self.colNumRect = self.colNum.get_rect(midtop=(self.x + (bl_width / 2), self.y + bl_height + 5))
        elif self.row == 0:
            self.isColText = True
            self.colFont = pygame.font.Font(None, 20)
            self.colNum = self.colFont.render(str(self.column + 1), True, self.color)
            self.colNumRect = self.colNum.get_rect(midbottom=(self.x + (bl_width / 2) - bl_border, self.y))
        else:
            self.isColText = False


    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, bl_width, bl_height), width=int(round(bl_border)))
        if self.isRowText and self.row % 5 == 4:
            screen.blit(self.rowNum, self.rowNumRect)
        if self.isColText and self.column % 5 == 4:
            screen.blit(self.colNum, self.colNumRect)

        if self.drawer:
            if self.stitch:
                pygame.draw.line(screen, (0, 0, 0), (self.x - bl_width/2, self.y + bl_height/2),
                                 (self.x + bl_width/2, self.y + bl_height/2), int(round(bl_border*1.5)))
            else:
                screen.blit(S_surf, S_surf.get_rect(center=(self.x, self.y + bl_height/2)))


    def highlight(self, state):
        self.is_highlighted = state
        if state:
            self.color = (200, 200, 200)
            self.draw()
        else:
            self.color = (100, 100, 100)
            self.draw()

    def update(self):
        self.x = self.original_x + x_shift
        self.y = self.original_y + y_shift
        if self.isRowText:
            if self.column == columns - 1:
                self.rowNumRect = self.rowNum.get_rect(midleft=(self.x + bl_width + 5, self.y+(bl_height/2)))
            elif self.column == 0:
                self.rowNumRect = self.rowNum.get_rect(midright=(self.x - 5, self.y + (bl_height / 2)))
        if self.isColText:
            if self.row == rows - 1:
                self.colNumRect = self.colNum.get_rect(midtop=(self.x + (bl_width / 2), self.y + bl_height + 5))
            elif self.row == 0:
                self.colNumRect = self.colNum.get_rect(midbottom=(self.x + (bl_width / 2) - bl_border, self.y))



class Block:
    def __init__(self, color, stitch, ser_num, row = 0, column = 0, hover = True):
        global isHovered
        self.color = color
        self.stitch = stitch # True = Z stitch, False = S stitch
        self.ser_num = ser_num
        self.row = row
        self.column = column
        self.hover = hover
        self.x = 0
        self.y = 0

        if self.color == 'green':
            self.rgb = (164, 205, 57)
            self.width = 3
        elif self.color == 'blue':
            self.rgb = (113, 197, 238)
            self.width = 3
        elif self.color == 'orange':
            self.rgb = (250, 153, 12)
            self.width = 4
        elif self.color == 'pink':
            self.rgb = (217, 104, 166)
            self.width = 2
        elif self.color == 'red':
            self.rgb = (162, 46, 33)
            self.width = 2
        elif self.color == 'purple':
            self.rgb = (178, 154, 200)
            self.width = 2

        self.highlighted_rgb = (np.clip(self.rgb[0]  +20, 0, 255),
                                np.clip(self.rgb[1] + 20, 0, 255),
                                np.clip(self.rgb[2] + 20, 0, 255))
        self.currRGB = self.rgb
        self.rect = pygame.Rect(self.x - self.width * bl_width, self.y, bl_width*self.width, bl_height)

    def draw(self):
        if self.hover:
            self.x, self.y = grid_group[highlighted_ser_num].x, grid_group[highlighted_ser_num].y
        else:
            if rows -1 >= self.row > -1 and columns - 1 >= self.column > -1:
                self.x = grid_group[columns * self.row + self.column].x
                self.y = grid_group[columns * self.row + self.column].y
        if (self.hover or (not self.hover and self.row <= rows -1 and self.column <= columns -1)) and self.row > -1 and self.column > -1:
            self.rect = pygame.Rect(self.x - (self.width - 1) * bl_width + int(round(bl_border)),
                                    self.y + int(round(bl_border)), bl_width*self.width - 2 * int(round(bl_border)),
                                    bl_height - 2 * int(round(bl_border)))
            pygame.draw.rect(screen, self.currRGB, self.rect)
            if self.stitch:
                screen.blit(Z_surf, Z_surf.get_rect(center=self.rect.center))
            else:
                screen.blit(S_surf, S_surf.get_rect(center=self.rect.center))

        if showLines:
            if self.color == 'orange':
                pygame.draw.rect(screen, (0, 0, 0), (self.x - 3 * int(round(bl_border)) - 3 * int(round(bl_width)),
                                    self.y - int(round(bl_height)),6 * int(round(bl_border)), 3 * int(round(bl_height))))
                pygame.draw.rect(screen, (0, 0, 0), (self.x - 3 * int(round(bl_border)) + int(round(bl_width)),
                                    self.y - int(round(bl_height)),6 * int(round(bl_border)), 3 * int(round(bl_height))))
            elif self.color == 'green':
                for b in blocks:
                    if b.row == self.row and b.column == self.column - 3:
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (self.x - 3 * int(round(bl_border)) - 2 * int(round(bl_width)),
                                          self.y - int(round(bl_height)), 6 * int(round(bl_border)),
                                          3 * int(round(bl_height))))

    def update(self):
        global isHovered, stitch_state, draw
        draw_block = True
        if self.hover:
            if pressed:
                self.column = highlighted_column
                self.row = highlighted_row
                self.hover = False
                isHovered = False
                self.draw()
            if keydown == pygame.K_q:
                self.stitch = not self.stitch
                stitch_state = self.stitch
        else:
            if self.rect.collidepoint(mouse_pos):
                self.currRGB = self.highlighted_rgb
                if mouse_buttons[2]:
                    self.hover = True
                    isHovered = True
                elif keydown == pygame.K_q:
                    self.stitch = not self.stitch
                    stitch_state = self.stitch
                elif pressed:
                    blocks.pop(self.ser_num)
                    for b in blocks:
                        if b.ser_num > self.ser_num:
                            b.ser_num -= 1
                    draw_block = False
                    draw = True
            else:
                self.currRGB = self.rgb
        if draw_block:
            self.draw()

    def save_data(self):
        return {
            'color': self.color,
            'stitch': self.stitch,
            'row': self.row,
            'column': self.column,
        }



def generate_grid():
    grid_group.clear()
    for r in range(rows):
        for c in range(columns):
            if (r, c) in S_stitches:
                grid_group.append(GRect(c * int(math.floor(bl_width)), r * int(math.floor(bl_height)),
                                        r, c, r * columns + c, False))
            else:
                grid_group.append(GRect(c*int(math.floor(bl_width)), r*int(math.floor(bl_height)),
                                        r, c, r*columns+c, True))
    update_blocks()


def resize_grid():
    global S_font, S_surf, Z_surf
    for g in grid_group:
        g.original_x = g.column*int(math.floor(bl_width))
        g.original_y = g.row*int(math.floor(bl_height))
    redraw()
    S_font = pygame.font.Font(None, int(round(bl_height)))
    S_surf = S_font.render('S', True, (0, 0, 0))
    Z_surf = S_font.render('Z', True, (0, 0, 0))


def highlight(pos):
    global highlighted_ser_num, prev_highlighted_ser_num, isHighlighted, highlighted_column, highlighted_row, \
        highlighted_column, prev_highlighted_row, prev_highlighted_column
    if (pygame.Rect(x_shift, y_shift, columns * int(math.floor(bl_width)), rows * int(math.floor(bl_height))).
            collidepoint(pos)):
        isHighlighted = True
        prev_highlighted_row = highlighted_row
        prev_highlighted_column = highlighted_column
        highlighted_row = math.floor((pos[1] - y_shift) / int(math.floor(bl_height)))
        highlighted_column = math.floor((pos[0] - x_shift) / int(math.floor(bl_width)))

        highlighted_ser_num = highlighted_row * columns + highlighted_column
        if highlighted_ser_num != prev_highlighted_ser_num:
            grid_group[highlighted_ser_num].highlight(True)
            grid_group[prev_highlighted_ser_num].highlight(False)
            prev_highlighted_ser_num = highlighted_ser_num
    else:
        isHighlighted = False
        prev_highlighted_ser_num = columns + 2
        grid_group[highlighted_ser_num].highlight(False)
        highlighted_ser_num = columns + 2


def redraw():
    global draw
    screen.fill(BG_color)
    for g in grid_group:
        g.update()
        g.draw()
    draw = True


def add_block(color):
    global isHovered
    if not isHovered:
        blocks.append(Block(color, stitch_state, len(blocks)))
        isHovered = True


def update_blocks():
    for b in blocks:
        b.update()


def hun_button():
    global language, scene, draw
    language = 'hun'
    scene = 'select'
    create.update('Új létrehozása')
    load.update('Megnyitás')
    save.update('Mentés (F9)')
    screenshot.update('Képernyőkép (F10)')
    back.update('Vissza')
    backDraw.update('Vissza')
    rowsText.update(str('Sorok: ' + str(rows)))
    columnsText.update(str('Oszlopok: ' + str(columns)))
    continueText.update('Jelenlegi projekt folytatása')
    sidebar_text.update('Menüsáv megjelenítése/eltüntetése (F11)')
    line_text.update('Lyukak megjelenítése/eltüntetése (F12)')
    draw = True


def en_button():
    global language, scene, draw
    language = 'en'
    scene = 'select'
    create.update('Crete new')
    load.update('Load')
    save.update('Save (F9)')
    screenshot.update('Screenshot (F10)')
    back.update('Back')
    backDraw.update('Back')
    rowsText.update(str('Rows: ' + str(rows)))
    columnsText.update(str('Columns: ' + str(columns)))
    continueText.update(str('Continue current project'))
    sidebar_text.update('Show/Hide sidebar (F11)')
    line_text.update('Show/Hide wholes (F12)')
    draw = True


def create_new_button():
    global scene, generate, draw, blocks, isOpenedProject, bl_width, bl_height, bl_border, rows, columns, x_shift, y_shift
    blocks.clear()
    S_stitches.clear()
    scene = 'draw'
    bl_width = 35
    bl_height = 50
    bl_border = 3

    rows = 17
    columns = 36
    x_shift = 0
    y_shift = 0
    generate = True
    isOpenedProject = True


def load_button():
    global scene, draw
    scene = 'load'
    draw = True


def back_button():
    global scene, draw
    if scene == 'draw':
        scene = 'select'
    elif scene == 'select':
        scene = 'lang'
    draw = True


def save_button():
    global draw, scene
    scene = 'save'
    draw = True


def screenshot_button():
    global showLines
    redraw()
    showLines = True
    update_blocks()
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        initialdir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'saves'),
        title="Screenshot",
        defaultextension=".png",
        initialfile=loaded_name[:-5],
        filetypes=[
            ("PNG", "*.png"),
            ("Minden fájl", "*.*")
        ]
)
    if file_path:
        pygame.image.save(screen, file_path)
    root.destroy()


def continue_button():
    global draw, scene
    scene = 'draw'
    draw = True

path = os.path.dirname(__file__)
scene = 'lang'
language = None
tool_surf = pygame.Surface((165, 255))
loaded_name = ''

bl_width = 35
bl_height = 50
bl_border = 3
rows = 17
columns = 36
x_shift = 0
y_shift = 0
w, h = (1366, 698)
BG_color = (255, 255, 255)

highlighted_ser_num = 0
prev_highlighted_ser_num = 0
highlighted_row = 0
highlighted_column = 0
prev_highlighted_row = 0
prev_highlighted_column = 0

prevRows = rows
prevColumns = columns

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
pygame.display.set_caption("Sprang designer 2.0")

hwnd = pygame.display.get_wm_info()["window"]
SW_MAXIMIZE = 3
ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
w, h = pygame.display.get_window_size()

grid_group = []
S_stitches = []
blocks = []
pan = []
lines = []

running = True
generate = False
draw = False
isPressed = False
pressed = False
isHovered = False
stitch_state = True
showTools = True
wheelButton = False
prevWheelButton = False
isOpenedProject = False
isHighlighted = False
showBlockTip = False
showLines = True

block_font = pygame.font.Font(None, 25)
block_surf = block_font.render(str("     "
                               "1               "
                               "2                "
                               "3               "
                               "4           "
                               "5           "
                               "6"), True, (0, 0, 0))
S_font = pygame.font.Font(None, int(round(bl_height)))
S_surf = S_font.render('S', True, (0, 0, 0))
Z_surf = S_font.render('Z', True, (0, 0, 0))

hun = Text("Magyar", w/2-300, h/2, (0, 0, 0), 100, 'center', 10, hun_button)
en = Text("English", w/2+300, h/2, (0, 0, 0), 100, 'center', 10, en_button)

create = Text("Create new", w/2, h/2-60, (0, 0, 0), 100, 'center', 10, create_new_button)
load = Text("Load", w/2, h/2+60, (0, 0, 0), 100, 'center', 10, load_button)

back = Text('Back', w-10, 10, (0, 0, 0), 50, 'topright', 5, back_button)
backDraw = Text('Back', 155, 10, (0, 0, 0), 25, 'topright', 2, back_button, surface='tool_surf')
save = Text('Save', 155, 45,  (0, 0, 0), 25, 'topright', 2, save_button, surface='tool_surf')
screenshot = Text('Screenshot', 155, 80,  (0, 0, 0), 25, 'topright', 2, screenshot_button, surface='tool_surf')

rowsText = Text(str('Rows: ' + str(rows)), 155, 115, (0, 0, 0), 25, 'topright', 2, surface='tool_surf')
columnsText = Text(str('Columns: ' + str(columns)), 155, 150, (0, 0, 0), 25, 'topright', 2, surface='tool_surf')

currRow = Text(str('row: ' + str(highlighted_row)), 155, 185, (0, 0, 0), 25, 'topright', surface='tool_surf')
currCol = Text(str('column: ' + str(highlighted_column)), 155, 220, (0, 0, 0), 25, 'topright', surface='tool_surf')

continueText = Text('Continue current project', w/2, h/2 - 180, (0, 0, 0), 100, 'center', 10, continue_button)

sidebar_text = Text('Show/Hide sidebar (F11)', 436, h-3, (0, 0, 0), 25, 'bottomleft')
line_text = Text('Show/Hide wholes (F12)', 800, h-3, (0, 0, 0), 25, 'bottomleft')


while running:
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    mouse_buttons = pygame.mouse.get_pressed()
    keydown = None
    if mouse_buttons[0] and not isPressed:
        pressed = True
        isPressed = True
    else:
        pressed = False
    if mouse_buttons[1] and not prevWheelButton:
        wheelButton = True
        prevWheelButton = True
        pan = [mouse_pos, x_shift, y_shift]
    else:
        wheelButton = False

    if mouse_buttons[1]:
        x_shift = (mouse_pos[0] - pan[0][0]) + pan[1]
        y_shift = (mouse_pos[1] - pan[0][1]) + pan[2]
        draw = True

    if not mouse_buttons[0]:
        isPressed = False
    if not mouse_buttons[1]:
        prevWheelButton = False


    if generate:
        generate_grid()
        generate = False
        draw = True

    if draw:
        screen.fill(BG_color)
        tool_surf.fill(BG_color)
        if scene == 'draw':
            redraw()
        draw = False
        showBlockTip = True


    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            w, h = pygame.display.get_window_size()
            redraw()

        elif event.type == pygame.MOUSEWHEEL and scene == 'draw':
            text_mouse = (mouse_pos[0] - w + 165, mouse_pos[1])
            if rowsText.rect.collidepoint(text_mouse) and showTools:
                rows = np.clip(rows + event.y * 2, 4, 100000)
            elif columnsText.rect.collidepoint(text_mouse) and showTools:
                columns = np.clip(columns + event.y * 2, 4, 1000)
            elif keys[pygame.K_LSHIFT]:
                x_shift += event.y * 20
                if scene == 'draw':
                    redraw()
            elif keys[pygame.K_LCTRL]:
                if event.y == -1:
                    bl_width *= 0.95
                    bl_height *= 0.95
                    bl_border *= 0.95
                    resize_grid()
                else:
                    bl_width /= 0.95
                    bl_height /= 0.95
                    bl_border /= 0.95
                    resize_grid()
            else:
                y_shift += event.y * 20
                redraw()

        elif event.type == pygame.KEYDOWN:
            keydown = event.key
            if scene == 'draw':
                if keydown == pygame.K_F10:
                    screenshot_button()
                elif keydown == pygame.K_F9:
                    scene = 'save'
                elif keydown == pygame.K_UP:
                    for b in blocks:
                        b.row -= 1
                        draw = True
                elif keydown == pygame.K_DOWN:
                    for b in blocks:
                        b.row += 1
                        draw = True
                elif keydown == pygame.K_LEFT:
                    for b in blocks:
                        b.column -= 1
                        draw = True
                elif keydown == pygame.K_RIGHT:
                    for b in blocks:
                        b.column += 1
                        draw = True
                elif keydown == pygame.K_F12:
                    showLines = not showLines
                    draw = True

                if isHighlighted:
                    if event.key == pygame.K_LALT:
                        if grid_group[highlighted_ser_num].drawer:
                            if grid_group[highlighted_ser_num].stitch:
                                S_stitches.append((grid_group[highlighted_ser_num].row, grid_group[highlighted_ser_num].column))
                            else:
                                S_stitches.remove((grid_group[highlighted_ser_num].row, grid_group[highlighted_ser_num].column))
                            grid_group[highlighted_ser_num].stitch = not grid_group[highlighted_ser_num].stitch
                        else:
                            if grid_group[highlighted_ser_num+1].stitch:
                                S_stitches.append((grid_group[highlighted_ser_num + 1].row, grid_group[highlighted_ser_num + 1].column))
                            else:
                                S_stitches.remove((grid_group[highlighted_ser_num + 1].row, grid_group[highlighted_ser_num + 1].column))
                            grid_group[highlighted_ser_num+1].stitch = not grid_group[highlighted_ser_num+1].stitch
                        redraw()

                    elif event.key == pygame.K_1:
                        add_block('blue')
                    elif event.key == pygame.K_2:
                        add_block('green')
                    elif event.key == pygame.K_3:
                        add_block('orange')
                    elif event.key == pygame.K_4:
                        add_block('pink')
                    elif event.key == pygame.K_5:
                        add_block('red')
                    elif event.key == pygame.K_6:
                        add_block('purple')


    if scene == 'lang':
        hun.draw()
        en.draw()

    elif scene == 'select':
        create.draw()
        load.draw()
        back.draw()
        if isOpenedProject:
            continueText.draw()

    elif scene == 'draw':
        backDraw.draw()
        highlight(mouse_pos)
        if language == 'hun':
            if prev_highlighted_row != highlighted_row:
                currRow.update(str('sor: ' + str(highlighted_row + 1)))
            if prev_highlighted_column != highlighted_column:
                currCol.update(str('oszlop: ' + str(highlighted_column + 1)))
            if prevRows != rows:
                rowsText.update(str('Sorok: ' + str(rows)))
                prevRows = rows
                generate = True
            if prevColumns != columns:
                columnsText.update(str('Oszlopok: ' + str(columns)))
                prevColumns = columns
                generate = True
        else:
            if prev_highlighted_row != highlighted_row:
                currRow.update(str('row: ' + str(highlighted_row + 1)))
            if prev_highlighted_column != highlighted_column:
                currCol.update(str('column: ' + str(highlighted_column + 1)))
            if prevRows != rows:
                rowsText.update(str('Rows: ' + str(rows)))
                prevRows = rows
                generate = True
            if prevColumns != columns:
                columnsText.update(str('Columns: ' + str(columns)))
                prevColumns = columns
                generate = True
        currCol.draw()
        currRow.draw()
        columnsText.draw()
        rowsText.draw()
        save.draw()
        screenshot.draw()

        update_blocks()

        if keydown == pygame.K_F11:
            showTools = not showTools
            draw = True
        if showTools:
            screen.blit(tool_surf, tool_surf.get_rect(topright=(w, 0)))
            if showBlockTip:
                pygame.draw.rect(screen, BG_color, (0, h-31, w, 31))
                pygame.draw.rect(screen, (164, 205, 57), (3, h - 28, 52, 25))
                pygame.draw.rect(screen, (113, 197, 238), (86, h - 28, 52, 25))
                pygame.draw.rect(screen, (250, 153, 12), (167, h - 28, 70, 25))
                pygame.draw.rect(screen, (217, 104, 166), (267, h - 28, 35, 25))
                pygame.draw.rect(screen, (162, 46, 33), (332, h - 28, 35, 25))
                pygame.draw.rect(screen, (178, 154, 200), (397, h - 28, 35, 25))
                screen.blit(block_surf, block_surf.get_rect(bottomleft=(0, h-3)))
                showBlockTip = False
                sidebar_text.draw()
                line_text.draw()
    elif scene == 'save':
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            initialdir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                    'saves'),
            title="Save",
            defaultextension=".json",
            initialfile=loaded_name,
            filetypes=[
                ("JSON", "*.json"),
            ]
        )
        if file_path:
            save_datas = {}
            block_datas = []
            for b in blocks:
                block_datas.append(b.save_data())
            save_datas = {
                'verification': 'sprang_sample_V2',
                'rows': int(rows),
                'columns': int(columns),
                's_stitches': S_stitches,
                'blocks': block_datas,
            }
            with open(file_path, 'w') as save_file:
                json.dump(save_datas, save_file, indent=4)
        root.destroy()
        scene = 'draw'

    elif scene == 'load':
        blocks.clear()
        S_stitches.clear()
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            initialdir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'saves'),
            title="Open",
            defaultextension=".json",
            filetypes=[
                ("JSON", "*.json"),
            ]
        )
        if file_path:
            loaded_name = os.path.basename(file_path)
            with open(file_path, 'r') as opened:
                data = json.load(opened)
                if data['verification'] == 'sprang_sample_V2':
                    rows = data['rows']
                    columns = data['columns']
                    for s in data['s_stitches']:
                        S_stitches.append((s[0], s[1]))
                    for b in data['blocks']:
                        blocks.append(Block(b['color'], b['stitch'], len(blocks), b['row'], b['column'], False))
            root.destroy()
        isOpenedProject = True
        generate = True
        scene = 'draw'
    clock.tick(30)
    pygame.display.update()
pygame.quit()
pygame.mixer.quit()
sys.exit()
