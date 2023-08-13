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