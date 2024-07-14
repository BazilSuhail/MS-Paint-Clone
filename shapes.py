from tkinter import *
from tkinter import colorchooser
from tkinter import Button, PhotoImage
import math
class Pentagon:
    def __init__(self, canvas, color_brush, sz_outline):
        self.canvas = canvas
        self.color_brush = color_brush
        self.sz_outline = sz_outline
        self.shape_type = None
        self.prev_x = None
        self.prev_y = None
    def function_of_pentagon(self, event):  
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_x is None:
            self.prev_x, self.prev_y = event.x, event.y
            return
        len = abs(event.x - self.prev_x)
        a=36
        dis_centre = len / (2 * math.sin(math.radians(a)))
        m = -54
        angle = math.radians(m)
        num_of_points = []
        for _ in range(5):
            x = self.prev_x + dis_centre * math.cos(angle)
            y = self.prev_y - dis_centre * math.sin(angle)
            num_of_points.append((x, y))
            angle += math.radians(72)
        self.shape_type = self.canvas.create_polygon(*num_of_points, outline= self.color_brush, fill='', width=self.sz_outline.get())
    def generic_end(self, event):
        self.prev_x, self.prev_y = None, None
        self.shape_type = None
        

class _Triangle_:
    def __init__(self, canvas, color, size):
        self.canvas = canvas
        self.color = color
        self.size = size
        self.shape_number = None
        self.prev_a = None 
        self.prev_b = None
    def function_of_triangle(self, event):
        if self.shape_number is not None:
            self.canvas.delete(self.shape_number)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        len = abs(event.x - self.prev_a)
        height = abs(event.y - self.prev_b)
        self.brush_activate=True
        x1, y1 = self.prev_a, self.prev_b
        self.brush_activate=True
        x2, y2 = self.prev_a + len, self.prev_b + height
        self.brush_activate=False
        x3, y3 = self.prev_a - len, self.prev_b + height
        self.shape_number = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.color, fill='',width=self.size.get())
        
    def generic_end(self, event):
        self.prev_a, self.prev_b = None, None
        self.shape_number = None

class _Square:
    def __init__(self, canvas, color_brush, sz_outline):
        self.canvas = canvas
        self.color_brush = color_brush
        self.outline_sz = sz_outline
        self.shape_type = None
        self.prev_a = None
        self.prev_b = None
        
    def square_tool(self):
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.bind("<B1-Motion>", self.function_of_square)
            self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def function_of_square(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        v1 = 0
        side = max(abs(self.prev_a - event.x), abs(self.prev_b - event.y))
        if self.prev_a < event.x:
            #{
            if self.prev_b < event.y:
                a1, b1 = self.prev_a, self.prev_b
                for _ in range(1):
                    v1+=1
                self.brush_activate=True
                a2, b2 = self.prev_a + side, self.prev_b + side
            else:
                a1, b1 = self.prev_a, self.prev_b - side
                for _ in range(1):
                    v1+=1
                a2, b2 = self.prev_a + side, self.prev_b
            #}
        elif self.prev_b < event.y:
            a1, b1 = self.prev_a - side, self.prev_b
            a2, b2 = self.prev_a, self.prev_b + side
        else:
            a1, b1 = self.prev_a - side, self.prev_b - side
            for _ in range(1):
                v1+=1
            a2, b2 = self.prev_a, self.prev_b
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_rectangle(a1, b1, a2, b2, outline=self.color_brush, wid=self.outline_sz.get())
    def generic_end(self, event):
        self.prev_a, self.prev_b = None, None
        self.shape_type = None