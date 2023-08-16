from utils.Model import Model

class TestSuite:
    def __init__(self):
        self.test_get_entity_intersections()

    def line_set_intersections(self, line_set_a, line_set_b):
        intersection_count = 0
        for line_a in line_set_a:
            for line_b in line_set_b:
                print(line_a, line_b)
                line_intersection_type = Model.get_line_intersection_type(self.model, line_a, line_b)
                lines_are_distinct = not (line_a[0] == line_a[1] or line_b[0] == line_b[1])
                if lines_are_distinct and line_intersection_type != 0:
                    print(line_intersection_type)
                    intersection_count += 1
        return intersection_count
    def test_get_entity_intersections(self):
        self.model = Model([],[])

        # # Overlapping rectangles in x and y directions. No two lines are colinear.
        # line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        # line_set_b = [((50, 50), (150, 50)), ((150, 50), (150, 150)), ((150, 150), (50, 150)), ((50, 150), (50, 50))]
        # intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        # assert intersection_count == 2

        # Overlapping rectangles in x direction. Two lines are colinear.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((150, 100), (250, 100)), ((250, 100), (250, 200)), ((250, 200), (150, 200)), ((150, 200), (150, 100))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 2

        pass