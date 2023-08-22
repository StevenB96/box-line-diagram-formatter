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

    def get_intersections_count(self):
        intersection_count = 0
        combined = [item for item in self.entities + self.connections]
        for i, item_a in enumerate(combined):
            for j, item_b in enumerate(combined[i+1:]):
                if item_a.id() == item_b.id():
                    continue
                intersection_count += self.get_entity_intersections(
                        combined[i], item_b)
        print(intersection_count)
        self.intersections_count = intersection_count

    def get_entity_intersections(self, item_a, item_b):
        intersection_count = 0
        for line_a in item_a.line_set():
            for line_b in item_b.line_set():
                intersection_type = self.get_line_intersection_type(line_a, line_b)
                if (intersection_type != 0):
                    print(item_a.id(), item_a.line_set(), item_b.id(), item_b.line_set())
                    intersection_count += 1
        return intersection_count

    def get_line_intersection_type(self, line_a, line_b):
        coord_1, coord_2 = line_a
        coord_3, coord_4 = line_b
        x1, y1 = coord_1
        x2, y2 = coord_2
        x3, y3 = coord_3
        x4, y4 = coord_4

        if ((x1 == x3 and y1 == y3 and x2 == x4 and y2 == y4) or
            (x1 == x4 and y1 == y4 and x2 == x3 and y2 == y3)):
            return 6

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
            if abs(x1 - x3) < 1e-9:
                y_minA = min(y1, y2)
                y_maxA = max(y1, y2)
                y_minB = min(y3, y4)
                y_maxB = max(y3, y4)
                if ((y_maxB > y_maxA > y_minB) or (y_maxB > y_minA > y_minB)):
                    return 2
                else:
                    return 0
            else:
                return 0

        # Check if line A is vertical and intersects B
        if m1 is None and m2 is not None:
            # print('B')
            x_intersect = x1
            y_intersect = m2 * x_intersect + b2
            # A
            y_minA = min(y1, y2)
            y_maxA = max(y1, y2)
            x_minB = min(x3, x4)
            x_maxB = max(x3, x4)
            if ((y_minA < y_intersect < y_maxA) and (x_minB < x_intersect < x_maxB)):
                return 3
            else:
                return 0

        # Check if line B is vertical and intersects A
        if m1 is not None and m2 is None:
            # print('A')
            x_intersect = x3
            y_intersect = m1 * x_intersect + b1
            # B
            x_minA = min(x1, x2)
            x_maxA = max(x1, x2)
            y_minB = min(y3, y4)
            y_maxB = max(y3, y4)
            if ((y_minB < y_intersect < y_maxB) and (x_minA < x_intersect < x_maxA)):
                return 4
            else:
                return 0

        # Check if lines are colinear
        if (abs(m1 - m2) < 1e-9):
            if (abs(b1 - b2) < 1e-9):
                if ((min(x1, x2) < x3 < max(x1, x2)) or (min(x1, x2) < x4 < max(x1, x2)) or
                        (min(x3, x4) < x1 < max(x3, x4)) or (min(x3, x4) < x2 < max(x3, x4))):
                    return 5
                else:
                    return 0
            else:
                return 0
        # print('V')
        # Calculate standard intersection
        x_intersect = (b2 - b1) / (m1 - m2)
        y_intersect = m1 * x_intersect + b1
        x_minA = min(x1, x2)
        x_maxA = max(x1, x2)
        y_minA = min(y1, y2)
        y_maxA = max(y1, y2)
        x_minB = min(x3, x4)
        x_maxB = max(x3, x4)
        y_minB = min(y3, y4)
        y_maxB = max(y3, y4)
        x_intersect_within_a_range = x_minA < x_intersect < x_maxA
        x_intersect_within_b_range = x_minB < x_intersect < x_maxB
        y_intersect_within_a_range = y_minA < y_intersect < y_maxA
        y_intersect_within_b_range = y_minB < y_intersect < y_maxB
        # Check if point of intersection is within both line ranges
        if (((x_intersect_within_a_range and (m1 == 0) and y_intersect_within_a_range) or
            (x_intersect_within_a_range and (m1 != 0) and y_intersect_within_a_range)) and
            ((x_intersect_within_b_range and (m2 == 0) and y_intersect_within_b_range) or
            (x_intersect_within_b_range and (m2 != 0) and y_intersect_within_b_range))):
            return 1
        else:
            return 0
