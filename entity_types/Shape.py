from utils.Helpers import Helpers

class Shape:
    def __init__(self, entity_dictionary = None, grid_spacing = None):
        if entity_dictionary != None:
            self.entity_dictionary = entity_dictionary
        if grid_spacing != None:
            self.grid_spacing = grid_spacing

    @property
    def id(self):
        try:
            return self.entity_dictionary['@id']
        except:
            return None
    
    @property
    def text(self):
        try:
            return self.entity_dictionary['@value']
        except:
            return None
        
    @property
    def style(self):
        try:
            return Helpers.xml_string_to_dict(self.entity_dictionary['@style'])
        except:
            return None

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
        self.entity_dictionary['mxGeometry']['@x'] = str(int(coordinates[0] - 0.5 * self.width))
        self.entity_dictionary['mxGeometry']['@y'] = str(int(coordinates[1] - 0.5 * self.height))

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            raise KeyError(f"Invalid key '{key}'")
