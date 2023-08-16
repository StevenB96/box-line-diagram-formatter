import tkinter as tk
import random
from tqdm import tqdm
import copy
from utils.Helpers import Helpers
from utils.Model import Model
from utils.NumberedCanvas import NumberedCanvas

class CoordinateManager:
    def __init__(self, entities, connections, grid_spacing):
        self.current_entities = entities
        self.current_connections = connections
        self.grid_spacing = grid_spacing
        self.models = []
        self.initial_forest = 1000

    def initialise_models(self):
        model = Model(self.current_entities, self.current_connections)

        # Set grid dimensions
        total_width = 0
        for entity in self.current_entities:
            total_width += entity.width        
        initial_width = Helpers.round_to_grid(total_width, self.grid_spacing)
        self.set_canvas_size(initial_width, initial_width)

        # Set first itteration
        entities = copy.deepcopy(self.current_entities)
        connections = copy.deepcopy(self.current_connections)

        # for i in range(self.initial_forest):
        for i in tqdm(range(self.initial_forest)):
            for entity in entities:
                entity.set_grid_center((self.canvas_size[0] * random.random(), self.canvas_size[1] * random.random()))
            model = Model(entities, connections)

            self.models.append(model)

        self.models = sorted(self.models, key=lambda x: x.score)
        print(self.models[0].intersections_count)
        self.display_graph(self.models[0])

    def optimise_coordinates(self):
        # Generate minimal grid
        # debug_print(str(self.canvas_size))
        # Generate random layouts
        # Evaluate layouts
        # Select best layouts
        # Modify layouts
        # Evaluate layouts
        # Select best layouts
        # End after improvement slows or stops
        # Generate minimal grid
        # Repeat
        pass

    def set_canvas_size(self, width, height):
        self.canvas_size = (Helpers.round_to_grid(width, self.grid_spacing), Helpers.round_to_grid(height, self.grid_spacing))
    
    def display_graph(self, model):
        root = tk.Tk()
        canvas = NumberedCanvas(root, self.grid_spacing, model.entities + model.connections, width=4000, height=4000, bg='white', highlightthickness=0)
        canvas.pack()
        root.mainloop()