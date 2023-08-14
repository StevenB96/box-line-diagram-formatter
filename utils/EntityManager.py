from factories.EntityFactory import EntityFactory
from utils.Helpers import Helpers

class EntityManager:
    def __init__(self):
        pass
    
    def generate_entities(self, input_dict, grid_spacing):
        self.entities = []
        self.connections = []

        # Iterate through all `mxCell`s in the root dictionary
        for mx_cell in input_dict:
            # If a `Shape` instance can be created from the `mxCell`, add it to the `shapes` list
            try:
                shape = EntityFactory.create_shape(mx_cell, grid_spacing)
                if (shape.entity_type == Helpers.text_to_entity_type('Shape')):
                    self.entities.append(EntityFactory.create_shape(mx_cell, grid_spacing))
                elif (shape.entity_type == Helpers.text_to_entity_type('Connection')):
                    self.connections.append(EntityFactory.create_shape(mx_cell, grid_spacing))
            # If creating a `Shape` instance from the `mxCell` fails, skip it and move to the next one
            except Exception as e:
                print(e)
                continue