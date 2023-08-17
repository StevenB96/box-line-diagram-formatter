from utils.ModelSpaceItem import ModelSpaceItem

class Entity(ModelSpaceItem):
    def __init__(self):
        pass

    @property
    def grid_center(self):
        x = [p[0] for p in self.coordinate_set]
        y = [p[1] for p in self.coordinate_set]
        centroid = (self.round_to_grid(sum(x) / len(self.coordinate_set)), self.round_to_grid(sum(y) / len(self.coordinate_set)))
        return centroid
    
    def set_grid_center(self, coordinates):
        self.entity_dictionary['mxGeometry']['@x'] = str(int(coordinates[0] - 0.5 * self.width))
        self.entity_dictionary['mxGeometry']['@y'] = str(int(coordinates[1] - 0.5 * self.height))