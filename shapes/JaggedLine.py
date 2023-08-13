from shape_types.Line import Line
from utils.Helpers import Helpers

class JaggedLine(Line):
    def __init__(self, shape_dict, grid_spacing):
        self.shape_dict = shape_dict
        self.grid_spacing = grid_spacing
        self.type = Helpers.text_to_type('Jagged Line')

    @property
    def coordinates(self):
        coordinates = []
        for coord in self.shape_dict['mxGeometry']['Array']['mxPoint']:
            coordinates.append([coord['@x'], coord['@y']])
        return coordinates

    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        filtered_attribute_list = [(attr_name, attr_value) for attr_name, attr_value in self_attribute_list if attr_name in Helpers.DISPLAY_ATTRS]
        string_attributes = [f"{value[0]}: {value[1]}" for value in filtered_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return f"* {Helpers.type_to_text(0)} *\n{string}"