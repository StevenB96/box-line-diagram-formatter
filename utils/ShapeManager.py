from factories.ShapeFactory import ShapeFactory

class ShapeManager:
    def __init__(self):
        pass
    
    def generate_shapes(self, input_dict, grid_spacing):
        shapes = []

        # Iterate through all `mxCell`s in the root dictionary
        for mx_cell in input_dict:
            # If a `Shape` instance can be created from the `mxCell`, add it to the `shapes` list
            try:
                shapes.append(ShapeFactory.create_shape(mx_cell, grid_spacing))
            # If creating a `Shape` instance from the `mxCell` fails, skip it and move to the next one
            except Exception as e:
                print(e)
                continue

        return shapes