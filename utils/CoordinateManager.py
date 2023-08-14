import random
from utils.Helpers import Helpers

class CoordinateManager:
    def __init__(self, entities, connections):
        self.entities = []
        self.connections = connections
        print(entities, connections)
        for entity in entities:
            if (Helpers.text_to_type('Rectangle') == entity.type or Helpers.text_to_type('Straight Line') == entity.type):
                if(Helpers.text_to_type('Rectangle') == entity.type):
                    entity.set_grid_center((10 * random.randint(0, 999), 10 * random.randint(0, 999)))
                self.entities.append(entity)

        print(str(self.check_for_intersections()))

    def optimise_coordinates(self, grid_spacing):
        pass

    def generate_grid(self, grid_size):
        pass

    def check_for_intersections(self):
        for entity_a in self.entities:
            for entity_b in self.entities:
                if (entity_a.id != entity_b.id):
                    if (self.is_entity_intersection(entity_a, entity_b)):
                        return True
        return False

    def is_entity_intersection(self, entity_a, entity_b):
        for line_a in entity_a.lines:
            for line_b in entity_b.lines:
                if (self.is_line_intersection(line_a, line_b) == True):
                    return True
        return False

    def is_line_intersection(self, line_a, line_b):
        # line_a: tuple of two coordinates (x1, y1), (x2, y2)
        # line_b: tuple of two coordinates (x1, y1), (x2, y2)

        # check if points of each line are distinct
        if line_a[0] == line_a[1] or line_b[0] == line_b[1]:
            print("Invalid input - points must be distinct")
            return False

        # calculate slope and y-intercept of line a
        try:
            slope_a = (line_a[1][1] - line_a[0][1]) / (line_a[1][0] - line_a[0][0])
        except ZeroDivisionError:
            # Line A is vertical (undefined slope)
            if line_b[0][0] <= line_a[0][0] <= line_b[1][0] or \
                    line_b[0][0] <= line_a[1][0] <= line_b[1][0] or \
                    line_a[0][0] <= line_b[0][0] <= line_a[1][0] or \
                    line_a[0][0] <= line_b[1][0] <= line_a[1][0]:
                return True
            else:
                return False
        y_intercept_a = line_a[0][1] - slope_a * line_a[0][0]

        # calculate slope and y-intercept of line b
        try:
            slope_b = (line_b[1][1] - line_b[0][1]) / (line_b[1][0] - line_b[0][0])
        except ZeroDivisionError:
            # Line B is vertical (undefined slope)
            if line_a[0][0] <= line_b[0][0] <= line_a[1][0] or \
                    line_a[0][0] <= line_b[1][0] <= line_a[1][0] or \
                    line_b[0][0] <= line_a[0][0] <= line_b[1][0] or \
                    line_b[0][0] <= line_a[1][0] <= line_b[1][0]:
                return True
            else:
                return False
        y_intercept_b = line_b[0][1] - slope_b * line_b[0][0]

        # check if lines are collinear
        if abs(slope_a - slope_b) < 1e-10 and abs(y_intercept_a - y_intercept_b) < 1e-10:
            # check if lines overlap
            if (max(line_a[0][0], line_a[1][0]) >= min(line_b[0][0], line_b[1][0]) and
                    min(line_a[0][0], line_a[1][0]) <= max(line_b[0][0], line_b[1][0])):
                return True
            else:
                return False
        # check if lines are parallel
        elif abs(slope_a - slope_b) < 1e-10:
            return False

        # calculate x-coordinate of intersection point
        x_intersect = (y_intercept_b - y_intercept_a) / (slope_a - slope_b)

        # check if intersection point lies on both lines
        if (x_intersect < min(line_a[0][0], line_a[1][0]) or
                x_intersect > max(line_a[0][0], line_a[1][0]) or
                x_intersect < min(line_b[0][0], line_b[1][0]) or
                x_intersect > max(line_b[0][0], line_b[1][0])):
            return False
        else:
            return True