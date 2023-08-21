from shape_types.connection.Connection import Connection


class Line(Connection):
    def __init__(self, cell, grid_spacing):
        self.cell = cell
        self.grid_spacing = grid_spacing
        self.shape_type = 'Connection'
        self.type = 'Line'
