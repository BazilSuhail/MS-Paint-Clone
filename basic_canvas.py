from tkinter import *
from tkinter import colorchooser
from tkinter import Button, PhotoImage
import math
from tkinter import simpledialog
from turtle import circle
from PIL import ImageGrab
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from PIL import ImageGrab
from tkinter import filedialog, messagebox
class Image_Saver_tool:
    def __init__(self, console, canvas):
        self.console = console
        self.canvas = canvas
    def save_image(self):
        try:
            file_location = filedialog.asksaveasfilename(defaultextension="png")
            x = self.console.winfo_x() + 33
            y = self.console.winfo_y() + 180
            can_wid = self.canvas.winfo_width() + 346
            can_heg = self.canvas.winfo_height() + 155
            img = ImageGrab.grab(bbox=(x, y, x + can_wid, y + can_heg))
            img.save(file_location)
            if messagebox.askyesno("Paint App", "Would you like to preview the image?"):
                img.show()
        except Exception as e:
            messagebox.showinfo("Paint App", f"An error occurred while saving the image: {str(e)}")

class ImageLoader:
    def __init__(self, canvas):
        self.canvas = canvas
        self.background_image = None

    def open_press(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            image = Image.open(file_path)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image = image.resize((canvas_width, canvas_height), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
            

# zoom tool
class ZoomTool:
    def __init__(self, canvas, wid, heg):
        self.factor = 1.0
        self.canvas = canvas
        self.screen_wid = wid
        self.screen_heg = heg
    def zoom_in_tool(self):
        a = 0.1
        self.factor += a
        self.apply_zoom()
    def zoom_out_tool(self):
        b = 0.1
        if self.factor > b:
            self.factor -= b
            self.apply_zoom()
    def apply_zoom(self):
        wid_scale = int(self.screen_wid * self.factor)
        heg_scale = int(self.screen_heg * self.factor)
        offset_x = (self.screen_wid - wid_scale) // 2
        offset_y = (self.screen_heg - heg_scale) // 2
        self.canvas.config(width = wid_scale, height = heg_scale)
        self.canvas.scale("all", 0, 0, self.factor, self.factor)
        self.canvas.move("all", offset_x, offset_y)

class Selection_Tool:
    
    def __init__(self,canvas,console):
        self.canvas=canvas
        self.shape_type = None
        self.selected_objects = []
        self.prev_x ,self.prev_y , self.sel_x , self.sel_y = None ,None ,None ,None
        self.image_stored = None
        self.console = console
        self.is_selection_active = False
        
        # Bind the drag and release events
        self.console.bind("<B1-Motion>", self.dragging_func)
        self.console.bind("<ButtonRelease-1>", self.releasing_point)
        self.console.bind("<Button-1>", self.clicking_point)
        
    
    def on_selection_press(self):
        self.is_selection_active = not self.is_selection_active

        if self.is_selection_active:
            self.canvas.bind("<B1-Motion>", self.selection_drawing)
            self.canvas.bind("<ButtonRelease-1>", self.area_selection)
            #self.selection_button.config(bg="LightBlue")
        else:
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.shape_type=None
            self.selected_objects = []
            self.prev_x ,self.prev_y , self.sel_x , self.sel_y = None ,None ,None ,None
            self.sel = True
            self.image_stored = None
            #self.selection_button.config(bg="white")
    
    # def on_selection_press(self):
    #     self.canvas.unbind("<B1-Motion>")
    #     self.canvas.unbind("<ButtonRelease-1>")
    #     self.canvas.bind("<B1-Motion>", self.selection_drawing)
    #     self.canvas.bind("<ButtonRelease-1>", self.area_selection)

    def selection_drawing(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        n1, n2 = None, None
        if self.prev_x is None:
            self.prev_x, self.prev_y = event.x, event.y
            return
        x1, y1 = self.prev_x, self.prev_y
        self.sel = True
        x2, y2 = event.x, event.y
        self.shape_type = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", wid=3)

    def area_selection(self, event):
        if self.prev_x is None or self.prev_y is None:
            return
        sel_items = []
        objects = self.canvas.find_all()
        min1, max1 = min(self.prev_x, event.x), max(self.prev_x, event.x)
        #max1 = max(self.prev_x, event.x)
        self.sel = True
        min2, max2 = min(self.prev_y, event.y), max(self.prev_y, event.y)
        for obj_id in objects:
            bbox = self.canvas.bbox(obj_id)
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                if min1 <= x1 <= max1 and min2 <= y1 <= max2 and min1 <= x2 <= max1 and min2 <= y2 <= max2:
                    sel_items.append(obj_id)
        self.selected_objects = sel_items
        self.sel_x = min1
        self.sel_y = min2
        self.image_store_and_placing(max1, max2)

    def image_store_and_placing(self, x, y):
        if self.sel_x is not None and self.sel_y is not None:
            x1, y1 = self.sel_x, self.sel_y
            x2, y2 = x, y
            n1 = None
            captured_image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            self.captured_image = captured_image# Store the captured img for later use
            screen_shot2 = None
            self.canvas.create_rectangle(x1 - 1, y1 - 1, x2 + 1, y2 + 1, fill="white", outline="white")#white back

    def dragging_func(self, event):
        if self.selected_objects:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            for obj_id in self.selected_objects:
                self.canvas.move(obj_id, dx, dy)
            self.img=None
            self.prev_x ,self.prev_y = event.x ,event.y
            self.draw_selected_area()  # Draw the selection rectangle


    def releasing_point(self, event):
        pass

    def clicking_point(self, event):
        if self.selected_objects:
            if self.prev_x is not None and self.prev_y is not None and self.sel_x is not None and self.sel_y is not None:
                dx , dy = event.x - self.sel_x , event.y - self.sel_y
                for obj_id in self.selected_objects:
                    self.canvas.move(obj_id, dx, dy)
            self.selected_objects = []
            stored_img=None
            w1,w2=None,None
            self.prev_x , self.prev_y , self.sel_x , self.sel_y = None ,None ,None ,None
            self.canvas.delete("selected_area")

    def draw_selected_area(self):
        if self.prev_x is not None and self.prev_y is not None:
            self.canvas.delete("selected_area")
            self.canvas.create_rectangle(self.prev_x, self.prev_y, self.prev_x + 1, self.prev_y + 1, tags="selected_area", outline="red", wid=2)

