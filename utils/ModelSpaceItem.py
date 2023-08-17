from utils.Helpers import Helpers

class ModelSpaceItem:
    def __init__(self):
        self.cell = None
        self.grid_spacing = None

    @property
    def id(self):
        try:
            return self.cell['@id']
        except Exception as e:
            print(e)
    
    @property
    def text(self):
        try:
            return self.cell['@value']
        except Exception as e:
            print(e)

    @property
    def style(self):
        try:
            return Helpers.xml_string_to_dict(self.cell['@style'])
        except Exception as e:
            print(e)

    @property
    def line_set(self):
        try:
            lines = []
            for i in range(len(self.coordinate_set)):
                if i == len(self.coordinate_set) - 1:
                    lines.append((self.coordinate_set[i], self.coordinate_set[0]))
                else:
                    lines.append((self.coordinate_set[i], self.coordinate_set[i+1]))
            return lines
        except Exception as e:
            print(e)

    def round_to_grid(self, number):
        return round(number / self.grid_spacing) * self.grid_spacing
        
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            raise KeyError(f"Invalid key '{key}'")
        
    def __str__(self):
        self_attributes = vars(self)
        self_attribute_list = list(self_attributes.items())
        string_attributes = [f"{value[0]}: {value[1]}" for value in self_attribute_list]
        property_attributes = [f"{attr_name}(): {getattr(self, attr_name)}" for attr_name in dir(self) if isinstance(getattr(type(self), attr_name, None), property)]
        string = '\n'.join(string_attributes + property_attributes)
        return string
    
