from utils.Model import Model

class TestSuite:
    def __init__(self):
        self.test_get_entity_intersections()

    def line_set_intersections(self, line_set_a, line_set_b):
        intersection_count = 0
        for line_a in line_set_a:
            for line_b in line_set_b:
                line_intersection_type = Model.get_line_intersection_type(self.model, line_a, line_b)
                if line_intersection_type != 0:
                    intersection_count += 1
        return intersection_count

    def test_get_entity_intersections(self):
        self.model = Model([],[])

        # Idendical rectangles.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 4 # 2 x type 5, 2 x type 3

        # Overlapping rectangles in x and y directions. No lines are colinear.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((50, 50), (150, 50)), ((150, 50), (150, 150)), ((150, 150), (50, 150)), ((50, 150), (50, 50))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 4 # 2 x type 4, 2 x type 3

        # Overlapping rectangles in x direction. Two lines are colinear.
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((150, 100), (250, 100)), ((250, 100), (250, 200)), ((250, 200), (150, 200)), ((150, 200), (150, 100))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 6 # 2 x type 4, 2 x type 3, 2 x type 5  

        # One line intersecting a rectangle with endpoints outside the boundaries
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((50, 150), (150, 50))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 2 # 1 x type 3, 1 x type 1

        # One line intersecting a rectangle with both endpoints on the boundaries
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((100, 150), (150, 100))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 0

        # One line intersecting a rectangle with one endpoint on the boundaries
        line_set_a = [((100, 100), (200, 100)), ((200, 100), (200, 200)), ((200, 200), (100, 200)), ((100, 200), (100, 100))]
        line_set_b = [((100, 150), (150, 50))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 1 # 1 x type 1

        # Two lines at right angles
        line_set_a = [((100, 100), (200, 100))]
        line_set_b = [((200, 100), (200, 200))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 0

        # Test case A
        line_set_a = [((140, 170), (260, 170)), ((260, 170), (260, 230)), ((260, 230), (140, 230)), ((140, 230), (140, 170))]
        line_set_b = [((140, 370), (200, 130))]
        intersection_count = self.line_set_intersections(line_set_a, line_set_b)
        assert intersection_count == 1
        pass