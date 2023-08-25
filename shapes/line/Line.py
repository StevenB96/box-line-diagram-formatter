from shape_types.connection.Connection import Connection


class Line(Connection):
    def __init__(self, cell, grid_unit):
        self.cell = cell
        self.grid_unit = grid_unit
        self.shape_type = 'Connection'
        self.type = 'Line'
