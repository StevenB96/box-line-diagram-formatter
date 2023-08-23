from utils.FileManager import FileManager
from graph.model_space.ModelSpace import ModelSpace
from utils.TestSuite import TestSuite

class Main:
    test_suite = TestSuite()
    file_manager = FileManager()
    file_manager.convert_xml('Example Input.xml', 'Example Input.json')
    root_cell = file_manager.root_cell
    grid_spacing = file_manager.grid_spacing
    model_space = ModelSpace(root_cell, grid_spacing)
    model_space.optimise_model_space()