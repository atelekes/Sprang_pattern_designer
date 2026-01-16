import pygame
import sys
import ctypes
import json
import os
import tkinter as tk
from tkinter import filedialog

class Text:
    def __init__(self, text, x, y, color=(0, 0, 0), size=100, pos='center', border=0, static=True):
        self.rect = None
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.border = border
        self.static = static
        self.pos = pos
        self.font = pygame.font.Font(None, self.size)
        self.state = False
        self.surf = None
        self.original_color = self.color
        self.hover = False
        self.generated = False

    def draw(self):
        if not self.generated and self.static:
            self.surf = self.font.render(str(self.text), True, self.color)
            if self.pos == 'center':
                self.rect = self.surf.get_rect(center=(self.x, self.y))
            elif self.pos == 'topleft':
                self.rect = self.surf.get_rect(topleft=(self.x, self.y))
            elif self.pos == 'midleft':
                self.rect = self.surf.get_rect(midleft=(self.x, self.y))
            elif self.pos == 'bottomleft':
                self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))
            elif self.pos == 'midbottom':
                self.rect = self.surf.get_rect(midbottom=(self.x, self.y))
            elif self.pos == 'bottomright':
                self.rect = self.surf.get_rect(bottomright=(self.x, self.y))
            elif self.pos == 'midright':
                self.rect = self.surf.get_rect(midright=(self.x, self.y))
            elif self.pos == 'topright':
                self.rect = self.surf.get_rect(topright=(self.x, self.y))
            elif self.pos == 'midtop':
                self.rect = self.surf.get_rect(midtop=(self.x, self.y))
        elif not self.static:
            self.surf = self.font.render(str(self.text), True, self.color)
            if self.pos == 'center':
                self.rect = self.surf.get_rect(center=(self.x, self.y))
            elif self.pos == 'topleft':
                self.rect = self.surf.get_rect(topleft=(self.x, self.y))
            elif self.pos == 'midleft':
                self.rect = self.surf.get_rect(midleft=(self.x, self.y))
            elif self.pos == 'bottomleft':
                self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))
            elif self.pos == 'midbottom':
                self.rect = self.surf.get_rect(midbottom=(self.x, self.y))
            elif self.pos == 'bottomright':
                self.rect = self.surf.get_rect(bottomright=(self.x, self.y))
            elif self.pos == 'midright':
                self.rect = self.surf.get_rect(midright=(self.x, self.y))
            elif self.pos == 'topright':
                self.rect = self.surf.get_rect(topright=(self.x, self.y))
            elif self.pos == 'midtop':
                self.rect = self.surf.get_rect(midtop=(self.x, self.y))
        screen.blit(self.surf, self.rect)
        if self.border != 0:
            pygame.draw.rect(screen, self.color, self.rect.inflate(10 + self.border, 10 + self.border), width=self.border)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

    def button(self):
        self.draw()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = (200, 200, 200)
            self.draw()
        else:
            self.color = self.original_color
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.state == False:
            self.state = pygame.mouse.get_pressed()[0]
            return True
        else:
            self.state = pygame.mouse.get_pressed()[0]
            return False



