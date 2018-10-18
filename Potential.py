class PotentialSim:
    def __init__(self, _grid_size_x, _grid_size_y, _steps_per_iteration):
        self.Grid = {}
        self.gridSizeX = _grid_size_x
        self.gridSizeY = _grid_size_y
        self.StepsPerIteration = _steps_per_iteration
        self._build_grid()
        self.set_initial_neighbors()
        self.create_initial_edge()

    class Tile:
        def __init__(self, location, item, field, canvas_id=None):
            self.location = location
            self.item = item
            self.field = field
            self.neighbors = []
            self.canvas_id = canvas_id

        def __repr__(self):
            return 'Location: ' + str(self.location) + '\n' + 'Item: ' + str(self.item) + '\n' \
                   + 'Field: ' + str(self.field) + '\n' + 'Canvas ID: ' + str(self.canvas_id)

        def calc_field_strength(self):
            if self.item == 'source':
                self.field = 255
            elif self.item == 'wall':
                pass
            elif self.item == 'sink':
                self.field = 0
            else:
                self.field = sum(tile.field for tile in self.neighbors)/float(len(self.neighbors))

    def set_initial_neighbors(self):
        for location, tile in self.Grid.items():
            for neighbor in self.find_neighbor_tiles(tile):
                if neighbor:
                    tile.neighbors.append(neighbor)

    def find_neighbor_tiles(self, tile):
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
        for tile in self.Grid[cell_position].neighbors:
            try:
                tile.neighbors.remove(self.Grid[cell_position])
            except ValueError:
                print('clicked: ' + str(cell_position) + ' failed to remove connection from: ' + str(tile.location))

        self.Grid[cell_position].neighbors.clear()

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


