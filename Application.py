from tkinter import *
import Potential

class Application(object):
    def __init__(self, master):
        self.master = master
        self.steps_per_iteration = 1
        self.animation_speed = 10
        self.cell_height, self.cell_width = 10, 10
        self.num_x_cells, self.num_y_cells = 50, 50
        self.total_x_size, self.total_y_size = self.cell_width * self.num_x_cells, self.cell_height * self.num_y_cells
        self.myCanvas = self.build_canvas()
        self.mySimulation = Potential.PotentialSim(self.num_x_cells, self.num_y_cells, self.steps_per_iteration)
        self.build_visual_grid('red')

        self.mySimulation.Grid[5, 5].item = 'source'
        self.myCanvas.pack()
        self.master.after(0, self.animate)

    def animate(self):
        self.mySimulation.do_simulation()
        self.update_visual_grid()
        self.master.after(self.animation_speed, self.animate)

    def left_click_callback(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        self.mySimulation.Grid[cell_position].item = "source"

    def middle_click_callback(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        self.mySimulation.Grid[cell_position].item = "sink"

    def right_click_callback(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        self.mySimulation.Grid[cell_position].item = "wall"
        self.mySimulation.remove_connections(cell_position)

    def build_canvas(self):
        canvas = Canvas(self.master, width=self.total_x_size, height=self.total_y_size)
        canvas.bind("<Button-1>", self.left_click_callback)
        canvas.bind("<Button-2>", self.middle_click_callback)
        canvas.bind("<Button-3>", self.right_click_callback)
        canvas.bind("<B1-Motion>", self.left_click_callback)
        canvas.bind("<B2-Motion>", self.middle_click_callback)
        canvas.bind("<B3-Motion>", self.right_click_callback)
        canvas.pack()
        return canvas

    def build_visual_grid(self, default_color):
        for location, tile in self.mySimulation.Grid.items():
            bounds = self.get_cell_bounds(location)
            tile.canvas_id = self.myCanvas.create_rectangle(*bounds, fill=default_color)

    def update_visual_grid(self):
        for location, tile in self.mySimulation.Grid.items():
            if tile.item == 'wall':
                self.myCanvas.itemconfig(tile.canvas_id, fill=self.color_picker(0, 255, 0))
            elif tile.item == 'sink':
                self.myCanvas.itemconfig(tile.canvas_id, fill=self.color_picker(255, 255, 255))
            elif tile.item == 'source':
                self.myCanvas.itemconfig(tile.canvas_id, fill=self.color_picker(255, 255, 0))
            else:
                self.myCanvas.itemconfig(tile.canvas_id, fill=self.color_picker(tile.field, 0, 0))

    def get_cell_bounds(self, location):
        x = location[0]
        y = location[1]
        x0 = x * self.cell_width
        x1 = (x + 1) * self.cell_width
        y0 = y * self.cell_height
        y1 = (y + 1) * self.cell_height
        return x0, y0, x1, y1

    def find_cell_from_position(self, x, y):
        cell_x = x // self.cell_width
        cell_y = y // self.cell_height
        return cell_x, cell_y

    def color_picker(self, r, g, b):
        color = '#%02x%02x%02x' % (int(r), int(g), int(b))
        return color


root = Tk()
root.title("Potential Mapping")
app = Application(root)
root.mainloop()
