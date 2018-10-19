class PotentialSim:
    def __init__(self, _grid_size_x, _grid_size_y, _steps_per_iteration, pipe_conductivity, default_conductivity):
        self.Grid = {}
        self.gridSizeX = _grid_size_x
        self.gridSizeY = _grid_size_y
        self.StepsPerIteration = _steps_per_iteration
        self.pipe_conductivity = pipe_conductivity
        self.default_conductivity = default_conductivity
        self._build_grid()
        self.set_initial_neighbors()
        self.create_initial_edge()

    class Tile:
        def __init__(self, location, item, field, canvas_id=None):
            self.location = location
            self.item = item
            self.field = field
            # TODO conductivity is really resistivity
            self.neighbor_conductivity = {}
            self.canvas_id = canvas_id
            self.source_growth = 100
            self.sink_drain = 50

        def __repr__(self):
            return 'Location: ' + str(self.location) + '\n' + 'Item: ' + str(self.item) + '\n' \
                   + 'Field: ' + str(self.field) + '\n' + 'Canvas ID: ' + str(self.canvas_id) \
                    + '\n' + 'NC: ' + str(self.neighbor_conductivity.values())

        def calc_field_strength(self):

            if self.item == 'wall':
                pass
            else:
                self.field = sum(tile.field/conductivity for tile, conductivity in self.neighbor_conductivity.items())/ \
                             sum(1 / conductivity for tile, conductivity in self.neighbor_conductivity.items())

            if self.item == 'source':
                self.field += self.source_growth
                if self.field > 510:
                    self.field = 510
            elif self.item == 'sink':
                self.field -= self.sink_drain
                if self.field < 0:
                    self.field = 0

    def set_initial_neighbors(self):
        for location, tile in self.Grid.items():
            for neighbor in self.find_initial_neighbor_tiles(tile):
                if neighbor:
                    tile.neighbor_conductivity[neighbor] = self.default_conductivity

    def find_initial_neighbor_tiles(self, tile):
        neighbor_list = []
        try:
            neighbor_list.append(self.Grid[tile.location[0] - 1, tile.location[1]])
        except KeyError:
            pass
        try:
            neighbor_list.append(self.Grid[tile.location[0], tile.location[1] + 1])
        except KeyError:
            pass
        try:
            neighbor_list.append(self.Grid[tile.location[0] + 1, tile.location[1]])
        except KeyError:
            pass
        try:
            neighbor_list.append(self.Grid[tile.location[0], tile.location[1] - 1])
        except KeyError:
            pass
        return neighbor_list

    def remove_connections(self, cell_position):
        for tile in self.Grid[cell_position].neighbor_conductivity:
            try:
                del tile.neighbor_conductivity[self.Grid[cell_position]]
            except ValueError:
                print('clicked: ' + str(cell_position) + ' failed to remove connection from: ' + str(tile.location))

        self.Grid[cell_position].neighbor_conductivity.clear()

    def change_conductivity(self, cell_position):
        tile = self.Grid[cell_position]
        for neighbor in tile.neighbor_conductivity:
            if neighbor.item == 'pipe':
                tile.neighbor_conductivity[neighbor] = self.pipe_conductivity
                for reverse_connection in neighbor.neighbor_conductivity:
                    if reverse_connection.item == 'pipe':
                        neighbor.neighbor_conductivity[reverse_connection] = self.pipe_conductivity

    def _build_grid(self):
        for x in range(self.gridSizeX):
            for y in range(self.gridSizeY):
                tile = self.Tile((x, y), "", 0)
                self.Grid[x, y] = tile

    def do_simulation(self):
        for i in range(self.StepsPerIteration):
            for location, tile in self.Grid.items():
                tile.calc_field_strength()

    def create_initial_edge(self):
        for location, tile in self.Grid.items():
            if location[0] == 0 or location[0] == self.gridSizeX - 1 \
                    or location[1] == 0 or location[1] == self.gridSizeY - 1:
                tile.item = 'sink'


