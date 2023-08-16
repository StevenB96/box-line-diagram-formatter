from utils.Helpers import Helpers
import sys
# "@id": "_AMruqflp3BRAEhRA3ei-5",
# "@value": "A",
# "@id": "_AMruqflp3BRAEhRA3ei-6",
# "@value": "C",
# "@id": "_AMruqflp3BRAEhRA3ei-1",
# "@value": "B",
# "@id": "_AMruqflp3BRAEhRA3ei-9",
# "@value": "D",

class Model():
    def __init__(self, entities, connections):
        self.entities = entities
        self.connections = connections
        # Weights
        self.size_weight = 0.1
        # self.average_entity_spacing_weight = -0.001
        self.intersections_count_weight = 1
        self.update_connections()
        self.get_intersections_count()
        self.get_size()
        # self.get_average_entity_spacing()
        self.get_score()



    def get_score(self):
        try:
            intersections_count_score = self.intersections_count * self.intersections_count_weight
            size_score = self.size * self.size_weight
            # average_entity_spacing_score = self.average_entity_spacing * self.average_entity_spacing_weight
            self.score = intersections_count_score + size_score
        except Exception as e:
            Helpers.debug_print('Cannot define score attribute:', e, debug_type = 'error')
            return None
    
    # def get_average_entity_spacing(self):
    #     try:
    #         total_distance = 0
    #         for entity_a in self.entities:
    #             for entity_b in self.entities:
    #                 total_distance += ((entity_a.grid_center[1] - entity_a.grid_center[0]) ** 2 + (entity_b.grid_center[1] - entity_b.grid_center[0]) ** 2) ** 0.5
    #         self.average_entity_spacing = total_distance / (len(self.entities) ** 2)
    #     except Exception as e:
    #         Helpers.debug_print('Cannot define average_entity_spacing attribute:', e, debug_type = 'error')
    #         return None

    def get_coordinate_range(self):
        try:
            # Initialize the minimum and maximum values of x and y
            min_x = float('inf')
            max_x = float('-inf')
            min_y = float('inf')
            max_y = float('-inf')

            # Loop through each item in the combined list
            combined = self.entities + self.connections

            for item in combined:
                # Check if the item has coordinates and if they are True
                for coordinate in item.coordinates:
                    # If the coordinates are True, update min and max values of x and y
                    x, y = coordinate
                    if x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x
                    if y < min_y:
                        min_y = y
                    if y > max_y:
                        max_y = y

            # Return the x-range and y-range as a tuple
            self.coordinate_range = (min_x, max_x), (min_y, max_y)
        except Exception as e:
            Helpers.debug_print('Cannot define coordinate_range attribute:', e, debug_type = 'error')
            return None
    

    def get_width(self):
        self.get_coordinate_range()
        try:
            self.width = self.coordinate_range[0][1] - self.coordinate_range[0][0]
        except Exception as e:
            Helpers.debug_print('Cannot define width attribute:', e, debug_type = 'error')
            return None

    def get_height(self):
        self.get_coordinate_range()
        try:
            self.height = self.coordinate_range[1][1] - self.coordinate_range[1][0]
        except Exception as e:
            Helpers.debug_print('Cannot define height attribute:', e, debug_type = 'error')
            return None
        
    def get_size(self):
        self.get_width()
        self.get_height()
        try:
            self.size = (self.width + self.height) / 2
        except Exception as e:
            Helpers.debug_print('Cannot define size attribute:', e, debug_type = 'error')
            return None

    def get_intersections_count(self):
        intersections = 0
        combined = [item for item in (self.entities + self.connections) if item.type not in [Helpers.text_to_type('Jagged Line')]]
        for item_a in combined:
            for item_b in combined:
                if (item_a.id != item_b.id):
                    intersections += self.get_entity_intersections(item_a, item_b)
        # print(intersections)
        self.intersections_count = intersections

    def get_entity_intersections(self, item_a, item_b):
        intersections = 0
        for line_a in item_a.lines:
            for line_b in item_b.lines:
                if (self.get_line_intersection_type(line_a, line_b) != 0):
                    intersections += 1
                    Helpers.debug_print(Helpers.type_to_text(item_a.type), item_a.id, line_a, "crossed with" , Helpers.type_to_text(item_b.type), item_b.id, line_b)
        return intersections
    
    def get_line_intersection_type(self, line_a, line_b):
        coord_1, coord_2 = line_a
        coord_3, coord_4 = line_b
        x1, y1 = coord_1
        x2, y2 = coord_2
        x3, y3 = coord_3
        x4, y4 = coord_4
    
        # Calculate slopes and y-intercepts
        if x2 - x1 != 0:
            m1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - m1 * x1
        else:
            m1 = None
            b1 = None
        
        if x4 - x3 != 0:
            m2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - m2 * x3
        else:
            m2 = None
            b2 = None

        # Check if lines are both vertical and intersect
        if m1 is None and m2 is None:
            if x1 == x3:
                return 2
            else:
                return 0
        
        # Check if line A is vertical and intersects B
        if m1 is None and m2 is not None:
            x_intersect = x1
            intersect_on_line_b = max(x3, x4) > x_intersect > min(x3, x4)
            if intersect_on_line_b:
                return 3
            else:
                return 0
        
        # Check if line B is vertical and intersects A
        if m1 is not None and m2 is None:
            x_intersect = x3
            intersect_on_line_a = max(x1, x2) > x_intersect > min(x1, x2)
            if intersect_on_line_a:
                return 4
            else:
                return 0
        
        # Check if lines are colinear
        if (abs(m1 - m2) < 1e-9):
            if (abs(b1 - b2) < 1e-9):
                if ((y1 <= y3 <= y2) or (y1 >= y3 >= y2) or (y3 <= y1 <= y4) or (y3 >= y1 >= y4)):
                    return 5
                else:
                    return 0
            else:
                return 0
        
        # Check if lines intersect at a point
        x_intersect = (b2 - b1) / (m1 - m2)
        intersect_on_line_a = (abs(m1) < 1e-9) and (max(x1, x2) >= x_intersect >= min(x1, x2)) or ((max(x1, x2) > x_intersect > min(x1, x2)))
        intersect_on_line_b = (abs(m2) < 1e-9) and (max(x3, x4) >= x_intersect >= min(x3, x4)) or ((max(x3, x4) > x_intersect > min(x3, x4)))

        if (intersect_on_line_a and intersect_on_line_b):
            return 1
        else:
            return 0

    def update_connections(self):
        for connection in self.connections:
            if (Helpers.text_to_type('Straight Line') == connection.type):
                # Find the source entity in the entities list
                source_entity = next((entity for entity in self.entities if entity.id == connection.source), None)
                if source_entity is None:
                    Helpers.debug_print("Cannot find source entity for connection", connection)
                    continue
                
                # Find the target entity in the entities list
                target_entity = next((entity for entity in self.entities if entity.id == connection.target), None)
                if target_entity is None:
                    Helpers.debug_print("Cannot find target entity for connection", connection)
                    continue
                # Set the connections coordinates based on the entity coordinates
                connection.set_coordinates(source_entity, target_entity)

    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        string_attributes = [f"{value[0]}: {value[1]}" for value in self_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return f"* Model *\n{string}"