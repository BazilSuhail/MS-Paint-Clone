from tkinter import *
from tkinter import colorchooser
from tkinter import Button, PhotoImage
import math
from tkinter import simpledialog
class Text_Drawing:
    def __init__(self, canvas, textValue, selected_font, text_size, brush_color, undo_stack):
        self.canvas = canvas
        self.textValue = textValue
        self.selected_font = selected_font
        self.text_size = text_size
        self.brush_color = brush_color
        self.undo_stack = undo_stack
        self.shape_id = None
    def on_text_press(self):
        self.canvas.unbind("<Button-3>")
        self.canvas.unbind("<ButtonRelease-3>")
        self.canvas.bind("<Button-3>", self.draw_text)
        self.canvas.bind("<ButtonRelease-3>", self.draw_generic_end)
    def draw_text(self, event):
        self.shape_id = self.canvas.create_text(event.x,event.y,
            text=self.textValue.get(),
            font=(self.selected_font.get(), self.text_size.get(), "bold"),
            fill=self.brush_color,
        )
        self.undo_stack.append(self.shape_id)
    def undo(self):
        if self.undo_stack:
            shape_id = self.undo_stack.pop()
            self.canvas.delete(shape_id)
    def draw_generic_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

class NoteDialog:
    def __init__(self):
        self.dialog = None
        self.dialog_width = 500
        self.dialog_height = 300
    def open_dialog(self):
        self.dialog = Toplevel()
        self.dialog.title("Enter Note")
        self.calculate_dialog_position()
        self.note_frame = Frame(self.dialog, relief=GROOVE, borderwidth=2)
        self.note_frame.pack(padx=10, pady=10)
        self.note_text = Text(self.note_frame, relief=GROOVE, font=("Gungsuh", 10, "bold"), borderwidth=2, bg="white", width=70, height=20)
        self.note_text.pack()
    def calculate_dialog_position(self):
        self.screen_width = self.dialog.winfo_screenwidth()
        self.screen_height = self.dialog.winfo_screenheight()
        x = (self.screen_width // 2) - (self.dialog_width // 2)
        y = (self.screen_height // 2) - (self.dialog_height // 2)
        self.dialog.geometry(f"{self.dialog_width}x{self.dialog_height}+{x}+{y}")
