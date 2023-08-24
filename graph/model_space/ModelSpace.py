from shapes.line.Line import Line
from shapes.rectangle.Rectangle import Rectangle
from graph.model.Model import Model
import random
from tqdm import tqdm
import copy
import time
from collections import Counter


class ModelSpace:
    def __init__(self, root_cell, grid_spacing):
        # Set the initial model space
        self.root_cell = root_cell
        self.grid_spacing = grid_spacing
        self.connections = []
        self.initial_entities = []
        self.entity_relationships = []
        self.models = []
        self.grid_gap = 10
        self.generate_shapes()
        self.generate_entity_relationships()
        self.update_entity_relationships()
        self.initial_forest_size = 100 * len(self.initial_entities)
        self.top_forest_size = 1 * len(self.initial_entities)
        self.model_optimisation_time = 1 * len(self.initial_entities)        
        self.set_canvas()
        self.grid_info = {}
        self.generate_initial_forest()

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
            entity_relationship_dict[entity_id] = {
                'parents': [], 'children': []}
            for connection in self.connections:
                source_id = connection.source()
                target_id = connection.target()
                if source_id == entity_id:
                    entity_relationship_dict[entity_id]['children'].append(
                        target_id)
                if target_id == entity_id:
                    entity_relationship_dict[entity_id]['parents'].append(
                        source_id)
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

    def generate_initial_forest(self):
        # Create a deep copy of the 'entities' and 'connections' lists
        entities = copy.deepcopy(self.initial_entities)
        connections = copy.deepcopy(self.connections)

        models = []
        for i in tqdm(range(self.initial_forest_size), desc='Generating initial forest'):
            for entity in entities:
                random_grid_center = random.choice(random.choice(self.canvas))
                entity.set_grid_center(random_grid_center)
            self.update_connections(connections, entities)
            model = Model(connections, entities, self.grid_spacing)

            # Create a deep copy of the 'model' object and append the copy to the 'models' list
            models.append(copy.deepcopy(model))

        sorted_models = []

        for model in tqdm(models, desc='Evaluating initial forest'):
            model_penalty = model.get_penalty()
            if not sorted_models:
                sorted_models.append(model)
            else:
                for index, sorted_model in enumerate(sorted_models):
                    if model_penalty < sorted_model.get_penalty():
                        sorted_models.insert(index, model)
                        break
                    elif index == len(sorted_models) - 1:
                        sorted_models.append(model)
                        break
        
        self.models = sorted_models

    def optimise_model_space(self):
        best_model = self.models[0]
        for model in tqdm(self.models[0:self.top_forest_size], desc='Optimising forest'):
            modified_models = []
            # Create a deep copy of the 'entities' and 'connections' lists
            entities = copy.deepcopy(model.entities)
            connections = copy.deepcopy(model.connections)
            last_improvement_time = time.monotonic()
            while True:
                if time.monotonic() - last_improvement_time > self.model_optimisation_time:
                    break
                random_index = random.randrange(len(entities))
                random_entity = entities[random_index]
                random_grid_center = random.choice(random.choice(self.canvas))
                random_entity.set_grid_center(random_grid_center)
                self.update_connections(connections, entities)
                model = Model(connections, entities, self.grid_spacing)
                if modified_models and model.get_penalty() < min([model.get_penalty() for model in modified_models]):
                    last_improvement_time = time.monotonic()
                modified_models.append(copy.deepcopy(model))
            modified_models = sorted(
                modified_models, key=lambda x: - x.get_penalty())
            best_modification = modified_models[0]
            if (best_modification.get_penalty() < best_model.get_penalty()):
                best_model = best_modification

        print(best_model.get_penalty())
        print(best_model.get_size())
        print(best_model.get_intersections_count())
        best_model.display()

    def round_to_grid(self, number):
        return round(number / self.grid_spacing) * self.grid_spacing

    def set_canvas(self):
        self.set_grid_info()
        grid_info = self.grid_info
        grid = []
        for y in range(0, grid_info['height'], self.grid_spacing * self.grid_gap):
            row = []
            for x in range(0, grid_info['width'], self.grid_spacing * self.grid_gap):
                row.append((x + self.grid_spacing * self.grid_gap,
                           y + self.grid_spacing * self.grid_gap))
            grid.append(row)
        self.canvas = grid

    def set_grid_info(self):
        entities_by_parent_depth  = sorted(
            self.initial_entities, key=lambda x: - x.parent_depth)
        max_parent_depth = entities_by_parent_depth[0].parent_depth
        parent_depths = [entity.parent_depth for entity in entities_by_parent_depth]
        count_dict = Counter(parent_depths)
        most_common_parent_depth, most_common_parent_depth_count = count_dict.most_common(1)[0]
        width = self.round_to_grid((most_common_parent_depth_count + 1) * self.grid_spacing * self.grid_gap)
        height = self.round_to_grid((max_parent_depth + 1) * self.grid_spacing * self.grid_gap)
        grid_info = {}
        grid_info['width'] = width
        grid_info['height'] = height
        grid_info['most_common_parent_depth_count'] = most_common_parent_depth_count
        grid_info['max_parent_depth'] = max_parent_depth
        self.grid_info = grid_info
