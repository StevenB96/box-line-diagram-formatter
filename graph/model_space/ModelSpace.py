from shapes.line.Line import Line
from shapes.rectangle.Rectangle import Rectangle
from graph.model.Model import Model


class ModelSpace:
    def __init__(self, root_cell, grid_spacing):
        self.root_cell = root_cell
        self.grid_spacing = grid_spacing
        self.connections = []
        self.entities = []
        self.entity_relationships = []
        self.generate_shapes()
        # self.entities[0].set_grid_center([400,200])
        self.update_shapes()
        self.generate_entity_relationships()
        self.update_entity_relationships()
        
        model = Model(self.connections, self.entities, self.grid_spacing)
        model.get_intersections_count()
        # model.display()

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
        self.update_connections()

    def update_connections(self):
        for connection in self.connections:
            if (connection.type == 'Line'):
                source_entity = next(
                    (entity for entity in self.entities if entity.id() == connection.source()), None)
                target_entity = next(
                    (entity for entity in self.entities if entity.id() == connection.target()), None)
                connection.set_coordinates(source_entity, target_entity)

    def generate_entity_relationships(self):
        entity_relationship_dict = {}
        for entity in self.entities:
            entity_id = entity.id()
            entity_relationship_dict[entity_id] = {'parents': [], 'children': []}
            for connection in self.connections:
                source_id = connection.source()
                target_id = connection.target()
                if source_id == entity_id:
                    entity_relationship_dict[entity_id]['children'].append(target_id)
                if target_id == entity_id:
                    entity_relationship_dict[entity_id]['parents'].append(source_id)
        self.set_entity_relationships(entity_relationship_dict)

    def set_entity_relationships(self, entity_relationship_dict):
        entity_id_set = [entity.id() for entity in self.entities]
        self.entity_relationships.append(entity_id_set)
        for entity in self.entities:
            entity_id = entity.id()
            row = []
            for other_entity in self.entities:
                if other_entity.id() == entity_id:
                    row.append(0)
                elif other_entity.id() in entity_relationship_dict[entity_id]['parents']:
                    row.append(1)
                elif other_entity.id() in entity_relationship_dict[entity_id]['children']:
                    row.append(-1)
                else:
                    row.append(0)
            self.entity_relationships.append(row)

    def update_entity_relationships(self):
        for entity in self.entities:
            entity.set_relationships_list(self.entity_relationships)

    def optimise_model(self):
        pass