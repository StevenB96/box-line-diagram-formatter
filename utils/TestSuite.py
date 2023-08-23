from graph.model.Model import Model

class TestSuite:
    def __init__(self):
        if (False):
            self.test_get_entity_intersections()

    def line_set_intersections(self, line_set_a, line_set_b):
        intersection_count = 0
        for i, line_a in enumerate(line_set_a):
            for j, line_b in enumerate(line_set_b):
                intersection_type  = self.model.get_line_intersection_type(line_a, line_b)
                print(i, j, line_a, line_b, intersection_type, '\n')
                if (intersection_type != 0):
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
        print('\n# Debug Case A')
        # Debug Case A
        line_set_a = [((600, 350), (720, 350)), ((720, 350), (720, 410)), ((720, 410), (600, 410)), ((600, 410), (600, 350))]
        line_set_b = [((600, 350), (510, 230))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 0
        print('\n# Debug Case B')
        # Debug Case B
        line_set_a = [((450, 170), (570, 170)), ((570, 170), (570, 230)), ((570, 230), (450, 230)), ((450, 230), (450, 170))]
        line_set_b = [((430, 350), (510, 230))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 0
        print('\n# Debug Case C')
        # Debug case C
        line_set_a = [((140, 170), (260, 170)), ((260, 170), (260, 230)), ((260, 230), (140, 230)), ((140, 230), (140, 170))]
        line_set_b = [((140, 370), (200, 130))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 2
        pass