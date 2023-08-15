import tkinter as tk
import random
from tqdm import tqdm
import copy
from utils.Helpers import Helpers
from utils.NumberedCanvas import NumberedCanvas

class CoordinateManager:
    def __init__(self, entities, connections, grid_spacing):
        self.entities = entities
        self.connections = connections
        self.grid_spacing = grid_spacing
        self.update_connections()
        self.models = []
        self.initial_forest = 1000

    def initialise_models(self):
        # Set grid dimensions
        total_width = 0
        for entity in self.entities:
            total_width += entity.width        
        self.canvas_size = (Helpers.round_to_grid(total_width, self.grid_spacing), Helpers.round_to_grid(total_width, self.grid_spacing))

        # Set first itteration
        for i in tqdm(range(self.initial_forest)):
            for entity in self.entities:
                entity.set_grid_center((self.canvas_size[0] * random.random(), self.canvas_size[1] * random.random()))
            self.update_connections()
            self.models.append({
                "model": copy.deepcopy(self.entities),
                "score": self.intersections_count()
            })

        self.models = sorted(self.models, key=lambda x: x["score"])
        self.entities = self.models[0]["model"]
        self.update_connections()
        # print(self.models[0])
        self.display_graph()

    def optimise_coordinates(self):
        # Generate minimal grid
        # print(str(self.canvas_size))
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

    def generate_grid(self):
        pass

    def intersections_count(self):
        intersections = 0
        combined = self.entities + self.connections
        for entity_a in combined:
            for entity_b in combined:
                intersections += self.entity_intersections(entity_a, entity_b)
        return intersections

    def entity_intersections(self, entity_a, entity_b):
        intersections = 0
        for line_a in entity_a.lines:
            for line_b in entity_b.lines:
                if (self.is_line_intersection(line_a, line_b) == True):
                    intersections += 1
                    # print(Helpers.type_to_text(entity_a.type), entity_a.id, line_a, "crossed with" , Helpers.type_to_text(entity_b.type), entity_b.id, line_b)
        return intersections

    def is_line_intersection(self, line_a, line_b):
        if line_a[0] == line_a[1] or line_b[0] == line_b[1]:
            # print("Invalid input - points must be distinct")
            return False

        try:
            slope_a = (line_a[1][1] - line_a[0][1]) / (line_a[1][0] - line_a[0][0])
            y_intercept_a = line_a[0][1] - slope_a * line_a[0][0]
            line_dict_a = {
                "coordinates": line_a,
                "m": slope_a,
                "c": y_intercept_a
            }
        except ZeroDivisionError:
            # Vertical Intersection
            return self.handle_vertical_intersection(line_a, line_b)
        try:
            slope_b = (line_b[1][1] - line_b[0][1]) / (line_b[1][0] - line_b[0][0])
            y_intercept_b = line_b[0][1] - slope_b * line_b[0][0]
            line_dict_b = {
                "coordinates": line_b,
                "m": slope_b,
                "c": y_intercept_b
            }
        except ZeroDivisionError:
            # Vertical Intersection
            return self.handle_vertical_intersection(line_a, line_b)

        if (abs(slope_a - slope_b) < 1e-10 and abs(y_intercept_a - y_intercept_b) < 1e-10):
            # Colinear Intersection
            return self.handle_colinear_intersection(line_a, line_b)
        else:
            # Intersection
            return self.handle_intersection(line_dict_a, line_dict_b)

    def handle_vertical_intersection(self, line_a, line_b):
        if (line_a[0][0] == line_b[0][0] and line_a[0][1] == line_b[0][1] and line_a[1][0] == line_b[1][0] and line_a[1][1] == line_b[1][1]):
            # print('are identical')
            return True

        a_is_vertical = line_a[0][0] == line_a[1][0]
        b_is_vertical = line_b[0][0] == line_b[1][0]
        if (a_is_vertical and b_is_vertical):
            # print('both are vertical')
            by_start_within_a_range = (line_a[0][1] < line_b[0][1] < line_a[1][1]) or (line_a[0][1] > line_b[0][1] > line_a[1][1])
            ay_start_within_b_range = (line_b[0][1] < line_a[0][1] < line_b[1][1]) or (line_b[0][1] > line_a[0][1] > line_b[1][1])
            by_end_within_a_range = (line_a[0][1] < line_b[1][1] < line_a[1][1]) or (line_a[0][1] > line_b[1][1] > line_a[1][1])
            ay_end_within_b_range = (line_b[0][1] < line_a[1][1] < line_b[1][1]) or (line_b[0][1] > line_a[1][1] > line_b[1][1])
            do_intersect = by_start_within_a_range or ay_start_within_b_range or by_end_within_a_range or ay_end_within_b_range
            # print(str(do_intersect))
            return do_intersect
        elif (a_is_vertical):
            # print('a is vertical')
            slope_b = (line_b[1][1] - line_b[0][1]) / (line_b[1][0] - line_b[0][0])
            y_intercept_b = line_b[0][1] - slope_b * line_b[0][0]
            y_line_intercept = int(slope_b * line_a[0][0] + y_intercept_b)
            ax_within_b_range = line_b[0][0] < line_a[0][0] < line_b[1][0]
            y_line_intercept_within_a_range = (line_a[0][1] < y_line_intercept < line_a[1][1]) or (line_a[0][1] > y_line_intercept > line_a[1][1])
            do_intersect = y_line_intercept_within_a_range and ax_within_b_range
            # print(str(do_intersect))
            return do_intersect
        elif (b_is_vertical):
            # print('b is vertical')
            slope_a = (line_a[1][1] - line_a[0][1]) / (line_a[1][0] - line_a[0][0])
            y_intercept_a = line_a[0][1] - slope_a * line_a[0][0]
            y_line_intercept = int(slope_a * line_b[0][0] + y_intercept_a)
            bx_within_b_range = line_a[0][0] < line_b[0][0] < line_a[1][0]
            y_line_intercept_within_b_range = (line_b[0][1] < y_line_intercept < line_b[1][1]) or (line_b[0][1] > y_line_intercept > line_b[1][1])
            do_intersect = y_line_intercept_within_b_range and bx_within_b_range
            # print(str(do_intersect))
            return do_intersect

    def handle_colinear_intersection(self, line_a, line_b):
        # print('are colinear')
        bx_start_within_a_range = (line_a[0][0] < line_b[0][0] < line_a[1][0]) or (line_a[0][0] > line_b[0][0] > line_a[1][0])
        ax_start_within_b_range = (line_b[0][0] < line_a[0][0] < line_b[1][0]) or (line_b[0][0] > line_a[0][0] > line_b[1][0])
        bx_end_within_a_range = (line_a[0][0] < line_b[1][0] < line_a[1][0]) or (line_a[0][0] > line_b[1][0] > line_a[1][0])
        ax_end_within_b_range = (line_b[0][0] < line_a[1][0] < line_b[1][0]) or (line_b[0][0] > line_a[1][0] > line_b[1][0])
        do_intersect = bx_start_within_a_range or ax_start_within_b_range or bx_end_within_a_range or ax_end_within_b_range
        # print(str(do_intersect))
        return do_intersect

    def handle_intersection(self, line_dict_a, line_dict_b):
        are_both_horizontal = abs(line_dict_a['m'] - line_dict_b['m']) < 1e-10
        if (are_both_horizontal):
            # print('are both horizontal but not colinear')
            do_intersect = (line_dict_a['coordinates'][0][1] < line_dict_b['coordinates'][0][1] < line_dict_a['coordinates'][1][1]) or (line_dict_b['coordinates'][0][1] < line_dict_a['coordinates'][0][1] < line_dict_b['coordinates'][1][1])
            # print(str(do_intersect))
            return do_intersect
        else:
            # print('are not colinear')
            x_intercept = int((line_dict_b['c'] - line_dict_a['c']) / (line_dict_a['m'] - line_dict_b['m']))
            x_intercept_within_a_range = line_dict_a['coordinates'][0][0] < x_intercept < line_dict_a['coordinates'][1][0]
            x_intercept_within_b_range = line_dict_b['coordinates'][0][0] < x_intercept < line_dict_b['coordinates'][1][0]
            do_intersect = x_intercept_within_a_range and x_intercept_within_b_range
            # print(str(do_intersect))
            return do_intersect
        
    def display_graph(self):
        root = tk.Tk()
        canvas = NumberedCanvas(root, self.grid_spacing, self.entities + self.connections, width=4000, height=4000, bg='white', highlightthickness=0)
        canvas.pack()
        root.mainloop()

    def is_point_within_coords(point, coordinates):
        x = point[0]
        y = point[1]
        num_coords = len(coordinates)
        inside = False
        p1x, p1y = coordinates[0]
        for i in range(num_coords+1):
            p2x, p2y = coordinates[i % num_coords]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def update_connections(self):
        for connection in self.connections:
            if (Helpers.text_to_type('Straight Line') == connection.type or Helpers.text_to_type('Rectangle') == connection.type):
                # Find the source entity in the entities list
                source_entity = next((entity for entity in self.entities if entity.id == connection.source), None)
                if source_entity is None:
                    print("Source entity not found for connection", connection)
                    continue
                
                # Find the target entity in the entities list
                target_entity = next((entity for entity in self.entities if entity.id == connection.target), None)
                if target_entity is None:
                    print("Target entity not found for connection", connection)
                    continue
                
                # Set the connections coordinates based on the entity coordinates
                connection.set_coordinates(source_entity, target_entity)