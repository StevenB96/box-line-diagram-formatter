import sys

class Helpers:
    DISPLAY_ATTRS = [
        'id', 
        'text', 
        'coordinates', 
        'type',
        'grid_center'
    ]
        
    REQUIRED_ATTRS = [
        'id', 
        'text', 
        'coordinates', 
        'type'
    ]

    DEBUG_TYPES = {
        0: None,
        1: 'message',
        2: 'error',
    }

    DEBUG_LEVEL = 2

    def __init__(self):
        pass

    @staticmethod
    def debug_print(*args, debug_type='message', **kwargs):
        if debug_type == Helpers.DEBUG_TYPES[Helpers.DEBUG_LEVEL]:
            print(*args, **kwargs)
        elif debug_type == Helpers.DEBUG_TYPES[Helpers.DEBUG_LEVEL]:
            print(*args, **kwargs)

    @staticmethod
    def round_to_grid(number, grid_spacing):
        return round(number / grid_spacing) * grid_spacing

    @staticmethod
    def type_to_text(type):
        try:
            dict = {}
            dict[0] = 'Jagged Line'
            dict[1] = 'Straight Line'
            dict[2] = 'Rectangle'
            return dict[type]
        except Exception as e:
            Helpers.debug_print('Cannot convert type to text:', e, debug_type = 'error')
            return ''
        
    @staticmethod
    def entity_type_to_text(type):
        try:
            dict = {}
            dict[0] = 'Shape'
            dict[1] = 'Connection'
            return dict[type]
        except Exception as e:
            Helpers.debug_print('Cannot convert entity type to text:', e, debug_type = 'error')
            return ''
        
    @staticmethod
    def text_to_type(type):
        try:
            dict = {}
            dict['Jagged Line'] = 0
            dict['Straight Line'] = 1
            dict['Rectangle'] = 2
            return dict[type]
        except Exception as e:
            Helpers.debug_print('Cannot convert text to type:', e, debug_type = 'error')
            return None
        
    @staticmethod
    def text_to_entity_type(type):
        try:
            dict = {}
            dict['Shape'] = 0
            dict['Connection'] = 1
            return dict[type]
        except Exception as e:
            Helpers.debug_print('Cannot convert text to entity type:', e, debug_type = 'error')
            return None
    
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
    def order_objects_by_attribute(objects, attr, order):
        order_dict = {val: i for i, val in enumerate(order)}
        return sorted(objects, key=lambda x: order_dict.get(x[attr], len(order_dict)))