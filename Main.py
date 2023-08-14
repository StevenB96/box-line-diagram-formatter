from utils.FileManager import FileManager
from utils.EntityManager import EntityManager
from utils.CoordinateManager import CoordinateManager

file_manager = FileManager()
file_manager.convert_xml_to_json('Example Input.xml', 'Example Input.json')
entity_manager = EntityManager()
entity_manager.generate_entities(file_manager.root_mx_cell, file_manager.grid_spacing)
coordinate_manager = CoordinateManager(entity_manager.entities, entity_manager.connections, file_manager.grid_spacing)
coordinate_manager.optimise_coordinates()