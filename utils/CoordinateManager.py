import tkinter as tk
import random
from tqdm import tqdm
import copy
from utils.Helpers import Helpers
from utils.Model import Model
from utils.NumberedCanvas import NumberedCanvas
import time

class CoordinateManager:
    def __init__(self, entities, connections, grid_spacing):
        self.current_entities = entities
        self.current_connections = connections
        self.grid_spacing = grid_spacing
        self.models = []
        self.initial_forest = 30

    def initialise_models(self):
        model = Model(self.current_entities, self.current_connections)

        # Set grid dimensions
        total_width = 0
        for entity in self.current_entities:
            total_width += entity.width        
        initial_width = Helpers.round_to_grid(total_width, self.grid_spacing)
        self.set_canvas(initial_width, initial_width)

        # Set first itteration
        entities = copy.deepcopy(self.current_entities)
        connections = copy.deepcopy(self.current_connections)

        # for i in range(self.initial_forest):
        for i in tqdm(range(self.initial_forest)):
            for entity in entities:
                grid_center = random.choice(random.choice(self.canvas))
                entity.set_grid_center(grid_center)
            model = Model(entities, connections)

            self.models.append(model)

        self.models = sorted(self.models, key=lambda x: x.score)

        # print(self.models[0].intersections_count)
        best_model = self.models[0]

        entities = copy.deepcopy(self.models[0].entities)

        # set the initial time to the current time
        last_improvement_time = time.monotonic()
        x = 30
        while True:
            # check if the time since the last improvement is greater than x seconds
            if time.monotonic() - last_improvement_time > x:
                print(f"No improvements made in {x} seconds, stopping the loop")
                break
            
            entity = random.choice(entities)
            grid_center = random.choice(random.choice(self.canvas))
            entity.set_grid_center(grid_center)
            model = Model(entities, connections)
            
            if model.score > best_model.score:
                # print(model.score)
                best_model = model
                last_improvement_time = time.monotonic()  # update the last improvement time

        print(best_model.intersections_count)
        self.display_graph(best_model)

    def optimise_coordinates(self):
        # Generate minimal grid
        # debug_print(str(self.canvas))
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

    def set_canvas(self, width, height):
        grid = []
        for y in range(0, Helpers.round_to_grid(height, self.grid_spacing), self.grid_spacing * 10):
            row = []
            for x in range(0, Helpers.round_to_grid(width, self.grid_spacing), self.grid_spacing * 10):
                row.append((x, y))
            grid.append(row)
        self.canvas = grid
    
    def display_graph(self, model):
        root = tk.Tk()
        canvas = NumberedCanvas(root, self.grid_spacing, model.entities + model.connections, width=4000, height=4000, bg='white', highlightthickness=0)
        canvas.pack()
        root.mainloop()