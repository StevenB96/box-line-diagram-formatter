from shapes.line.Line import Line
from shapes.rectangle.Rectangle import Rectangle
from graph.model.Model import Model
import random
from tqdm import tqdm
import copy

class ModelSpace:
    def __init__(self, root_cell, grid_spacing):
        # Set the initial model space
        self.root_cell = root_cell
        self.grid_spacing = grid_spacing
        self.connections = []
        self.initial_entities = []
        self.entity_relationships = []
        self.initial_forest = 1000
        self.generate_shapes()
        self.generate_entity_relationships()
        self.update_entity_relationships()
        self.set_canvas()
        self.models = [Model(self.connections, self.initial_entities, self.grid_spacing)]

    def generate_shapes(self):
        for cell in self.root_cell:
            try:
                if '@vertex' in cell:
                    rectangle = Rectangle(cell, self.grid_spacing)
                    self.initial_entities.append(rectangle)
                elif '@source' in cell and '@target' in cell:
                    if not ('mxGeometry' in cell and 'Array' in cell['mxGeometry']):
                        line = Line(cell, self.grid_spacing)
                        self.connections.append(line)
            except Exception as e:
                print(e)
        self.update_connections(self.connections, self.initial_entities)

    def update_connections(self, connections, entities):
        for connection in connections:
            if (connection.type == 'Line'):
                source_entity = next(
                    (entity for entity in entities if entity.id() == connection.source()), None)
                target_entity = next(
                    (entity for entity in entities if entity.id() == connection.target()), None)
                connection.set_coordinates(source_entity, target_entity)

    def generate_entity_relationships(self):
        entity_relationship_dict = {}
        for entity in self.initial_entities:
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
        entity_id_set = [entity.id() for entity in self.initial_entities]
        self.entity_relationships.append(entity_id_set)
        for entity in self.initial_entities:
            entity_id = entity.id()
            row = []
            for other_entity in self.initial_entities:
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
        for entity in self.initial_entities:
            entity.set_relationships_list(self.entity_relationships)

    # def optimise_model(self):
    #     entities = copy.deepcopy(self.initial_entities)
    #     connections = copy.deepcopy(self.connections)
    #     for i in tqdm(range(self.initial_forest)):
    #         for entity in entities:
    #             grid_center = random.choice(random.choice(self.canvas))
    #             entity.set_grid_center(grid_center)
    #         self.update_connections(connections, entities)
    #         model = Model(connections, entities, self.grid_spacing)
    #         self.models.append(model)

    #     self.models = sorted(self.models, key=lambda x: x.get_score())
    #     for model in self.models:
    #         print(model.get_score())
    #         print(model.get_size())
    #         print(model.get_intersections_count())
    #     self.models[0].display()
    #     pass

    def round_to_grid(self, number):
        return round(number / self.grid_spacing) * self.grid_spacing
    
    def set_canvas(self):
        total_width = 0
        for entity in self.initial_entities:
            total_width += entity.width()       
        width = self.round_to_grid(total_width)
        grid = []
        for y in range(0, self.round_to_grid(width), self.grid_spacing * 10):
            row = []
            for x in range(0, self.round_to_grid(width), self.grid_spacing * 10):
                row.append((x, y))
            grid.append(row)
        self.canvas = grid