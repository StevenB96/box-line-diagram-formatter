from utils.FileManager import FileManager
from graph.model_space.ModelSpace import ModelSpace

class Main:
    FileManager = FileManager()
    FileManager.convert_xml('Example Input.xml', 'Example Input.json')
    root_cell = FileManager.root_cell
    grid_spacing = FileManager.grid_spacing
    ModelSpace = ModelSpace(root_cell, grid_spacing)
    # print(FileManager.grid_spacing, FileManager.root_mx_cell)