from utils.ModelSpaceItem import ModelSpaceItem

class Connection(ModelSpaceItem):
    def __init__(self):
        pass

    def set_coordinates(self, source_shape, target_shape):
        # Exit coordinate
        base_coordinate = source_shape.coordinate_set[0]
        exit_x = float(self.style["exitX"])
        exit_y = float(self.style["exitY"])
        exit_coordinate = (self.round_to_grid(base_coordinate[0] + (exit_x * source_shape.width)), self.round_to_grid(base_coordinate[1] + (exit_y * source_shape.height)))
        # Entry coordinate
        base_coordinate = target_shape.coordinate_set[0]
        entry_x = float(self.style["entryX"])
        entry_y = float(self.style["entryY"])
        entry_coordinate = (self.round_to_grid(base_coordinate[0] + (entry_x * target_shape.width)), self.round_to_grid(base_coordinate[1] + (entry_y * target_shape.height)))
        self.coordinate_set = [exit_coordinate, entry_coordinate]

    @property
    def source(self):
        try:
            return self.cell['@source']
        except Exception as e:
            print(e)

    @property
    def target(self):
        try:
            return self.cell['@target']
        except Exception as e:
            print(e)