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

    def __init__(self):
        pass
    
    @staticmethod
    def round_to_grid(number, grid_spacing):
        return round(number / grid_spacing) * grid_spacing

    @staticmethod
    def type_to_text(type):
        # Helper method to convert the `type` to a human-readable string
        try:
            dict = {}
            dict[0] = 'Jagged Line'
            dict[1] = 'Straight Line'
            dict[2] = 'Rectangle'
            return dict[type]
        except Exception as e:
            print(e)
            return ''
        
    @staticmethod
    def entity_type_to_text(type):
        # Helper method to convert the `type` to a human-readable string
        try:
            dict = {}
            dict[0] = 'Shape'
            dict[1] = 'Connection'
            return dict[type]
        except Exception as e:
            print(e)
            return ''
        
    @staticmethod
    def text_to_type(type):
        # Helper method to convert the `type` to a value
        try:
            dict = {}
            dict['Jagged Line'] = 0
            dict['Straight Line'] = 1
            dict['Rectangle'] = 2
            return dict[type]
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def text_to_entity_type(type):
        # Helper method to convert the `type` to a value
        try:
            dict = {}
            dict['Shape'] = 0
            dict['Connection'] = 1
            return dict[type]
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def xml_string_to_dict(str):
        tokens = str.split(";")
        dict = {}
        for token in tokens:
            pair = token.split("=")
            # Assign the key and value to the dictionary
            if (len(pair) == 2):
                dict[pair[0]] = pair[1]
        # Convert the values to integers or floats if possible
        for key in dict:
            try:
                dict[key] = int(dict[key])
            except ValueError:
                try:
                    dict[key] = float(dict[key])
                except ValueError:
                    pass
        # Return the dictionary
        return dict
    
    @staticmethod
    def order_objects_by_attribute(objects, attr, order):
        """
        Sort an array of shapes by a dict attribute following a custom order.

        Args:
            attr (str): The name of the attribute to sort by.
            order (list): The custom order of the attribute values.

        Returns:
            The same array of shapes sorted by the attribute following the custom order.
        """
        # Convert the order list to a dictionary with values as keys and indexes as values
        order_dict = {val: i for i, val in enumerate(order)}
        # Sort the shapes array using the order dictionary to determine the order of attribute values
        return sorted(objects, key=lambda x: order_dict.get(x[attr], len(order_dict)))