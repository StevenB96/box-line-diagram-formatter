import xml.etree.ElementTree as ET

class Helpers:
    def __init__(self):
        pass

    @staticmethod
    def xml_string_to_dict(str):
        tokens = str.split(";")
        dict = {}
        for token in tokens:
            pair = token.split("=")
            if (len(pair) == 2):
                dict[pair[0]] = pair[1]
        for key in dict:
            try:
                dict[key] = int(dict[key])
            except ValueError:
                try:
                    dict[key] = float(dict[key])
                except ValueError:
                    pass
        return dict
    
    @staticmethod
    def dict_to_xml_string(dict):
        return ";".join([f"{key}={value}" for key, value in dict.items()]) + ";"

    @staticmethod
    def distance(coordinate_a, coordinate_b):
        x1, y1 = coordinate_a
        x2, y2 = coordinate_b
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
