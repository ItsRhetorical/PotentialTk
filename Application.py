from tkinter import *
import Potential


class Application(object):
    def __init__(self, master):
        self.master = master
        self.steps_per_iteration = 20
        self.cell_height, self.cell_width = 10, 10
        self.num_x_cells, self.num_y_cells = 100, 100
        self.total_x_size, self.total_y_size = self.cell_width * self.num_x_cells, self.cell_height * self.num_y_cells

        self.myCanvas = Canvas(self.master, width=self.total_x_size, height=self.total_y_size)
        self.myCanvas.pack()

        self.build_visual_grid('red')

        self.mySimulation = Potential.PotentialSim(self.num_x_cells, self.num_y_cells, self.steps_per_iteration)
        self.mySimulation.Grid[5, 5].item = 'source'
        self.myCanvas.pack()
        self.master.after(0, self.animate)

    def build_visual_grid(self, default_color):
        for y in range(self.num_y_cells):
            for x in range(self.num_x_cells):
                bounds = self.get_cell_bounds(x, y, self.cell_width, self.cell_height)
                self.myCanvas.create_rectangle(*bounds, fill=default_color)

    def update_visual_grid(self):
        for location, tile in self.mySimulation.Grid.items():
            bounds = self.get_cell_bounds(location[0], location[1], self.cell_width, self.cell_height)
            self.myCanvas.create_rectangle(*bounds,
                                           fill=self.color_picker(self.mySimulation.Grid[location].field, 0, 0))

    def get_cell_bounds(self, x, y, size_cell_x, size_cell_y):
        x0 = x * size_cell_x
        x1 = (x + 1) * size_cell_x
        y0 = y * size_cell_y
        y1 = (y + 1) * size_cell_y
        return x0, y0, x1, y1

    def color_picker(self, r, g, b):
        color = '#%02x%02x%02x' % (int(r), int(g), int(b))
        return color

    def animate(self):
        self.mySimulation.do_simulation()
        self.update_visual_grid()
        print('now')
        self.master.after(12, self.animate)


root = Tk()
root.title("Potential Mapping")
app = Application(root)
root.mainloop()
