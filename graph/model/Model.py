import tkinter as tk
from random import randint

class Model:
    def __init__(self, connections, entities, grid_spacing):
        self.connections = connections
        self.entities = entities
        self.grid_spacing = grid_spacing

    def display(self):
        items = self.connections + self.entities
        root = tk.Tk()
        canvas = tk.Canvas(root, width=4000, height=4000, bg='white')
        canvas.pack()
        for i, item in enumerate(items):
            for j, line in enumerate(item.line_set()):
                color = f'#{randint(0,255):02x}{randint(0,255):02x}{randint(0,255):02x}'
                canvas.create_line(line[0][0], line[0][1],
                        line[1][0], line[1][1],
                        fill=color,
                        width=4,
                        tags=(f'line{i}{j}'))
                canvas.create_text(
                    line[0][0] + 5, 
                    line[0][1] + 5, 
                    anchor='nw', 
                    text=item.text(),
                    tags='collabel')
        root.mainloop()
        
