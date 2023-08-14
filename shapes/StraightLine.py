from entity_types.Connection import Connection
from utils.Helpers import Helpers

class StraightLine(Connection):
    def __init__(self, entity_dictionary, grid_spacing):
        self.entity_dictionary = entity_dictionary
        self.grid_spacing = grid_spacing
        self.entity_type = Helpers.text_to_entity_type('Connection')
        self.type = Helpers.text_to_type('Straight Line')

    @property
    def coordinates(self):
        print(self.style)
        source_point = next((coord for coord in self.entity_dictionary['mxGeometry']['mxPoint'] if coord['@as'] == 'sourcePoint'), None)
        target_point = next((coord for coord in self.entity_dictionary['mxGeometry']['mxPoint'] if coord['@as'] == 'targetPoint'), None)
        return [
            (
                Helpers.round_to_grid(int(source_point['@x']), self.grid_spacing), 
                Helpers.round_to_grid(int(source_point['@y']), self.grid_spacing)
            ),
            (
                Helpers.round_to_grid(int(target_point['@x']), self.grid_spacing),
                Helpers.round_to_grid(int(target_point['@y']), self.grid_spacing)
            )
        ]

    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        filtered_attribute_list = [(attr_name, attr_value) for attr_name, attr_value in self_attribute_list if attr_name in Helpers.DISPLAY_ATTRS]
        string_attributes = [f"{value[0]}: {value[1]}" for value in filtered_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return f"* {Helpers.type_to_text(1)} *\n{string}"