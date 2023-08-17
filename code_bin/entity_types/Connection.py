from utils.Helpers import Helpers

class Connection:
    def __init__(self, entity_dictionary = None, grid_spacing = None):
        if entity_dictionary != None:
            self.entity_dictionary = entity_dictionary
        if grid_spacing != None:
            self.grid_spacing = grid_spacing

    @property
    def id(self):
        try:
            return self.entity_dictionary['@id']
        except Exception as e:
            Helpers.debug_print('Cannot define id attribute:', e, debug_type = 'error')
            return None
    
    @property
    def text(self):
        try:
            return self.entity_dictionary['@value']
        except Exception as e:
            Helpers.debug_print('Cannot define text attribute:', e, debug_type = 'error')
            return None

    @property
    def style(self):
        try:
            return Helpers.xml_string_to_dict(self.entity_dictionary['@style'])
        except Exception as e:
            Helpers.debug_print('Cannot define style attribute:', e, debug_type = 'error')
            return None

    @property
    def source(self):
        try:
            return self.entity_dictionary['@source']
        except Exception as e:
            Helpers.debug_print('Cannot define source attribute:', e, debug_type = 'error')
            return None

    @property
    def target(self):
        try:
            return self.entity_dictionary['@target']
        except Exception as e:
            Helpers.debug_print('Cannot define target attribute:', e, debug_type = 'error')
            return None
        
    @property
    def lines(self):
        try:
            lines = []
            for i in range(len(self.coordinates)):
                if i == len(self.coordinates) - 1:
                    lines.append((self.coordinates[i], self.coordinates[0]))
                else:
                    lines.append((self.coordinates[i], self.coordinates[i+1]))
            return lines
        except Exception as e:
            Helpers.debug_print('Cannot define lines attribute:', e, debug_type = 'error')
            return None
    
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            raise KeyError(f"Invalid key '{key}'")