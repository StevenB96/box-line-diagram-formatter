from factories.EntityFactory import EntityFactory
from utils.Helpers import Helpers

class EntityManager:
    def __init__(self):
        pass
    
    def generate_entities(self, input_dict, grid_spacing):
        self.entities = []
        self.connections = []

        for mx_cell in input_dict:
            try:
                entity = EntityFactory.generate_entity(mx_cell, grid_spacing)
                if (entity.entity_type == Helpers.text_to_entity_type('Shape')):
                    self.entities.append(EntityFactory.generate_entity(mx_cell, grid_spacing))
                elif (entity.entity_type == Helpers.text_to_entity_type('Connection')):
                    self.connections.append(EntityFactory.generate_entity(mx_cell, grid_spacing))
            except Exception as e:
                Helpers.debug_print('Cannot create and assign entity:', e, debug_type = 'error')
                continue