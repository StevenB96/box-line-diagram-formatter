from utils.FileManager import FileManager
from utils.ShapeManager import ShapeManager
from utils.CoordinateManager import CoordinateManager

file_manager = FileManager()
file_manager.convert_xml_to_json('Example Input.xml', 'Example Input.json')
shape_manager = ShapeManager()
shapes = shape_manager.generate_shapes(file_manager.root_mx_cell, file_manager.grid_spacing)
coordinate_manager = CoordinateManager(shapes)
coordinate_manager.optimise_coordinates(file_manager.grid_spacing)