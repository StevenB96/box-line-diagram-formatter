from shapes.line.Line import Line
from shapes.rectangle.Rectangle import Rectangle
from graph.model.Model import Model
import random
from tqdm import tqdm
import copy
import time
from collections import Counter
import bisect
import itertools
import multiprocessing
import math
from functools import partial


class ModelSpace:
    def __init__(self, root_cell, grid_unit):
        # Set the initial model space
        self.root_cell = root_cell
        self.grid_unit = grid_unit
        self.connections = []
        self.initial_entities = []
        self.entity_relationships = []
        self.models = []
        self.grid_gap = grid_unit * 10
        self.grid_multiplier_x = 2
        self.grid_multiplier_y = 1.5
        self.generate_shapes()
        self.generate_entity_relationships()
        self.update_entity_relationships()
        model = Model(self.connections, self.initial_entities, self.grid_unit)
        model.display()
        self.initial_forest_size = 1 * len(self.initial_entities)
        self.top_forest_size = 5 * len(self.initial_entities)
        self.model_optimisation_time = 5 * len(self.initial_entities)
        self.grid_info = {}
        self.set_canvas()
        self.generate_initial_forest()

    def generate_shapes(self):
        for cell in self.root_cell:
            try:
                if '@vertex' in cell:
                    rectangle = Rectangle(cell, self.grid_unit)
                    self.initial_entities.append(rectangle)
                elif '@source' in cell and '@target' in cell:
                    if not ('mxGeometry' in cell and 'Array' in cell['mxGeometry']):
                        line = Line(cell, self.grid_unit)
                        self.connections.append(line)
            except Exception as e:
                print(e)
        self.update_connections(self.connections, self.initial_entities)

    def update_connection(self, connection, entities):
        if (connection.type == 'Line'):
            source_entity = next(
                (entity for entity in entities if entity.id() == connection.source()), None)
            target_entity = next(
                (entity for entity in entities if entity.id() == connection.target()), None)
            connection.set_coordinates(source_entity, target_entity)

    def update_connections(self, connections, entities):
        for connection in connections:
            self.update_connection(connection, entities)

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
        pbar = tqdm(total=self.initial_forest_size, desc='Generating initial forest')
        while len(models) < self.initial_forest_size:  # Continue until the models length is equal to initial_forest_size
            for entity in entities:
                random_position = self.generate_random_position(entity)
                random_grid_center = self.find_free_position(entities, random_position, entity)
                entity.set_grid_center(random_grid_center)
            self.update_connections(connections, entities)
            model = Model(connections, entities, self.grid_unit)

            # Create a deep copy of the 'model' object and append the copy to the 'models' list
            if model.get_intersections_count() < len(self.initial_entities) * 0.5:
                models.append(copy.deepcopy(model))
                pbar.update(1)  # Increment progress bar if a model is added

        pbar.close()
        
        sorted_models = []
        for model in tqdm(models, desc='Evaluating initial forest'):
            model_penalty = model.get_penalty()
            bisect.insort_left(sorted_models, model, key=lambda x: model_penalty)

        self.models = sorted_models

    def optimise_model_space_worker(self, model, model_optimisation_time, generate_random_position, find_free_position, update_connection):
        entities = model.entities
        connections = model.connections

        # Create a deep copy of the initial model that we will modify in each iteration
        new_model = copy.deepcopy(model)

        best_model = copy.deepcopy(model)
        best_penalty = best_model.get_penalty()

        last_improvement_time = time.monotonic()
        while True:
            if time.monotonic() - last_improvement_time > model_optimisation_time:
                break

            random_entity = random.choice(entities)
            random_position = generate_random_position(random_entity)
            random_grid_center = find_free_position(entities, random_position, random_entity)
            random_entity.set_grid_center(random_grid_center)

            connections_for_entity = itertools.filterfalse(
                lambda c: random_entity.id() not in [c.source(), c.target()], connections)

            for connection in connections_for_entity:
                update_connection(connection, entities)

            new_model.entities = entities
            new_model.connections = connections
            penalty = new_model.get_penalty()

            if penalty < best_penalty:
                best_model = copy.deepcopy(new_model)
                best_penalty = penalty
                last_improvement_time = time.monotonic()

        return best_model, best_penalty

    def optimise_model_space(self):
        models = self.models[:int(self.top_forest_size)]  # Get top models
        n_processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=n_processes)

        partial_fn = partial(
            self.optimise_model_space_worker,
            model_optimisation_time=self.model_optimisation_time,
            generate_random_position=self.generate_random_position,
            find_free_position=self.find_free_position,
            update_connection=self.update_connection
        )

        best_model = None
        best_penalty = float('inf')
        results_iter = pool.imap(partial_fn, models)
        with tqdm(total=len(models), desc='Optimising forest') as pbar:
            for result in results_iter:
                if result[1] < best_penalty:
                    best_model, best_penalty = result
                pbar.update()

        print(best_penalty)
        print(best_model.get_size())
        print(best_model.get_intersections_count())
        best_model.display()

    def generate_random_position(self, entity):
        grid_info = self.grid_info
        most_common_parent_depth_count = grid_info['most_common_parent_depth_count']
        max_parent_depth = grid_info['max_parent_depth']
        # Define the mean position and standard deviation
        center_x = (len(self.canvas[0]) * self.grid_multiplier_x) / 2
        center_y = entity.parent_depth * self.grid_multiplier_y
        mean_position = (center_x, center_y)  # for example
        std_deviation_y = max_parent_depth * 0.3  # for example
        std_deviation_x = most_common_parent_depth_count * 1

        # Generate a random position until a valid one is found
        while True:
            # Generate random position based on normal distribution
            # x_pos = random.randint(0, len(self.canvas[0]) - 1)
            x_pos = int(random.normalvariate(
                mean_position[0], std_deviation_x))
            y_pos = int(random.normalvariate(
                mean_position[1], std_deviation_y))

            # Check if the position is within the bounds of the matrix
            if 0 <= x_pos < len(self.canvas[0]) and 0 <= y_pos < len(self.canvas):
                # Found a valid position
                random_position = self.canvas[y_pos][x_pos]
                break

        return random_position

    def find_free_position(self, entities, position, entity):
        """Find a free position for an entity"""
        while position in [entity.grid_center for entity in entities]:
            # Move all entities currently occupying this position
            taken_entities = [
                entity for entity in entities if entity.grid_center() == position]
            for taken_entity in taken_entities:
                random_position = self.generate_random_position(taken_entity)
                new_position = self.find_free_position(
                    entities, random_position)
                taken_entity.set_grid_center(new_position)
            random_position = self.generate_random_position(entity)
            position = random_position
        return position

    def round_to_grid(self, number):
        return round(number / self.grid_unit) * self.grid_unit

    def round_to_gap(self, number):
        return round(number / self.grid_gap) * self.grid_gap

    def set_canvas(self):
        self.set_grid_info()
        grid_info = self.grid_info
        grid = []
        for y in range(0, grid_info['height'], self.grid_gap):
            row = []
            for x in range(0, grid_info['width'], self.grid_gap):
                row.append((x + self.grid_gap,
                           y + self.grid_gap))
            grid.append(row)
        self.canvas = grid

    def set_grid_info(self):
        entities_by_parent_depth = sorted(
            self.initial_entities, key=lambda x: - x.parent_depth)
        max_parent_depth = entities_by_parent_depth[0].parent_depth
        parent_depths = [
            entity.parent_depth for entity in entities_by_parent_depth]
        count_dict = Counter(parent_depths)
        most_common_parent_depth, most_common_parent_depth_count = count_dict.most_common(1)[
            0]
        width = self.round_to_gap(
            (most_common_parent_depth_count * self.grid_multiplier_x) * self.grid_gap)
        height = self.round_to_gap(
            (max_parent_depth + self.grid_multiplier_y) * self.grid_gap)
        grid_info = {}
        grid_info['width'] = width
        grid_info['height'] = height
        grid_info['most_common_parent_depth_count'] = most_common_parent_depth_count
        grid_info['max_parent_depth'] = max_parent_depth
        self.grid_info = grid_info
