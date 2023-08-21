from utils.ModelSpaceItem import ModelSpaceItem


class Entity(ModelSpaceItem):
    def __init__(self):
        self.parent_list = []
        self.child_list = []

    def grid_center(self):
        x = [p[0] for p in self.coordinate_set()]
        y = [p[1] for p in self.coordinate_set()]
        centroid = (self.round_to_grid(sum(x) / len(self.coordinate_set())),
                    self.round_to_grid(sum(y) / len(self.coordinate_set())))
        return centroid

    def set_grid_center(self, coordinates):
        self.cell['mxGeometry']['@x'] = str(
            self.round_to_grid(coordinates[0] - 0.5 * self.width()))
        self.cell['mxGeometry']['@y'] = str(
            self.round_to_grid(coordinates[1] - 0.5 * self.height()))
        
    def set_relationships_list(self, entity_relationships):
        def get_children_and_parents(index):
            indexes = [sub_list[index] for sub_list in entity_relationships][1:]
            parents = [i for i, v in enumerate(indexes) if v == 1 for _ in range(2)]
            children = [i for i, v in enumerate(indexes) if v == -1 for _ in range(2)]
            return set(parents), set(children)

        parents = set()
        children = set()
        entity_index = entity_relationships[0].index(self.id())

        parents_buffer = [entity_index]
        children_buffer = [entity_index]
        while parents_buffer or children_buffer:
            parents |= set(parent_index for index in parents_buffer for parent_index in get_children_and_parents(index)[0])
            children |= set(child_index for index in children_buffer for child_index in get_children_and_parents(index)[1])
            parents_buffer = [index for parent_index in parents_buffer for index in get_children_and_parents(parent_index)[0]]
            children_buffer = [index for child_index in children_buffer for index in get_children_and_parents(child_index)[1]]
            
        self.parent_list = [entity_relationships[0][i] for i in list(parents)]
        self.child_list = [entity_relationships[0][i] for i in list(children)]
