from shapes.line.Line import Line
from shapes.rectangle.Rectangle import Rectangle

class ModelSpace:
    def __init__(self, root_cell, grid_spacing):
        self.root_cell = root_cell
        self.grid_spacing = grid_spacing
        self.connections = []
        self.entities = []
        self.generate_shapes()
        print(len(self.connections))
        print(len(self.entities))
        # for i in self.connections + self.entities:
        #     print(i, '\n')

    def generate_shapes(self):
        for cell in self.root_cell:
            try:
                if '@vertex' in cell:
                    rectangle = Rectangle(cell, self.grid_spacing)
                    self.entities.append(rectangle)
                elif '@source' in cell and '@target' in cell:
                    if not ('mxGeometry' in cell and 'Array' in cell['mxGeometry']):
                        line = Line(cell, self.grid_spacing)
                        self.connections.append(line)
            except Exception as e:
                print(e)
        self.update_shapes()

    def update_shapes(self):
        for connection in self.connections:
            if (connection.type == 'Line'):
                # Find the source entity in the entities list
                source_entity = next((entity for entity in self.entities if entity.id == connection.source), None)
                if source_entity is None:
                    print("Cannot find source entity for connection", connection)
                    continue
                
                # Find the target entity in the entities list
                target_entity = next((entity for entity in self.entities if entity.id == connection.target), None)
                if target_entity is None:
                    print("Cannot find target entity for connection", connection)
                    continue
                # Set the connections coordinates based on the entity coordinates
                connection.set_coordinates(source_entity, target_entity)