from shapes.Rectangle import Rectangle
from shapes.JaggedLine import JaggedLine
from shapes.StraightLine import StraightLine

class ShapeFactory:
    DISPLAY_ATTRS = [
        'id', 
        'text', 
        'coordinates', 
        'type',
        'grid_center'
    ]
        
    REQUIRED_ATTRS = [
        'id', 
        'text', 
        'coordinates', 
        'type'
    ]

    @staticmethod
    def create_shape(shape_dict, grid_spacing):
        if '@vertex' in shape_dict:
            return Rectangle(shape_dict, grid_spacing)
        elif '@source' in shape_dict and '@target' in shape_dict:
            if shape_dict['@source'] == shape_dict['@target']:
                return JaggedLine(shape_dict, grid_spacing)
            else:
                return StraightLine(shape_dict, grid_spacing)
        else:
            raise ValueError("Invalid shape dictionary provided.")