from entity_types.Shape import Shape
from utils.Helpers import Helpers

class Rectangle(Shape):
    def __init__(self, entity_dictionary, grid_spacing):
        self.entity_dictionary = entity_dictionary
        self.grid_spacing = grid_spacing
        self.entity_type = Helpers.text_to_entity_type('Shape')
        self.type = Helpers.text_to_type('Rectangle')

    @property
    def width(self):
        try:
            return Helpers.round_to_grid(int(self.entity_dictionary['mxGeometry']['@width']), self.grid_spacing)
        except:
            return None

    @property
    def height(self):
        try:
            return Helpers.round_to_grid(int(self.entity_dictionary['mxGeometry']['@height']), self.grid_spacing)
        except:
            return None

    @property
    def x(self):
        try:
            return Helpers.round_to_grid(int(self.entity_dictionary['mxGeometry']['@x']), self.grid_spacing)
        except:
            return None
    
    @property
    def y(self):
        try:
            return Helpers.round_to_grid(int(self.entity_dictionary['mxGeometry']['@y']), self.grid_spacing)
        except:
            return None

    @property
    def coordinates(self):
        coordinates = [
            (self.x, self.y), 
            (self.x + self.width, self.y), 
            (self.x + self.width, self.y + self.height), 
            (self.x, self.y + self.height)
        ]
        return coordinates

    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        filtered_attribute_list = [(attr_name, attr_value) for attr_name, attr_value in self_attribute_list if attr_name in Helpers.DISPLAY_ATTRS]
        string_attributes = [f"{value[0]}: {value[1]}" for value in filtered_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return f"* {Helpers.type_to_text(2)} *\n{string}"