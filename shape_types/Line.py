from utils.Helpers import Helpers

class Line:
    def __init__(self, shape_dict = None, grid_spacing = None):
        if shape_dict != None:
            self.shape_dict = shape_dict
        if grid_spacing != None:
            self.grid_spacing = grid_spacing

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
    def source(self):
        try:
            return self.shape_dict['@source']
        except:
            return None

    @property
    def target(self):
        try:
            return self.shape_dict['@target']
        except:
            return None