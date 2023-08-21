from utils.ModelSpaceItem import ModelSpaceItem
from utils.Helpers import Helpers

class Connection(ModelSpaceItem):
    def __init__(self):
        pass

    def set_coordinates(self, source_shape, target_shape):
        self.source_shape = source_shape
        self.target_shape = target_shape
        self.set_entity_coordinate()
        self.set_exit_style()
        
    def coordinate_set(self):
        try:
            return self._coordinate_set
        except Exception as e:
            print(e)

    def source(self):
        try:
            return self.cell['@source']
        except Exception as e:
            print(e)

    def target(self):
        try:
            return self.cell['@target']
        except Exception as e:
            print(e)

    def set_entity_coordinate(self):
        # Exit coordinate
        base_coordinate = self.source_shape.coordinate_set()[0]
        exit_x = float(self.style()["exitX"])
        exit_y = float(self.style()["exitY"])
        exit_coordinate_x = self.round_to_grid(base_coordinate[0] + (exit_x * self.source_shape.width()))
        exit_coordinate_y = self.round_to_grid(base_coordinate[1] + (exit_y * self.source_shape.height()))
        exit_coordinate = (exit_coordinate_x, exit_coordinate_y)
        # Entry coordinate
        base_coordinate = self.target_shape.coordinate_set()[0]
        entry_x = float(self.style()["entryX"])
        entry_y = float(self.style()["entryY"])
        entry_coordinate_x = self.round_to_grid(base_coordinate[0] + (entry_x * self.target_shape.width()))
        entry_coordinate_y = self.round_to_grid(base_coordinate[1] + (entry_y * self.target_shape.height()))
        entry_coordinate = (entry_coordinate_x, entry_coordinate_y)
        self._coordinate_set = [exit_coordinate, entry_coordinate]

    def set_exit_style(self):
        target_shortest_distance = {
            'distance': float('inf'),
            'coordinate': []
        }
        for coordinate in self.source_shape.coordinate_set():
            connection_coordinates = self.coordinate_set()
            distance = Helpers.distance(
                coordinate, connection_coordinates[1])
            if (distance < target_shortest_distance['distance']):
                target_shortest_distance['distance'] = distance
                target_shortest_distance['coordinate'] = coordinate
        exit_coordinate = target_shortest_distance['coordinate']
        exit_x = self.round_to_nearest_quarter((abs(self.source_shape.x() - exit_coordinate[0]) / self.source_shape.width()))
        exit_y = self.round_to_nearest_quarter((abs(self.source_shape.y() - exit_coordinate[1]) / self.source_shape.height()))
        style = self.style()
        style["exitX"] = str(exit_x)
        style["exitY"] = str(exit_y)
        style_string = Helpers.dict_to_xml_string(style)
        self.cell['@style'] = style_string
        self.set_entity_coordinate()
