from utils.FileManager import FileManager
from graph.model_space.ModelSpace import ModelSpace
from utils.TestSuite import TestSuite

if __name__ == '__main__':
    class Main:
        test_suite = TestSuite()
        file_manager = FileManager()
        file_manager.convert_xml('Example Input.xml', 'Example Input.json')
        root_cell = file_manager.root_cell
        grid_unit = file_manager.grid_unit
        model_space = ModelSpace(root_cell, grid_unit)
        model_space.optimise_model_space()

