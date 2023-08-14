from shapes.Rectangle import Rectangle
from shapes.JaggedLine import JaggedLine
from shapes.StraightLine import StraightLine

class EntityFactory:
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
    def create_shape(entity_dictionary, grid_spacing):
        if '@vertex' in entity_dictionary:
            return Rectangle(entity_dictionary, grid_spacing)
        elif '@source' in entity_dictionary and '@target' in entity_dictionary:
            if entity_dictionary['@source'] == entity_dictionary['@target']:
                return JaggedLine(entity_dictionary, grid_spacing)
            else:
                return StraightLine(entity_dictionary, grid_spacing)
        else:
            raise ValueError("Invalid shape dictionary provided.")