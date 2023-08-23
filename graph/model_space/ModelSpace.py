from shapes.line.Line import Line
from shapes.rectangle.Rectangle import Rectangle
from graph.model.Model import Model
import random
from tqdm import tqdm
import copy
import time
import numpy as np
import math


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
        self.covariance = 1
        self.double_optimisation_coefficient = 0.25
        self.generate_shapes()
        self.generate_entity_relationships()
        self.update_entity_relationships()
        self.initial_forest_size = 1000 * len(self.initial_entities)
        self.top_forest_size = 5 * len(self.initial_entities)
        self.model_optimisation_time = 5 * len(self.initial_entities)
        self.set_canvas()
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
        print('Generating initial forest')
        for i in tqdm(range(self.initial_forest_size)):
            for entity in entities:
                random_grid_center = random.choice(random.choice(self.canvas))
                entity.set_grid_center(random_grid_center)
            self.update_connections(connections, entities)
            model = Model(connections, entities, self.grid_spacing)

            # Create a deep copy of the 'model' object and append the copy to the 'models' list
            models.append(copy.deepcopy(model))

        sorted_models = []
        print('Evaluating initial forest')
        for model in tqdm(models):
            sorted_models.append((model.get_penalty(), model))
        sorted_models = [model for penalty, model in sorted_models]
        self.models = sorted_models

    def optimise_model_space(self):
        best_model = self.models[0]
        print('Optimising forest')
        for model in tqdm(self.models[0:self.top_forest_size]):
            modified_models = []
            # Create a deep copy of the 'entities' and 'connections' lists
            entities = copy.deepcopy(model.entities)
            connections = copy.deepcopy(model.connections)
            last_improvement_time = time.monotonic()
            last_covariance_doubling_time = time.monotonic()
            while True:
                improvement_time_difference = time.monotonic() - last_improvement_time
                if improvement_time_difference > self.model_optimisation_time:
                    self.covariance = 1
                    break
                doubling_time_time_difference = time.monotonic() - last_covariance_doubling_time
                if doubling_time_time_difference > self.model_optimisation_time * self.double_optimisation_coefficient:
                    self.covariance *= 2
                    last_covariance_doubling_time = time.monotonic()
                random_index = random.randrange(len(entities))
                random_entity = entities[random_index]
                original_grid_center = random_entity.grid_center()

                # Use a multivariate normal distribution
                x, y = original_grid_center
                mean = [x // (self.grid_spacing * self.grid_gap), y // (self.grid_spacing * self.grid_gap)]
                cov = [[self.covariance, 0], [0, self.covariance]]

                # Generate new valid grid center
                new_pos = np.random.multivariate_normal(mean, cov)
                new_x, new_y = int(round(new_pos[0])), int(round(new_pos[1]))
                new_x_is_valid = len(self.canvas[0]) - 1 >= new_x >= 0 and new_x != x
                new_y_is_valid = len(self.canvas) - 1 >= new_y >= 0 and new_y != y
                while (not new_x_is_valid or not new_y_is_valid):
                    new_pos = np.random.multivariate_normal(mean, cov)
                    new_x, new_y = int(round(new_pos[0])), int(round(new_pos[1]))
                    new_x_is_valid = len(self.canvas[0]) - 1 >= new_x >= 0 and new_x != x
                    new_y_is_valid = len(self.canvas) - 1 >= new_y >= 0 and new_y != y

                random_grid_center = self.canvas[new_y][new_x]
                random_entity.set_grid_center(random_grid_center)
                self.update_connections(connections, entities)
                model = Model(connections, entities, self.grid_spacing)
                if modified_models and model.get_penalty() < min([model.get_penalty() for model in modified_models]):
                    last_improvement_time = time.monotonic()
                else:
                    # Undo if change is not an improvement
                    random_entity.set_grid_center(original_grid_center)
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
        grid_size = self.get_grid_size()
        grid = []
        for y in range(0, grid_size[1], self.grid_spacing * self.grid_gap):
            row = []
            for x in range(0, grid_size[0], self.grid_spacing * self.grid_gap):
                row.append((x + self.grid_spacing * self.grid_gap,
                           y + self.grid_spacing * self.grid_gap))
            grid.append(row)
        self.canvas = grid

    def get_grid_size(self):
        entities_by_parent_depth = sorted(
            self.initial_entities, key=lambda x: - x.parent_depth)
        entity_parent_depth = entities_by_parent_depth[0].parent_depth
        parent_depths = [
            entity.parent_depth for entity in entities_by_parent_depth]
        max_parent_depth = max(parent_depths)
        width = self.round_to_grid(
            (max_parent_depth + 2) * self.grid_spacing * self.grid_gap)
        height = self.round_to_grid(
            (entity_parent_depth + 2) * self.grid_spacing * self.grid_gap)
        return (width, height)
