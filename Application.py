from tkinter import *
import tkinter.ttk as ttk
import Potential


class Application(object):
    def __init__(self, master):
        self.master = master
        self.steps_per_iteration = 1
        self.animation_speed = 10
        self.cell_height, self.cell_width = 20, 20
        self.num_x_cells, self.num_y_cells = 31, 31
        self.total_x_size, self.total_y_size = self.cell_width * self.num_x_cells, self.cell_height * self.num_y_cells
        self.default_conductivity = 20.0
        self.pipe_conductivity = 2.0
        self.left_click_item = 'source'

        self.myCanvas = None
        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.button4 = None
        self.button5 = None

        self.build_widgets()
        self.widget_grid_assignment()

        self.mySimulation = Potential.PotentialSim(
            self.num_x_cells, self.num_y_cells, self.steps_per_iteration, self.pipe_conductivity, self.default_conductivity)

        self.build_visual_grid('red')
        self.mySimulation.Grid[15, 15].item = 'source'

        self.master.after(0, self.animate)

    def animate(self):
        self.mySimulation.do_simulation()
        self.update_visual_grid()
        self.master.after(self.animation_speed, self.animate)

    def set_left_click(self, item):
        self.left_click_item = item
        # print(item)

    def test(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        print(self.mySimulation.Grid[cell_position])

    def left_click_callback(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        if self.left_click_item == "test":
            self.test(event)
            return

        self.mySimulation.Grid[cell_position].item = self.left_click_item

        if self.left_click_item == "wall":
            self.mySimulation.remove_connections(cell_position)
        elif self.left_click_item == "pipe":
            self.mySimulation.change_conductivity(cell_position)

    def middle_click_callback(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        self.mySimulation.Grid[cell_position].item = "sink"

    def right_click_callback(self, event):
        cell_position = self.find_cell_from_position(event.x, event.y)
        self.mySimulation.Grid[cell_position].item = "wall"
        self.mySimulation.remove_connections(cell_position)

    def build_widgets(self):
        self.myCanvas = self.build_canvas()
        self.button1 = ttk.Button(self.master, text="Source",
                                  command=(lambda item="source": self.set_left_click(item)))
        self.button2 = ttk.Button(self.master, text="Wall",
                                  command=(lambda item="wall": self.set_left_click(item)))
        self.button3 = ttk.Button(self.master, text="Sink",
                                  command=(lambda item="sink": self.set_left_click(item)))
        self.button4 = ttk.Button(self.master, text="Pipe",
                                  command=(lambda item="pipe": self.set_left_click(item)))
        self.button5 = ttk.Button(self.master, text="test",
                                  command=(lambda item="test": self.set_left_click(item)))

    def widget_grid_assignment(self):
        self.myCanvas.grid(row=1, column=1, columnspan=5)
        self.button1.grid(row=2, column=1, pady=10)
        self.button2.grid(row=2, column=2, pady=10)
        self.button3.grid(row=2, column=3, pady=10)
        self.button4.grid(row=2, column=4, pady=10)
        self.button5.grid(row=2, column=5, pady=10)

    def build_canvas(self):
        canvas = Canvas(self.master, width=self.total_x_size, height=self.total_y_size)
        canvas.bind("<Button-1>", self.left_click_callback)
        canvas.bind("<Button-2>", self.middle_click_callback)
        canvas.bind("<Button-3>", self.right_click_callback)
        canvas.bind("<B1-Motion>", self.left_click_callback)
        canvas.bind("<B2-Motion>", self.middle_click_callback)
        canvas.bind("<B3-Motion>", self.right_click_callback)
        return canvas

    def build_visual_grid(self, default_color):
        for location, tile in self.mySimulation.Grid.items():
            bounds = self.get_cell_bounds(location)
            tile.canvas_id = self.myCanvas.create_rectangle(*bounds, fill=default_color)

    def update_visual_grid(self):
        for location, tile in self.mySimulation.Grid.items():
            if tile.item == 'wall':
                self.myCanvas.itemconfig(tile.canvas_id, outline=self.color_picker(0, 255, 0))
            elif tile.item == 'sink':
                self.myCanvas.itemconfig(tile.canvas_id, outline=self.color_picker(255, 255, 255))
            elif tile.item == 'source':
                self.myCanvas.itemconfig(tile.canvas_id, outline=self.color_picker(255, 255, 0))
            elif tile.item == 'pipe':
                self.myCanvas.itemconfig(tile.canvas_id, outline=self.color_picker(0, 0, 255))
            else:
                pass
            red = int(tile.field / 2)
            if tile.field > 255:
                green = tile.field - 255
            else:
                green = 0
            self.myCanvas.itemconfig(tile.canvas_id, fill=self.color_picker(red, green, 0))

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


if __name__ == "__main__":
    root = Tk()
    root.title("Potential Mapping")
    app = Application(root)
    root.mainloop()
