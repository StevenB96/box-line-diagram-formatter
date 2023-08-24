import tkinter as tk
from random import randint

class NumberedCanvas(tk.Canvas):
    def __init__(self, parent, grid_spacing, items, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.items = items
        self.grid_spacing = grid_spacing
        self.font = ('Arial', 10)
        self.line_colour = '#a3aeba'
        self.draw_grid()
        self.bind('<Configure>', self.resize_grid)

    def draw_grid(self):
        # delete previous grid lines and labels
        self.delete('gridline', 'rowlabel', 'collabel')

        # draw horizontal lines and row labels
        for y in range(0, self.winfo_height(), self.grid_spacing):
            self.create_line(0, y, self.winfo_width(), y, fill=self.line_colour, tags='gridline', width=1 if (y % (10 * self.grid_spacing) == 0) == 0 else 2)
            if (y % (10 * self.grid_spacing) == 0):
                self.create_text(
                    5, 
                    y+5, 
                    anchor='w', 
                    text=str(y), 
                    font=self.font, tags='rowlabel')

        # draw vertical lines and column labels
        for x in range(0, self.winfo_width(), self.grid_spacing):
            self.create_line(x, 0, x, self.winfo_height(), fill=self.line_colour, tags='gridline', width=1 if (x % (10 * self.grid_spacing) == 0) == 0 else 2)
            if (x % (10 * self.grid_spacing) == 0):
                self.create_text(
                    x+5, 
                    5, 
                    anchor='nw', 
                    text=str(x), 
                    font=self.font, 
                    tags='collabel')

        # draw item lines
        for i, item in enumerate(self.items):
            for j, line in enumerate(item.line_set()):
                color = f'#{randint(0,255):02x}{randint(0,255):02x}{randint(0,255):02x}'
                self.create_line(line[0][0], line[0][1],
                                   line[1][0], line[1][1],
                                   fill=color,
                                   width=4,
                                   tags=(f'line{i}{j}'))
                self.create_text(
                    line[0][0] + 5,
                    line[0][1] + 5,
                    anchor='nw',
                    text=item.id()[-1],
                    tags='collabel')

    def resize_grid(self, event):
        self.draw_grid()