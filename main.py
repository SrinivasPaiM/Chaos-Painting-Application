import tkinter as tk
from tkinter import Canvas, filedialog, messagebox
import random
import math

class ChaosBrushApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chaos Painting Application")

        self.canvas = Canvas(self.master, bg='white', width=800, height=600)
        self.canvas.pack()

        self.create_control_panel()

        self.start_x = None
        self.start_y = None
        self.drawing = False
        self.selection_rectangle = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def create_control_panel(self):

        self.shape_var = tk.StringVar(value='none')
        shape_menu = tk.OptionMenu(self.master, self.shape_var, 'none', 'dots', 'lines', 'zigzag', 'spirals', 'random_shapes')
        shape_menu.pack(pady=5)


        self.brush_size_var = tk.IntVar(value=10)
        brush_size_scale = tk.Scale(self.master, from_=1, to=50, label='Brush Size', orient=tk.HORIZONTAL, variable=self.brush_size_var)
        brush_size_scale.pack(pady=5)


        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        clear_button = tk.Button(button_frame, text="Clear Canvas", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(button_frame, text="Save Drawing", command=self.save_drawing)
        save_button.pack(side=tk.LEFT, padx=5)

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            try:
                self.canvas.postscript(file=file_path + '.eps')  # Save as EPS
                # Optionally, convert EPS to PNG using PIL or other methods if needed
                messagebox.showinfo("Save Drawing", "Drawing saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Drawing", f"Error saving drawing: {e}")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True
        self.selection_rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='blue', dash=(4, 2))

    def on_mouse_drag(self, event):
        if self.drawing:
            self.canvas.coords(self.selection_rectangle, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.drawing:
            self.drawing = False
            x1, y1, x2, y2 = self.canvas.coords(self.selection_rectangle)
            self.apply_chaos(x1, y1, x2, y2)
            self.canvas.delete(self.selection_rectangle)

    def apply_chaos(self, x1, y1, x2, y2):
        for _ in range(100):
            x = random.randint(int(min(x1, x2)), int(max(x1, x2)))
            y = random.randint(int(min(y1, y2)), int(max(y1, y2)))

            current_color = self.get_vibrant_color()

            chaos_style = self.shape_var.get()
            if chaos_style == 'dots':
                self.canvas.create_oval(x, y, x + self.brush_size_var.get(), y + self.brush_size_var.get(), fill=current_color, outline=current_color)
            elif chaos_style == 'lines':
                self.canvas.create_line(x, y, x + random.randint(-20, 20), y + random.randint(-20, 20), fill=current_color, width=self.brush_size_var.get())
            elif chaos_style == 'zigzag':
                self.draw_zigzag(x, y, current_color)
            elif chaos_style == 'spirals':
                self.draw_spiral(x, y, current_color)
            elif chaos_style == 'random_shapes':
                self.draw_random_shape(x, y, current_color)

    def draw_zigzag(self, start_x, start_y, color):
        for i in range(0, 100, 10):
            if i % 20 == 0:
                self.canvas.create_line(start_x + i, start_y, start_x + i + 10, start_y + 10, fill=color, width=self.brush_size_var.get())
            else:
                self.canvas.create_line(start_x + i, start_y + 10, start_x + i + 10, start_y, fill=color, width=self.brush_size_var.get())

    def draw_spiral(self, start_x, start_y, color):
        for i in range(100):
            angle = i * 0.1
            x = start_x + int(10 * angle * math.cos(angle))
            y = start_y + int(10 * angle * math.sin(angle))
            self.canvas.create_oval(x, y, x + self.brush_size_var.get(), y + self.brush_size_var.get(), fill=color, outline=color)

    def draw_random_shape(self, start_x, start_y, color):
        shape_type = random.choice(['oval', 'rectangle'])
        size = random.randint(20, 100)
        if shape_type == 'oval':
            self.canvas.create_oval(start_x, start_y, start_x + size, start_y + size, fill=color, outline=color)
        elif shape_type == 'rectangle':
            self.canvas.create_rectangle(start_x, start_y, start_x + size, start_y + size, fill=color, outline=color)

    def get_vibrant_color(self):

        hue = random.randint(0, 360)
        saturation = 0.9
        lightness = random.uniform(0.3, 0.7)
        r, g, b = self.hsl_to_rgb(hue, saturation, lightness)
        return f'#{r:02x}{g:02x}{b:02x}'

    def hsl_to_rgb(self, h, s, l):

        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChaosBrushApp(root)
    root.mainloop()
