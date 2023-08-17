from shape_types.entity.Entity import Entity

class Rectangle(Entity):
    def __init__(self, cell, grid_spacing):
        self.cell = cell
        self.grid_spacing = grid_spacing
        self.shape_type = 'Entity'
        self.type = 'Rectangle'

    @property
    def width(self):
        try:
            return self.round_to_grid(int(self.cell['mxGeometry']['@width']))
        except Exception as e:
            print(e)

    @property
    def height(self):
        try:
            return self.round_to_grid(int(self.cell['mxGeometry']['@height']))
        except Exception as e:
            print(e)

    @property
    def x(self):
        try:
            return self.round_to_grid(int(self.cell['mxGeometry']['@x']))
        except Exception as e:
            print(e)
    
    @property
    def y(self):
        try:
            return self.round_to_grid(int(self.cell['mxGeometry']['@y']))
        except Exception as e:
            print(e)

    @property
    def coordinate_set(self):
        try:
            coordinate_set = [
                (self.x, self.y), 
                (self.x + self.width, self.y), 
                (self.x + self.width, self.y + self.height), 
                (self.x, self.y + self.height)
            ]
            return coordinate_set
        except Exception as e:
            print(e)