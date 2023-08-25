import xml.etree.ElementTree as ET
import xmltodict
import json

class FileManager:
    def __init__(self):
        pass
    
    def convert_xml(self, input_filename, output_filename):
        # Parsing the input XML file into an ElementTree object
        input_tree = ET.parse(input_filename)
        # Getting the root element of the ElementTree
        input_root = input_tree.getroot()
        # Converting the ElementTree to an XML string
        input_str = ET.tostring(input_root, encoding='utf8', method='xml')
        # Parsing the XML string to a Python dictionary using `xmltodict`
        self.input_dict = xmltodict.parse(input_str)
        # Converting the Python dictionary to a JSON string
        input_json = json.dumps(self.input_dict)

        # Writing the JSON string to the output file
        self.write_json_to_file(output_filename, input_json)

        # Extract optimisation parameters
        self.extract_optimisation_parameters()
    
    def write_json_to_file(self, output_filename, input_json):
        # Writing the JSON string to the output file
        with open(output_filename, "w") as outfile:
            outfile.write(input_json)

    def extract_optimisation_parameters(self):
        self.grid_unit = int(self.input_dict['mxfile']['diagram']['mxGraphModel']['@gridSize'])
        self.root_cell = self.input_dict['mxfile']['diagram']['mxGraphModel']['root']['mxCell'][2:]