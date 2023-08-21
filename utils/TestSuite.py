from graph.model.Model import Model

class TestSuite:
    def __init__(self):
        if (False):
            self.test_get_entity_intersections()

    def line_set_intersections(self, line_set_a, line_set_b):
        intersection_count = 0
        for line_a in line_set_a:
            for line_b in line_set_b:
                if (self.model.get_line_intersection_type(line_a, line_b) != 0):
                    intersection_count += 1
        return intersection_count

    def test_get_entity_intersections(self):
        self.model = Model([],[], 10)
        print('# Identical rectangles.\n')
        # Identical rectangles.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 4
        print('\n# Overlapping rectangles in x and y directions. No lines are colinear.\n')
        # Overlapping rectangles in x and y directions. No lines are colinear.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((50, 50), (150, 50)), ((150, 50), (150, 150)), ((150, 150), (50, 150)), ((50, 150), (50, 50))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 2
        print('\n# Overlapping rectangles in x direction. Two lines are colinear.\n')
        # Overlapping rectangles in x direction. Two lines are colinear.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((150, 100), (250, 100)), ((250, 100), (250, 200)), ((250, 200), (150, 200)), ((150, 200), (150, 100))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 2
        print('\n# One line intersecting a rectangle with endpoints outside the boundaries\n')
        # One line intersecting a rectangle with endpoints outside the boundaries
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((50, 200), (200, 50))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 2
        print('\n# One line intersecting a rectangle with both endpoints on the boundaries\n')
        # One line intersecting a rectangle with both endpoints on the boundaries
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((100, 150), (150, 150))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 0
        print('\n# One line intersecting a rectangle with one endpoint on the boundaries')
        # One line intersecting a rectangle with one endpoint on the boundaries
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((100, 150), (200, 50))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 1
        print('\n# Two lines at right angles')
        # Two lines at right angles
        line_set_a = [((100, 100), (200, 100))]
        line_set_b = [((200, 100), (200, 200))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 0
        pass