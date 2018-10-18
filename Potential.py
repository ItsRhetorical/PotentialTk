class PotentialSim:
    def __init__(self, _grid_size_x, _grid_size_y, _steps_per_iteration):
        self.Grid = {}
        self.gridSizeX = _grid_size_x
        self.gridSizeY = _grid_size_y
        self.StepsPerIteration = _steps_per_iteration
        self._build_grid()

    class Tile:
        def __init__(self, location, item, field):
            self.location = location
            self.item = item
            self.field = field

    def _build_grid(self):
        for x in range(self.gridSizeX):
            for y in range(self.gridSizeY):
                tile = self.Tile((x, y), "", 0)
                self.Grid[x, y] = tile

    def _average_neighbors(self, _x, _y):
        if _x == 0:
            left = 0
        else:
            left = self.Grid[_x - 1, _y].field

        if _y == 0:
            down = 0
        else:
            down = self.Grid[_x, _y - 1].field

        if _x == self.gridSizeX - 1:
            right = 0
        else:
            right = self.Grid[_x + 1, _y].field

        if _y == self.gridSizeY - 1:
            up = 0
        else:
            up = self.Grid[_x, _y + 1].field
        return (left + right + up + down)/4.0

    def do_simulation(self):
        for i in range(self.StepsPerIteration):
            for x in range(self.gridSizeX):
                for y in range(self.gridSizeY):
                    if self.Grid[x, y].item == "source":
                        self.Grid[x, y].field = 255
                    self.Grid[x, y].field = self._average_neighbors(x, y)
                    if self.Grid[x, y].item == "source":
                        self.Grid[x, y].field = 255



# Grid = {}
# cursor = [0, 0]
# lastKey = ""
# gridSizeX = 20
# gridSizeY = 20
# StepsPerIteration = 5
# TimePerStep = .3
# simulate = True


#
# def buildGrid():
#     for x in range(gridSizeX):
#         for y in range(gridSizeY):
#             tile = Tile((x, y), "", 0)
#             Grid[x, y] = tile


#
#
# buildGrid()
# while True:
#     time.sleep(TimePerStep)
#     if kbhit():
#         key = ord(getch())
#         if key == 120:  # x
#             print("Exit")
#             break
#         elif key == 32:  # space
#             print("Pause")
#             simulate = not simulate
#         elif key == 113:  # q
#             print("spawn")
#             Grid[cursor[0], cursor[1]].item = "source"
#             Grid[cursor[0], cursor[1]].field = 9
#             simulate = True
#         elif key == 97:  # a
#             print("left")
#             cursor[0] -= 1
#             simulate = False
#             drawScreen(Grid)
#         elif key == 100:  # d
#             print("right")
#             cursor[0] += 1
#             print(cursor)
#             simulate = False
#             drawScreen(Grid)
#         elif key == 119:  # w
#             print("up")
#             cursor[1] -= 1
#             simulate = False
#             drawScreen(Grid)
#         elif key == 115:  # s
#             print("down")
#             cursor[1] += 1
#             simulate = False
#             drawScreen(Grid)
#         new_cursor = [0 if i < 0 else i for i in cursor]  # change all negatives to 0
#         cursor = new_cursor
#     if simulate:
#         simulationIterations(StepsPerIteration)
#         drawScreen(Grid)










































