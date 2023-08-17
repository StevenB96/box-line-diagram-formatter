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