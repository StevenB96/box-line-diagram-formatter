import tkinter as tk
from random import randint


class Model:
    def __init__(self, connections, entities, grid_spacing):
        self.connections = connections
        self.entities = entities
        self.grid_spacing = grid_spacing
        self.font = ('Arial', 10)
        self.grid_line_colour = '#a3aeba'
        self.grid_gap = 10

    def get_penalty(self):
        size_penalty = self.get_size() * 0.001
        average_connection_length_penalty = self.get_average_connection_length() * \
            0.001
        intersections_count_penalty = self.get_intersections_count()
        return size_penalty + average_connection_length_penalty + intersections_count_penalty

    def display(self):
        grid_size = self.get_grid_size()
        print(grid_size)
        items = self.connections + self.entities
        root = tk.Tk()
        canvas = tk.Canvas(root, width=grid_size[0] + self.grid_spacing * self.grid_gap, height=grid_size[1] + self.grid_spacing * self.grid_gap, bg='white')
        canvas.pack()

        # draw horizontal lines and row labels
        for y in range(0, canvas.winfo_height(), self.grid_spacing):
            canvas.create_line(0, y, canvas.winfo_width(), y, fill=self.grid_line_colour, tags='gridline', width=1 if (
                y % (self.grid_gap * self.grid_spacing) == 0) == 0 else 2)
            if (y % (self.grid_gap * self.grid_spacing) == 0):
                canvas.create_text(
                    5,
                    y+5,
                    anchor='w',
                    text=str(y),
                    font=self.font, tags='rowlabel')

        # draw vertical lines and column labels
        for x in range(0, canvas.winfo_width(), self.grid_spacing):
            canvas.create_line(x, 0, x, canvas.winfo_height(), fill=self.grid_line_colour,
                             tags='gridline', width=1 if (x % (self.grid_gap * self.grid_spacing) == 0) == 0 else 2)
            if (x % (self.grid_gap * self.grid_spacing) == 0):
                canvas.create_text(
                    x+5,
                    5,
                    anchor='nw',
                    text=str(x),
                    font=self.font,
                    tags='collabel')

        # draw item lines
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
                    text=item.id()[-1],
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
        return intersection_count

    def get_entity_intersections(self, item_a, item_b):
        intersection_count = 0
        for line_a in item_a.line_set():
            for line_b in item_b.line_set():
                intersection_type = self.get_line_intersection_type(
                    line_a, line_b)
                if (intersection_type != 0):
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
        if (((x_intersect_within_a_range and (m1 == 0) and abs(y_intersect - y_maxA) < 1e-9) or
            (x_intersect_within_a_range and (m1 != 0) and y_intersect_within_a_range)) and
            ((x_intersect_within_b_range and (m2 == 0) and abs(y_intersect - y_maxB) < 1e-9) or
                (x_intersect_within_b_range and (m2 != 0) and y_intersect_within_b_range))):
            return 1
        else:
            return 0

    def get_coordinate_range(self):
        # Initialize the minimum and maximum values of x and y
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')

        # Loop through each item in the combined list
        for item in self.entities + self.connections:
            # Check if the item has coordinates and if they are True
            for x, y in item.coordinate_set():
                # Update min and max values of x and y
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)

        # Return the x-range and y-range as a tuple
        return (min_x, max_x), (min_y, max_y)

    def get_width(self):
        coordinate_range = self.get_coordinate_range()
        try:
            return coordinate_range[0][1] - coordinate_range[0][0]
        except Exception as e:
            print(e)

    def get_height(self):
        coordinate_range = self.get_coordinate_range()
        try:
            return coordinate_range[1][1] - coordinate_range[1][0]
        except Exception as e:
            print(e)

    def get_size(self):
        width = self.get_width()
        height = self.get_height()
        try:
            return (width + height) / 2
        except Exception as e:
            print(e)

    def get_average_connection_length(self):
        total_length = 0
        for connection in self.connections:
            total_length += connection.length()
        try:
            return total_length / len(self.connections)
        except Exception as e:
            print(e)

    def round_to_grid(self, number):
        return round(number / self.grid_spacing) * self.grid_spacing

    def get_grid_size(self):
        entities_by_parent_depth  = sorted(
            self.entities, key=lambda x: - x.parent_depth)
        entity_parent_depth = entities_by_parent_depth[0].parent_depth
        parent_depths = [entity.parent_depth for entity in entities_by_parent_depth]
        max_parent_depth = max(parent_depths)
        width = self.round_to_grid((max_parent_depth + 1) * self.grid_spacing * self.grid_gap)
        height = self.round_to_grid((entity_parent_depth + 1) * self.grid_spacing * self.grid_gap)
        return (width, height)

    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        string_attributes = [
            f"{value[0]}: {value[1]}" for value in self_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(
            self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return string
