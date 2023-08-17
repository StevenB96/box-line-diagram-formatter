from entity.Entity import Entity
from connection.Connection import Connection

class Model:
    def __init__(self):
        self.entity = Entity()
        self.connection = Connection()
        print('Model')