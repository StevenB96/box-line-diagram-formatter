from entity_types.Connection import Connection
from utils.Helpers import Helpers

class StraightLine(Connection):
    def __init__(self, entity_dictionary, grid_spacing):
        self.entity_dictionary = entity_dictionary
        self.grid_spacing = grid_spacing
        self.coordinates = []
        self.entity_type = Helpers.text_to_entity_type('Connection')
        self.type = Helpers.text_to_type('Straight Line')

    def set_coordinates(self, source_entity, target_entity):
        # Exit coordinate
        base_coordinate = source_entity.coordinates[0]
        exit_x = float(self.style["exitX"])
        exit_y = float(self.style["exitY"])
        exit_coordinate = (int(base_coordinate[0] + (exit_x * source_entity.width)), int(base_coordinate[1] + (exit_y * source_entity.height)))
        # Entry coordinate
        base_coordinate = target_entity.coordinates[0]
        entry_x = float(self.style["entryX"])
        entry_y = float(self.style["entryY"])
        entry_coordinate = (int(base_coordinate[0] + (entry_x * target_entity.width)), int(base_coordinate[1] + (entry_y * target_entity.height)))
        self.coordinates = [exit_coordinate, entry_coordinate]

    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        filtered_attribute_list = [(attr_name, attr_value) for attr_name, attr_value in self_attribute_list if attr_name in Helpers.DISPLAY_ATTRS]
        string_attributes = [f"{value[0]}: {value[1]}" for value in filtered_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return f"* {Helpers.type_to_text(1)} *\n{string}"