class Block:
    global columns, rows, block_width, block_height, line_width, h_shift, v_shift, nums
    def __init__(self, x, y, status, row, column, ser_num):
        self.x = x
        self.y = y
        self.status = status
        self.row = row
        self.column = column
        self.ser_num = ser_num
        self.color = (80, 80, 80)
        self.rect = None
        self.collide = False

    def change(self, draw=False):
        self.x = w/2- columns /2*block_width+(self.ser_num % columns)*block_width + h_shift
        self.y = 50+(self.ser_num // columns)*block_height + v_shift
        self.rect = pygame.Rect(self.x, self.y, block_width, block_height)
        if self.row == 0 and not draw:
            nums[self.column].x = self.x+block_width/8
            nums[self.column].y = self.y-5
    def draw(self):
        if self.rect.colliderect(screen.get_rect()):
            pygame.draw.rect(screen, self.color, self.rect, 2)
            if self.row % 2 == 0 and self.column % 2 == 0:
                pygame.draw.line(screen, (0,0,0), self.rect.center,
                                 (self.rect.center[0] + block_width, self.rect.center[1]), int(round(line_width)))
            elif self.row % 2 == 1 and self.column % 2 == 1 and self.column != columns-1:
                pygame.draw.line(screen, (0, 0, 0), self.rect.center,
                                 (self.rect.center[0] + block_width, self.rect.center[1]), int(round(line_width)))

            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.color = (230, 230, 230)
                self.collide = True
            else:
                self.color = (80, 80, 80)
                self.collide = False

class Marks:
    global block_width, block_height, line_width, blocks, active_hover
    def __init__(self, x, y, color_text, ser_num, hover = False, static=False, block_row=0, block_column=0):
        self.x = x
        self.y = y
        self.color_text = color_text
        self.static = static
        self.ser_num = ser_num
        self.hover = hover
        self.rect = pygame.Rect(self.x, self.y, block_width*3, block_height)
        self.collide = False
        self.color = None
        self.wait = False
        self.block_row = block_row
        self.block_column = block_column

        if color_text == 'blue':
            self.color = (99, 229, 255)
        elif color_text == 'green':
            self.color = (146, 208, 80)
        elif color_text == 'orange':
            self.color = (250, 156, 28)

    def draw(self):
        global active_hover, greens, blues, oranges
        screen_rect = screen.get_rect()
        if self.static:
            if self.color_text == 'orange':
                self.rect = pygame.Rect(self.x, self.y, 100, 50)
                pygame.draw.rect(screen, self.color, self.rect)
                pygame.draw.line(screen, (0, 0, 0), (self.rect.midleft[0] + 25 / 2, self.rect.midleft[1]),
                                 (self.rect.midright[0] - 25 / 2, self.rect.midright[1]), 5)
            else:
                self.rect = pygame.Rect(self.x, self.y, 75, 50)
                pygame.draw.rect(screen, self.color, self.rect)
                pygame.draw.line(screen, (0, 0, 0), (self.rect.midleft[0] + 25 / 2, self.rect.midleft[1]),
                                 (self.rect.midright[0] - 25 / 2, self.rect.midright[1]), 5)
        else:
            if self.hover:
                for bl in blocks:
                    if bl.collide:
                        self.x = bl.rect.topleft[0]
                        self.y = bl.rect.topleft[1]
                        self.block_row = bl.row
                        self.block_column = bl.column
                if pygame.mouse.get_pressed()[0]:
                    self.hover = False
                    active_hover = False
                    self.wait = True
            else:
                try:
                    self.x = blocks[self.block_row * columns + self.block_column].rect.topleft[0]
                    self.y = blocks[self.block_row * columns + self.block_column].rect.topleft[1]
                except:
                    pass

            if self.color_text == 'orange':
                self.rect = pygame.Rect(self.x, self.y, block_width * 4, block_height)
                if self.rect.colliderect(screen_rect):
                    pygame.draw.rect(screen, self.color, self.rect)
                    pygame.draw.line(screen, (0, 0, 0), (self.rect.midleft[0] + block_width / 2, self.rect.midleft[1]),
                                     (self.rect.midright[0] - block_width / 2, self.rect.midright[1]),
                                     int(round(line_width)))
            else:
                self.rect = pygame.Rect(self.x, self.y, block_width * 3, block_height)
                if self.rect.colliderect(screen_rect):
                    pygame.draw.rect(screen, self.color, self.rect)
                    pygame.draw.line(screen, (0, 0, 0), (self.rect.midleft[0]+block_width/2, self.rect.midleft[1]),
                                     (self.rect.midright[0]-block_width/2, self.rect.midright[1]), int(round(line_width)))
            if self.rect.colliderect(screen_rect):
                if not self.wait:
                    if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.hover:
                        if self.color_text == 'blue':
                            blues.pop(self.ser_num)
                            for blu_ in blues:
                                if blu_.ser_num > self.ser_num:
                                    blu_.ser_num -= 1
                        elif self.color_text == 'green':
                            greens.pop(self.ser_num)
                            for gre_ in greens:
                                if gre_.ser_num > self.ser_num:
                                    gre_.ser_num -= 1
                        elif self.color_text == 'orange':
                            oranges.pop(self.ser_num)
                            for ora in oranges:
                                if ora.ser_num > self.ser_num:
                                    ora.ser_num -= 1
                    elif (self.rect.collidepoint(pygame.mouse.get_pos()) and
                          pygame.mouse.get_pressed()[2] and not self.hover):
                        self.hover = True
                        active_hover = True


            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.color = True
                if self.color_text == 'blue':
                    self.color = (119, 249, 255)
                elif self.color_text == 'green':
                    self.color = (166, 228, 100)
                else:
                    self.color = (255, 176, 48)
            else:
                if self.color_text == 'blue':
                    self.color = (99, 229, 255)
                elif self.color_text == 'green':
                    self.color = (146, 208, 80)
                else:
                    self.color = (250, 156, 28)
            if self.wait and not self.rect.collidepoint(pygame.mouse.get_pos()):
                self.wait = False


    def button(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def saving_data(self):
        return {
            'color': self.color_text,
            'block_row': self.block_row,
            'block_column': self.block_column,
        }


def block_draw(row, column):
    blocks.clear()
    nums.clear()
    for i in range(row*column):
        blocks.append(Block(w/2-column/2*block_width+(i % column)*block_width + h_shift,
                            50+(i // column)*block_height + v_shift, 'none', i//column, i%column, len(blocks)))

    for bl in blocks:
        bl.change(True)
        if bl.row == 0:
            nums.append(Text(bl.column+1, bl.x+block_width/8, bl.y-5, (0,0,0), int(round(block_width)), 'bottomleft'))

def change_box():
    global columns, rows, v_shift, h_shift, blocks, block_width, block_height
    for blo in blocks:
        blo.change()



w, h = (1366, 698)
BG_color = (255, 236, 197)
block_width = 25
block_height = 50
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

hwnd = pygame.display.get_wm_info()["window"]
SW_MAXIMIZE = 3
ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)



lang = None
state = 'language'
running = True
blocks = []
rows = 15
columns = 28
h_shift = 0
v_shift = 0
line_width = 5
active_hover = False
path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'saves')
save_name = ''
nums = []
verific_blues = []
verific_greens = []
verific_oranges = []

pygame.display.set_caption("Sprang")
w,h = screen.get_size()
hun = Text('Magyar', w/2-200, h/2, (0,0,0), 100, 'center', 10)
eng = Text('English', w/2+200, h/2, (0,0,0), 100, 'center', 10)
back = Text('Back', w-10, 10, (0,0,0), 50, 'topright', 5)
create = Text('Create new', 10, 10, (0,0,0), 50, 'topleft', 5)
load = Text('Open', 10, 60, (0,0,0), 50, 'topleft', 5)
row_text = Text(str('Rows: ' + str(rows)), 10, 10, (0,0,0), 50, 'topleft', 5, False)
column_text = Text(str('Columns: ' + str(columns)), 10, 60, (0,0,0), 50, 'topleft', 5, False)
save = Text('Save', w-10, 70, (0,0,0), 50, 'topright', 5)
save_text = Text('Saving name (press enter to save)', w/2, h/2-100, (0,0,0), 50, 'center')
save_name_text = Text(save_name, w/2, h/2+100, (0,0,0), 50, 'center')

blue = Marks(10, 120, 'blue', None, False, True)
blue_num = Text('1', blue.rect.midright[0]+10, blue.rect.midright[1], (0,0,0), 50, 'midleft')
green = Marks(10, blue.rect.bottom + 10, 'green', None, False, True)
green_num = Text('2', green.rect.midright[0]+10, green.rect.midright[1], (0,0,0), 50, 'midleft')
orange = Marks(10, green.rect.bottom + 10, 'orange', None, False, True)
orange_num = Text('3', orange.rect.midright[0]+35, orange.rect.midright[1], (0,0,0), 50, 'midleft')

blues = []
greens = []
oranges = []
saving_blues = []
saving_greens = []
saving_oranges = []


while running:
    w,h = screen.get_size()
    screen.fill(BG_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            block_draw(rows, columns)
        elif event.type == pygame.MOUSEWHEEL and state == 'draw':
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                if event.y == -1:
                    block_width *= 0.95
                    block_height *= 0.95
                    line_width *= 0.95
                    change_box()
                else:
                    block_width /= 0.95
                    block_height /= 0.95
                    line_width /= 0.95
                    change_box()
            elif pygame.key.get_pressed()[pygame.K_LSHIFT]:
                h_shift += event.y * 20
                change_box()
            elif row_text.hover:
                rows += event.y
                block_draw(rows, columns)
                if lang == 'hun':
                    row_text.text = str('Sorok: ' + str(rows))
                else:
                    row_text.text = str('Rows: ' + str(rows))
            elif column_text.hover:
                columns += event.y*4
                block_draw(rows, columns)
                if lang == 'hun':
                    column_text.text = str('Oszlopok: ' + str(columns))
                else:
                    column_text.text = str('Columns: ' + str(columns))
            else:
                v_shift += event.y * 20
                change_box()

        elif event.type == pygame.KEYUP and state == 'draw':
            spec_key = pygame.key.name(event.key)
            if spec_key == 'up':
                for b in blues:
                    b.block_row -= 1
                for g in greens:
                    g.block_row -= 1
                for o in oranges:
                    o.block_row -= 1
            elif spec_key == 'down':
                for b in blues:
                    b.block_row += 1
                for g in greens:
                    g.block_row += 1
                for o in oranges:
                    o.block_row += 1
            elif spec_key == 'right':
                for b in blues:
                    b.block_column += 1
                for g in greens:
                    g.block_column += 1
                for o in oranges:
                    o.block_column += 1
            elif spec_key == 'left':
                for b in blues:
                    b.block_column -= 1
                for g in greens:
                    g.block_column -= 1
                for o in oranges:
                    o.block_column -= 1

    if state == 'language':
        if hun.button():
            state = 'selector'
            lang = 'hun'
            back.text = 'Vissza'
            create.text = 'Új létrehozása'
            load.text = 'Megnyitás'
            save.text = 'Mentés'
            save_text.text = 'Milyen néven mentse el? (nyomjon entert a mentéshez)'
        if eng.button():
            state = 'selector'
            lang = 'eng'
            back.text = 'Back'
            create.text = 'Create new'
            load.text = 'Open'
            save.text = 'Save'
            save_text.text = 'Save name (press enter to save)'
    elif state == 'selector':
        if back.button():
            state = 'language'
        if create.button():
            state = 'draw'
            blues.clear()
            greens.clear()
            oranges.clear()
        if load.button():
            blues.clear()
            greens.clear()
            oranges.clear()
            verific_blues.clear()
            verific_greens.clear()
            verific_oranges.clear()
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                initialdir=path,
                title="Minta megnyitása",
                filetypes=(("JSON fájlok", "*.json"), ("Minden fájl", "*.*"))
            )
            root.destroy()
            if file_path:
                with open(file_path, 'r') as opened:
                    data = json.load(opened)
                    if data['verification'] == 'sprang_sample':
                        rows = data['rows']
                        columns = data['columns']
                        for b in data['blues']:
                            if (b['block_row'], b['block_column']) not in verific_blues:
                                blues.append(Marks(0, 0, b['color'], len(blues),
                                                   False, False, b['block_row'], b['block_column']))
                                verific_blues.append((b['block_row'], b['block_column']))
                        for g in data['greens']:
                            if (g['block_row'], g['block_column']) not in verific_greens:
                                greens.append(Marks(0, 0, g['color'], len(greens),
                                                   False, False, g['block_row'], g['block_column']))
                                verific_greens.append((g['block_row'], g['block_column']))
                        for o in data['oranges']:
                            if (o['block_row'], o['block_column']) not in verific_oranges:
                                oranges.append(Marks(0, 0, o['color'], len(oranges),
                                                   False, False, o['block_row'], o['block_column']))
                                verific_oranges.append((o['block_row'], o['block_column']))
            state = 'draw'
            block_draw(rows, columns)
    elif state == 'draw':
        if back.button():
            state = 'selector'
        if len(blocks) == 0:
            block_draw(rows, columns)
        for b in blocks:
            b.draw()
        row_text.draw()
        column_text.draw()
        green.draw()
        blue.draw()
        blue_num.draw()
        green_num.draw()
        orange.draw()
        orange_num.draw()

        if blue.button() or pygame.key.get_pressed()[pygame.K_1] and not active_hover:
            blues.append(Marks(blue.rect.topleft[0], blue.rect.topleft[1], 'blue', len(blues), hover=True))
            active_hover = True
        for blu in blues:
            blu.draw()
        if green.button() or pygame.key.get_pressed()[pygame.K_2] and not active_hover:
            greens.append(Marks(green.rect.topleft[0], green.rect.topleft[1], 'green', len(greens), hover=True))
            active_hover = True
        for gre in greens:
            gre.draw()
        if orange.button() or pygame.key.get_pressed()[pygame.K_3] and not active_hover:
            oranges.append(Marks(orange.rect.topleft[0], orange.rect.topleft[1], 'orange', len(oranges), hover=True))
            active_hover = True
        for o in oranges:
            o.draw()

        if save.button():
            state = 'save'
            save_name = save_name[:-5]
        for n in nums:
            n.draw()



    elif state == 'save':
        save_path = filedialog.asksaveasfilename(
            initialdir=path,
            title="JSON fájl mentése",
            defaultextension=".json",
            filetypes=[
                ("JSON fájl", "*.json")
            ]
        )
        if save_path:
            saving_blues.clear()
            saving_greens.clear()
            saving_oranges.clear()
            save_data = {}
            for b2 in blues:
                saving_blues.append(b2.saving_data())
            for g2 in greens:
                saving_greens.append(g2.saving_data())
            for o2 in oranges:
                saving_oranges.append(o2.saving_data())
            save_data = {
                'verification': 'sprang_sample',
                'rows': rows,
                'columns': columns,
                'blues': saving_blues,
                'greens': saving_greens,
                'oranges': saving_oranges,
            }
            with open(save_path, 'w') as save_file:
                json.dump(save_data, save_file, indent=4)
        state = 'draw'


    clock.tick(24)
    pygame.display.update()
