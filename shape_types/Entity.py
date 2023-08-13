from utils.Helpers import Helpers

class Entity:
    def __init__(self, shape_dict = None, grid_spacing = None):
        if shape_dict != None:
            self.shape_dict = shape_dict
        if grid_spacing != None:
            self.grid_spacing = grid_spacing

    @property
    def id(self):
        try:
            return self.shape_dict['@id']
        except:
            return None
    
    @property
    def text(self):
        try:
            return self.shape_dict['@value']
        except:
            return None

    @property
    def width(self):
        try:
            return Helpers.round_to_grid(int(self.shape_dict['mxGeometry']['@width']), self.grid_spacing)
        except:
            return None

    @property
    def height(self):
        try:
            return Helpers.round_to_grid(int(self.shape_dict['mxGeometry']['@height']), self.grid_spacing)
        except:
            return None

    @property
    def x(self):
        try:
            return Helpers.round_to_grid(int(self.shape_dict['mxGeometry']['@x']), self.grid_spacing)
        except:
            return None
    
    @property
    def y(self):
        try:
            return Helpers.round_to_grid(int(self.shape_dict['mxGeometry']['@y']), self.grid_spacing)
        except:
            return None

    @property
    def coordinates(self):
        coordinates = [
            [self.x, self.y], 
            [self.x + self.width, self.y], 
            [self.x + self.width, self.y + self.height], 
            [self.x, self.y + self.height]
        ]

        return coordinates

    @property
    def lines(self):
        lines = []
        for i in range(len(self.coordinates)):
            if i == len(self.coordinates) - 1:
                lines.append((self.coordinates[i], self.coordinates[0]))
            else:
                lines.append((self.coordinates[i], self.coordinates[i+1]))
        return lines
    
    @property
    def grid_center(self):
        x = [p[0] for p in self.coordinates]
        y = [p[1] for p in self.coordinates]
        centroid = (Helpers.round_to_grid(sum(x) / len(self.coordinates), self.grid_spacing), Helpers.round_to_grid(sum(y) / len(self.coordinates), self.grid_spacing))
        return centroid
    
    def set_grid_center(self, coordinates):
        self.shape_dict['mxGeometry']['@x'] = coordinates[0] - 0.5 * self.width
        self.shape_dict['mxGeometry']['@y'] = coordinates[1] - 0.5 * self.height
