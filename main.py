from tkinter import *
from tkinter import colorchooser
from tkinter import Button, PhotoImage
import math
from tkinter import simpledialog
from turtle import circle
from PIL import ImageGrab
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk,ImageDraw
from tkinter.colorchooser import askcolor

from basic_canvas import ImageLoader,ZoomTool,Selection_Tool,Image_Saver_tool
from shapes import Pentagon,_Triangle_,_Square
from toolbar import NoteDialog,Text_Drawing

class My_Paint:
    def __init__(self,width,height,title):
        self.console = Tk()
        self.console.title(title)
        self.console.geometry(f'{str(width)}x{str(height)}')
        #===========================================
        # canvas
        #===========================================
        
        #   area for buttons
        self.Area_for_buttons = Frame(self.console,width = width,height = 110,relief=SUNKEN,bg = "grey86")
        self.Area_for_buttons.pack()
        self.canvas = Canvas(self.console, width=width, height=height, bg="white")
        self.canvas.pack()
        #   bind
        self.canvas.bind("<B1-Motion>",self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>",self.brush_draw_ending)
        #   toogle magnify 
        self.console.bind("<Button-2>", self.magnify_tool)
        
        #===========================================
        # Default Attributes
        #===========================================
        
        # default attributes
        self.color_brush = 'black'
        self.color_eraser = 'white'
        self.shape_type = None
        self.prev_a,self.prev_b = None,None
        self.outline_sz = IntVar()
        self.default_num_points=7
        self.outline_sz.set(2)
        self.brush_activate = False
        # toogle magnify 
        self.win_mag = None #window magnify
        self.mag_label = None
        self.is_mag_active = False
        
        #==========================================
        self.pen = Pentagon(self.canvas, self.color_brush, self.outline_sz)
        self.tri = _Triangle_(self.canvas, self.color_brush, self.outline_sz)
        self.sq = _Square(self.canvas, self.color_brush, self.outline_sz)
        
        #undo buttons 
        self.undo_stack = []  # Stack to store actions for undo
        self.redo_stack = []  # Stack to store actions for redo
        self.selected_objects1 = []
        
        #===========================================
        # Selection tool attributes
        #self.console.bind("<B1-Motion>", self.on_canvas_drag)
        #self.console.bind("<ButtonRelease-1>", self.on_canvas_release)
        #self.console.bind("<Button-1>", self.on_canvas_click)
        
        # Initialize selected objects and last position variables
        self.selected_objects = []
        self.prev_a = None
        self.prev_b = None
        self.selected_area_start_x = None
        self.selected_area_start_y = None
        self.stored_image_id = None
        
        # pictures
        self.image_open = PhotoImage(file="pics/open.png")
        self.image_save = PhotoImage(file="pics/save.png")
        self.image_B = PhotoImage(file="pics/brush.png")
        self.image_home = PhotoImage(file="pics/home.png")
        self.image_eraser = PhotoImage(file="pics/eraser.png")
        self.image_picker = PhotoImage(file="pics/color_picker.png")
        self.image_polygon = PhotoImage(file="pics/polygon_n.png")
        self.image_octagon = PhotoImage(file="pics/octagon.png")
        self.image_P = PhotoImage(file="pics/pentagon.png")
        self.image_C = PhotoImage(file="pics/circle.png")
        self.image_mag = PhotoImage(file="pics/selection.png")
        self.image_bucket = PhotoImage(file="pics/bucket.png")
        self.image_D = PhotoImage(file="pics/diamond.png")
        self.image_arrow = PhotoImage(file="pics/arrow.png")
        self.image_o = PhotoImage(file="pics/oval.png")
        self.image_t = PhotoImage(file="pics/triangle.png")
        self.image_h = PhotoImage(file="pics/hexagon.png")
        self.image_S = PhotoImage(file="pics/star.png")
        self.image_s = PhotoImage(file="pics/square.png")
        self.image_R = PhotoImage(file="pics/rectangle.png")
        self.image_rightTriangle = PhotoImage(file="pics/rightTriangle.png")
        self.image_txt = PhotoImage(file="pics/txt.png")
        self.note_img = PhotoImage(file="pics/note.png")
        self.zoom_in11 = PhotoImage(file="pics/zoom_in.png")
        self.zoom_out22 = PhotoImage(file="pics/zoom_out.png")
        self.image_undo = PhotoImage(file="pics/undo.png")
        self.image_redo = PhotoImage(file="pics/redo.png")
        
        #===========================================
        # Home
        #===========================================
        
        #   clear button
        self.new_button = Button(self.Area_for_buttons,text = "CLear",bg='Lightgrey' , width=5,command=self.clear_canvas)
        self.new_button.place(x=3,y=60)
        #   open button
        self.loader = ImageLoader(self.canvas)
        self.open_button = Button(self.Area_for_buttons,image = self.image_open,bg='Lightgrey' , width=38,command=self.loader.open_press)
        self.open_button.configure(bg="grey84")
        self.open_button.place(x=3,y=2)
        
        #   save button
        save_tool = Image_Saver_tool(self.console, self.canvas)
        self.save_button = Button(self.Area_for_buttons,image = self.image_save,bg='Lightgrey', width=38,command=save_tool.save_image)
        self.save_button.place(x=60,y=2)
        
        #   help button
        self.help_button = Button(self.Area_for_buttons,text = "Help",bg='Lightgrey', width=5,command=self.help)
        self.help_button.place(x=60,y=60)
        #   toogle
        self.home_button = Label(self.Area_for_buttons,image=self.image_home,bg="grey86",relief=FLAT)
        self.home_button.place(x=0,y=90)
        
        #===========================================
        # Tools
        #===========================================
        
        # brush 
        self.brush_button = Button(self.Area_for_buttons,image=self.image_B,borderwidth=2,relief=GROOVE,command=self.brush_tool)
        self.brush_button.place(x=188,y=2)
        # eraser button
        self.eraser_button = Button(self.Area_for_buttons,image=self.image_eraser,borderwidth=2,relief=GROOVE,command=self.eraser_tool)
        self.eraser_button.place(x=188,y=46)
        # color picker
        self.picker_button = Button(self.Area_for_buttons, image=self.image_picker, borderwidth=2, relief=GROOVE, command=self.pixel_color_picker)
        self.picker_button.place(x=230, y=46)
        self.bool_picker = False
        # bucket button
        self.bool_fill=False
        self.bucket_button = Button(self.Area_for_buttons,image=self.image_bucket,borderwidth=2,relief=GROOVE,command=self.fill_bucket_tool)
        self.bucket_button.place(x=230,y=2)
        # Selection button
        selection_man = Selection_Tool(self.canvas,self.console)
        self.selection_button = Button(self.Area_for_buttons,image=self.image_mag,borderwidth=2,relief=GROOVE,command=selection_man.on_selection_press)
        self.selection_button.place(x=130,y=2)
        #   font size
        self.sizeLabel = Label(self.Area_for_buttons , text="Brush Size",height=2, width=9,font=("Times New Roman",10,"bold"),bg="grey79")
        self.sizeLabel.place(x=278,y=5)
        self.options = [1,2,3,4,5,10,30,40,50,100,200]
        self.sizeList = OptionMenu(self.Area_for_buttons , self.outline_sz , *self.options)
        self.sizeList.place(x=288,y=50)
        
        #===========================================
        # Shapes
        #===========================================
        
        #   circle button
        b_circle = Button(self.Area_for_buttons,image=self.image_C,borderwidth=1,relief=SUNKEN,command=self.circle_tool)
        b_circle.place(x=420,y=30)
        #   diamond button
        b_diamond = Button(self.Area_for_buttons,image=self.image_D,borderwidth=1,relief=SUNKEN,command=self.diamond_tool)
        b_diamond.place(x=385,y=30)
        #   arrow button
        b_arrow = Button(self.Area_for_buttons,image=self.image_arrow,borderwidth=1,relief=SUNKEN ,command=self.arrow_tool)
        b_arrow.place(x=385,y=1)
        #   oval button
        b_oval = Button(self.Area_for_buttons,image=self.image_o, borderwidth=1,relief=SUNKEN,command=self.oval_tool)
        b_oval.place(x=420,y=2)
        #   triangle button
        b_triangle = Button(self.Area_for_buttons,image=self.image_t,borderwidth=1,relief=SUNKEN,command=self.triangle_tool)
        b_triangle.place(x=385,y=60)
        #   hexagon button
        b_hexagon = Button(self.Area_for_buttons,image=self.image_h,borderwidth=1,relief=SUNKEN,command=self.hexagon_tool)
        b_hexagon.place(x=420,y=60)
        #   star button 
        b_star = Button(self.Area_for_buttons,image=self.image_S,borderwidth=1,relief=SUNKEN,command=self.star_tool)
        b_star.place(x=455,y=2)
        #   square button
        b_Square = Button(self.Area_for_buttons,image=self.image_s,borderwidth=1,relief=SUNKEN,command=self.sq.square_tool)
        b_Square.place(x=455,y=30)
        #   rectangle button
        b_Rectangle = Button(self.Area_for_buttons,image=self.image_R,borderwidth=1,relief=SUNKEN,command=self.rectangle_tool)
        b_Rectangle.place(x=455,y=60)
        #   pentagon button
        b_pentagon = Button(self.Area_for_buttons,image=self.image_P,borderwidth=1,relief=SUNKEN,command=self.pentagon_tool)
        b_pentagon.place(x=490,y=60)
        #   rightTriangle button
        b_rightTriangle = Button(self.Area_for_buttons,image=self.image_rightTriangle,borderwidth=1,relief=SUNKEN,command=self.Right_tool)
        b_rightTriangle.place(x=490,y=30)
        #   octagon button
        b_octagon = Button(self.Area_for_buttons,image=self.image_octagon,borderwidth=1,relief=SUNKEN,command=self.octagon_tool)
        b_octagon.place(x=490,y=2)
        #   polygon button
        b_polygon = Button(self.Area_for_buttons,image=self.image_polygon,borderwidth=1 ,command=self.N_polygon_tool)
        b_polygon.place(x=530,y=2)
        #                                       ===========================================
        #                                               Bonus :    label of polygon
        #                                       ===========================================
        self.polygon_num = Label(self.Area_for_buttons,text="Enter Points",height=1 ,width=9 , bg="Lightgrey")
        self.polygon_num.place(x=532, y=34)
        self.entry_polygon = Entry(self.Area_for_buttons,relief=SUNKEN, bg="white" , width=11 )
        self.entry_polygon.place(x=532,y=64)
        self.entry_polygon.bind("<KeyRelease>", self.update_default_num_points)
        
        #===========================================
        # Text
        #===========================================
        
        self.text_size = IntVar()
        self.textValue = StringVar()
        self.text_size.set(20)
        self.text_font=[10,20,50,72,100]
        self.available_fonts = ["Arial", "Times New Roman", "Courier New", "Verdana"]
        
        self.entryButton = Entry(self.Area_for_buttons, textvariable=self.textValue,relief=SUNKEN, bg="white" , width=14 )
        self.entryButton.place(x=630,y=34)
        # note frame
        self.note_dialog = NoteDialog()
        dialog_button = Button(self.Area_for_buttons, image=self.note_img, command=self.note_dialog.open_dialog)
        dialog_button.place(x=726, y=64)

        #text size
        self.txtLabel = Label(self.Area_for_buttons , text="Size :",bg="grey86", width=4,font=("Times New Roman",10,"bold"))
        self.txtLabel.place(x=628,y=64)
        self.txtList = OptionMenu(self.Area_for_buttons , self.text_size , *self.text_font)
        self.txtList.configure(width=1, height=1)
        self.txtList.place(x=668,y=60)
        
        # Create a StringVar variable to store the selected font
        self.selected_font = StringVar()
        self.selected_font.set(self.available_fonts[1])  # Set the first font as the default
        self.txt_fnt = Label(self.Area_for_buttons , text="Text Font",bg="grey86", width=19,relief=GROOVE,font=("Times New Roman",10,"bold"))
        self.txt_fnt.place(x=725,y=5)
        # Create the OptionMenu widget
        self.font_menu = OptionMenu(self.Area_for_buttons, self.selected_font, *self.available_fonts)
        self.font_menu.configure(height=1,width=16)
        self.font_menu.configure(bg="grey83")
        self.font_menu.place(x=725,y=30)
        
        text_tool = Text_Drawing(self.canvas, self.textValue, self.selected_font, self.text_size, self.color_brush, self.undo_stack)
        # text button
        
        self.textTitle_Button = Button(self.Area_for_buttons ,image=self.image_txt,borderwidth=1,command=self.text_tool )
        self.textTitle_Button.place(x=628,y=5)
        
        #===========================================
        # color buttons all or color pallete
        #===========================================
        
        # color 1
        self.label_back = Button(self.Area_for_buttons,text="Color 1",width=5,relief=FLAT, bg="LightGrey",command=self.select_color)
        self.label_back.place(x=949, y=65)
        self.color_label = Label(self.Area_for_buttons,height=3, width=6,relief=SUNKEN, bg=self.color_brush)
        self.color_label.place(x=949, y=10)
        # color 2
        self.label_back1 = Button(self.Area_for_buttons,text="Color 2",width=5,relief=FLAT, bg="LightGrey",command=self.eraser_brush_color)
        self.label_back1.place(x=899, y=65)
        self.color_label1 = Label(self.Area_for_buttons,height=3, width=6,relief=SUNKEN, bg=self.color_eraser)
        self.color_label1.place(x=899, y=10)
        #1
        redButton = Button(self.Area_for_buttons, bg="red", width=2, command=lambda: (setattr(self, 'color_brush', 'red'), self.update_color_label()))
        redButton.place(x=1016, y=1)
        tomatoButton = Button(self.Area_for_buttons, text="", bg="red3", width=2, command=lambda: (setattr(self, 'color_brush', 'red3'), self.update_color_label()))
        tomatoButton.place(x=1016, y=30)
        tomato4Button = Button(self.Area_for_buttons, text="", bg="red4", width=2, command=lambda: (setattr(self, 'color_brush', 'red4'), self.update_color_label()))
        tomato4Button.place(x=1016, y=60)
        #2
        RosyBrown3Button = Button(self.Area_for_buttons, text="", bg="RosyBrown3", width=2, command=lambda: (setattr(self, 'color_brush', 'RosyBrown3'), self.update_color_label()))
        RosyBrown3Button.place(x=1043, y=30)
        coralButton = Button(self.Area_for_buttons, text="", bg="coral", width=2, command=lambda: (setattr(self, 'color_brush', 'coral'), self.update_color_label()))
        coralButton.place(x=1043, y=60)
        yellowButton = Button(self.Area_for_buttons, text="", bg="yellow", width=2, command=lambda: (setattr(self, 'color_brush', 'yellow'), self.update_color_label()))
        yellowButton.place(x=1043, y=1)
        #3
        orangeButton = Button(self.Area_for_buttons, text="", bg="orange", width=2, command=lambda: (setattr(self, 'color_brush', 'orange'), self.update_color_label()))
        orangeButton.place(x=1070, y=1)
        orangeredButton = Button(self.Area_for_buttons, text="", bg="orange red", width=2, command=lambda: (setattr(self, 'color_brush', 'orange red'), self.update_color_label()))
        orangeredButton.place(x=1070, y=30)
        orange3Button = Button(self.Area_for_buttons, text="", bg="orange3", width=2, command=lambda: (setattr(self, 'color_brush', 'orange3'), self.update_color_label()))
        orange3Button.place(x=1070, y=60)
        #4
        greenyellowButton = Button(self.Area_for_buttons, text="", bg="green yellow", width=2, command=lambda: (setattr(self, 'color_brush', 'green yellow'), self.update_color_label()))
        greenyellowButton.place(x=1097, y=1)
        greenButton = Button(self.Area_for_buttons, text="", bg="green", width=2, command=lambda: (setattr(self, 'color_brush', 'green'), self.update_color_label()))
        greenButton.place(x=1097, y=30)
        LightGreenButton = Button(self.Area_for_buttons, text="", bg="LightGreen", width=2, command=lambda: (setattr(self, 'color_brush', 'LightGreen'), self.update_color_label()))
        LightGreenButton.place(x=1097, y=60)
        #5
        blue1Button = Button(self.Area_for_buttons, text="", bg="blue1", width=2, command=lambda: (setattr(self, 'color_brush', 'blue1'), self.update_color_label()))
        blue1Button.place(x=1124, y=1)
        blue3Button = Button(self.Area_for_buttons, text="", bg="blue3", width=2, command=lambda: (setattr(self, 'color_brush', 'blue3'), self.update_color_label()))
        blue3Button.place(x=1124, y=30)
        BlueVioletButton = Button(self.Area_for_buttons, text="", bg="BlueViolet", width=2, command=lambda: (setattr(self, 'color_brush', 'BlueViolet'), self.update_color_label()))
        BlueVioletButton.place(x=1124, y=60)
        #6
        pink1Button = Button(self.Area_for_buttons, text="", bg="pink", width=2, command=lambda: (setattr(self, 'color_brush', 'pink'), self.update_color_label()))
        pink1Button.place(x=1151, y=1)
        pink4Button = Button(self.Area_for_buttons, text="", bg="pink4", width=2, command=lambda: (setattr(self, 'color_brush', 'pink4'), self.update_color_label()))
        pink4Button.place(x=1151, y=30)
        plum2Button = Button(self.Area_for_buttons, text="", bg="plum2", width=2, command=lambda: (setattr(self, 'color_brush', 'plum2'), self.update_color_label()))
        plum2Button.place(x=1151, y=60)
        #7
        darksalmonButton = Button(self.Area_for_buttons, text="", bg="black", width=2, command=lambda: (setattr(self, 'color_brush', 'black'), self.update_color_label()))
        darksalmonButton.place(x=1178, y=1)
        gray31Button = Button(self.Area_for_buttons, text="", bg="gray31", width=2, command=lambda: (setattr(self, 'color_brush', 'gray31'), self.update_color_label()))
        gray31Button.place(x=1178, y=30)
        gray12Button = Button(self.Area_for_buttons, text="", bg="gray", width=2, command=lambda: (setattr(self, 'color_brush', 'gray'), self.update_color_label()))
        gray12Button.place(x=1178, y=60)
        
        #===========================================
        # Select Color button
        #===========================================       
        self.color_pallete=PhotoImage(file="pics/color.png")
        self.select_color_button = Button(self.Area_for_buttons,image=self.color_pallete,borderwidth=1,relief=RAISED,command=self.select_color)
        self.select_color_button.place(x=1208,y=2)
        
        #===========================================
        # magnify
        #===========================================  
        
        # zoom in
        zoom_tool = ZoomTool(self.canvas, width, height)
        self.mag_button1 = Button(self.Area_for_buttons,image=self.zoom_in11,borderwidth=2,command=zoom_tool.zoom_in_tool)
        self.mag_button1.place(x=1310,y=47)
        # zoom out
        self.mag_button2 = Button(self.Area_for_buttons,image=self.zoom_out22,borderwidth=2,command=zoom_tool.zoom_out_tool)
        self.mag_button2.place(x=1360,y=47)
        
        #===========================================
        # undo and redo
        #=========================================== 
        
        self.button_undo = Button(self.Area_for_buttons,image=self.image_undo,borderwidth=2,command=self.on_undo)
        self.button_undo.place(x=1310,y=2)
        self.button_redo = Button(self.Area_for_buttons,image=self.image_redo,borderwidth=2,command=self.on_redo)
        self.button_redo.place(x=1360,y=2)
        
    #===========================================
    # Home tools
    #=========================================== 
    
    #canvas clear function
    def clear_canvas(self):
        if messagebox.askokcancel("Paint app" , "Do you want to clear everything ...... !!\nContent's won't be saved Please save if haven't !!"):
            self.canvas.delete('all')
    #help function
    def help(self):
        self.helpText = "1. Draw by holding Left button of mouse.\n2.Click scroll well to pick color on canvas.\n3. Click on Select Color Option select specific color\n4. Click on Clear to clear entire Canvas\n5.Use RIght Click to put Text on Screen"
        messagebox.showinfo("Help" , self.helpText)
    
    #===========================================
    # brush and eraser
    #=========================================== 

    def brush_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ReleaseButton-1>")
        self.canvas.bind("<B1-Motion>",self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>",self.brush_draw_ending)
        
    def brush_draw(self,event):
        if self.prev_a is None:
            self.prev_a,self.prev_b = event.x,event.y
            return
        line_id = self.canvas.create_line(self.prev_a,self.prev_b,event.x,event.y,width = self.outline_sz.get(),capstyle = ROUND,fill= self.color_brush)
        self.undo_stack.append(line_id)
        brush_activate = True
        self.prev_a , self.prev_b = event.x,event.y
        self.canvas["cursor"] = 'tcross'
        
    def brush_draw_ending(self, event):
        self.prev_a, self.prev_b = None, None
        self.undo_stack.append(list(self.selected_objects))
        self.selected_objects = []

    #                                                 eraser function code
    def eraser_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ReleaseButton-1>")

        self.canvas.bind("<B1-Motion>",self.eraser_draw)
        self.canvas.bind("<ButtonRelease-1>",self.eraser_draw_ending)
    def eraser_draw(self,event):
        if self.prev_a is None:
            self.prev_a,self.prev_b = event.x,event.y
            return
        self.canvas.create_line(self.prev_a,self.prev_b,event.x,event.y,width = self.outline_sz.get(), capstyle = ROUND,fill= self.color_eraser)
        self.prev_a , self.prev_b = event.x,event.y
        brush_activate = False
        self.canvas["cursor"] = "dot"#DOTBOX
    def eraser_draw_ending(self,event):
        self.prev_a , self.prev_b = None,None
    
    
    #==========================================
    #color updation (labels)
    
    def update_color_label(self):
            self.color_label.config(bg=self.color_brush)
    def update_color_eraser_label(self):
            self.color_label1.config(bg=self.color_eraser)
    
    #==========================================
    
    # color selection
    def select_color(self):
        selected_color = colorchooser.askcolor()
        self.color_brush = selected_color[1]
        self.update_color_label()
    # eraser color selection 
    def eraser_brush_color(self):
        color_eraser = colorchooser.askcolor()
        self.color_eraser = color_eraser[1]
        self.update_color_eraser_label()
    
    #===========================================
    # color picker
    #===========================================
    def pixel_color_picker(self):
        self.bool_picker = not self.bool_picker  # Toggle the state

        if self.bool_picker:
            self.canvas.bind("<Button-1>", self.pick_color)
            self.picker_button.config(bg="LightBlue")
        else:
            self.canvas.unbind("<Button-1>")
            self.picker_button.config(bg="white")

    def pick_color(self, event):
        if self.bool_picker:
            item_id = self.canvas.find_closest(event.x, event.y)[0]
            color = self.canvas.itemcget(item_id, "fill")
            self.color_brush = color
            self.update_color_label()

    #===========================================
    # bucket tool
    #===========================================
    def fill_bucket_tool(self):
        self.bool_fill = not self.bool_fill  # Toggle the state
        if self.bool_fill:
            self.canvas.bind("<Button-1>", self.on_screen_click)
            self.brush_activate=True
            self.bucket_button.config(bg="LightBlue")
        else:
            self.canvas.unbind("<Button-1>")
            self.bucket_button.config(bg="white")

    def on_screen_click(self, event):
        x , y = event.x ,event.y
        brush_activate = False
        filling_clr = self.color_brush
        self.bucket_tool(x, y, filling_clr)

    def bucket_tool(self, x, y, filling_clr):
        target = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")
        if target == filling_clr:
            return
        self.brush_activate=True
        self.bounded_fill(x, y, target, filling_clr,1)

    def bounded_fill(self, x, y, target_color, filling_clr,boundary):
        current_color = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")
        if current_color != target_color:
            return
        self.canvas.itemconfig(self.canvas.find_closest(x, y), fill=filling_clr)
        self.bounded_fill(x + 1, y, target_color, filling_clr,3)
        fill_region = self.color_brush
        self.bounded_fill(x - 1, y, target_color, filling_clr,3)
        self.bounded_fill(x, y + 1, target_color, filling_clr,3)
        self.brush_activate=True
        self.bounded_fill(x, y - 1, target_color, filling_clr,3)
    
    #===========================================
    # shapes
    #=========================================== 
    
    def circle_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ReleaseButton-1>")
        self.canvas.bind("<B1-Motion>",self.function_of_circle)
        self.canvas.bind("<ButtonRelease-1>",self.generic_end)
    def diamond_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_diamond)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def arrow_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ReleaseButton-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_arrow)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def triangle_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ReleaseButton-1>")
        self.canvas.bind("<B1-Motion>", self.tri.function_of_triangle)
        self.canvas.bind("<ButtonRelease-1>",self.tri.generic_end)
    def oval_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_oval)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def hexagon_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_hexagon)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def star_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_star)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def rectangle_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def pentagon_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.pen.function_of_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.pen.generic_end)
    def Right_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_Right)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)  
    def octagon_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_octagon)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def N_polygon_tool(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.function_of_N_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.generic_end)
    def text_tool(self):
        self.canvas.unbind("<Button-3>")
        self.canvas.unbind("<ButtonRelease-3>")
        self.canvas.bind("<Button-3>", self.write_text)
        self.canvas.bind("<ButtonRelease-3>", self.generic_end)
    #   circle code

    def function_of_circle(self,event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a,self.prev_b = event.x,event.y
            return
        dis_centre = abs(self.prev_a - event.x) + abs(self.prev_b - event.y)
        a1,b1 = (self.prev_a - dis_centre),(self.prev_b - dis_centre)
        prev_m = 1
        last_cord = 2
        a2,b2 = (self.prev_a + dis_centre),(self.prev_b + dis_centre)
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_oval(a1,b1,a2,b2,outline = self.color_brush,width = self.outline_sz.get())  
        self.undo_stack.append(self.shape_type)
    
    #  diamond button 
    def function_of_diamond(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        wid = abs(event.x - self.prev_a)
        heg = abs(event.y - self.prev_b)
        a1, b1 = (self.prev_a - wid), self.prev_b
        p,q,r=10,11,22
        a2, b2 = self.prev_a, (self.prev_b - heg)
        brush_activate = False
        a3, b3 = (self.prev_a + wid), self.prev_b
        w,x,z=4,5,6
        a4, b4 = self.prev_a, (self.prev_b + heg)
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_polygon(a1, b1, a2, b2, a3, b3, a4, b4, outline=self.color_brush, fill='', wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
    
    # arrow press code
    def function_of_arrow(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        a1, b1 ,a2, b2 ,= self.prev_a, self.prev_b, event.x, event.y
        #a2, b2 = event.x, event.y
        n1, n2 = a2 - a1, b2 - b1
        st , a =  0.5 , 2
        length = (n1 ** a + n2 ** a) ** st
        if length == 0:
            return
        arrow_sz = 10
        centre_angle = 0.4
        len_arrow = arrow_sz * centre_angle
        if n1 == 0:
            if n2 > 0:
                centre_angle = -centre_angle
            a3, b3 = a2 - arrow_sz / 2, b2 - n2 / length * arrow_sz
            self.brush_activate=True
            a4, b4 = a2 + arrow_sz / 2, b2 - n2 / length * arrow_sz
            x5, y5 = a2, b2 - n2 / length * len_arrow
        else:
            angle = math.atan(n2 / n1)
            if n1 < 0:
                angle += math.pi
            a3, b3 = a2 - n1 / length * arrow_sz * math.cos(angle - centre_angle), b2 - n2 / length * arrow_sz * math.sin(angle - centre_angle)
            a4, b4 = a2 - n1 / length * arrow_sz * math.cos(angle + centre_angle), b2 - n2 / length * arrow_sz * math.sin(angle + centre_angle)
            x5, y5 = a2 - n1 / length * len_arrow * math.cos(angle), b2 - n2 / length * len_arrow * math.sin(angle)
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_line(a1, b1, a2, b2, arrowshape=(arrow_sz, arrow_sz, len_arrow), fill=self.color_brush, wid=self.outline_sz.get()) 
        self.undo_stack.append(self.shape_type)

    # oval code
    def function_of_oval(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            self.brush_activate=True
            return
        a1, b1 = self.prev_a, self.prev_b
        brush_activate = False
        a2, b2 = event.x, event.y
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_oval(a1, b1, a2, b2, outline=self.color_brush, wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
    
    #  Hexagon code
    def function_of_hexagon(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        brush_activate = False
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            self.brush_activate=True
            return
        side = abs(event.x - self.prev_a)
        sum=  2
        store = 3
        heg = int(side * math.sqrt(store) / sum)
        n , num = 2 , 10 
        a1, b1 = self.prev_a + side, self.prev_b
        a2, b2 = self.prev_a + side // n, self.prev_b + heg
        self.brush_activate=True
        a3, b3 = self.prev_a - side // n, self.prev_b + heg
        var, var2 = 0.5, 0.5
        a4, b4 = self.prev_a - side, self.prev_b
        a5, b5 ,a6 , b6 = self.prev_a - side // n , self.prev_b - heg ,self.prev_a + side // n, self.prev_b - heg
        #a6, b6 = self.prev_a + side // n, self.prev_b - heg
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_polygon(a1, b1, a2, b2, a3, b3, a4, b4, a5, b5, a6, b6, outline=self.color_brush, fill='', width =self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
    
    #===========================================
    # Text Tool
    #=========================================== 
    
    def write_text(self, event):
        self.shape_id=self.canvas.create_text(event.x , event.y , text=self.textValue.get(),font=(self.selected_font.get(), self.text_size.get(), "bold"), fill=self.color_brush)
        self.undo_stack.append(self.shape_id)
    
    # Star code
    def function_of_star(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        num = 2
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            self.brush_activate=True
            return
        p = 0.5
        dis_centre = ((self.prev_a - event.x) ** num + (self.prev_b - event.y) ** num) ** p
        a1, b1 = self.prev_a, self.prev_b
        self.brush_activate = False
        st = 5
        a2, b2 = event.x, event.y
        angle = 2 * math.pi / st
        points = []
        for i in range(5):
            x = (dis_centre / num) * math.cos(i * angle + math.pi / num) + (a1 + a2) / num
            y = (dis_centre / num) * math.sin(i * angle + math.pi / num) + (b1 + b2) / num
            self.brush_activate=True
            var, var2 = 0.5, 0.5
            points.extend((x, y))
            x = (dis_centre / 4) * math.cos(i * angle + math.pi / num + angle / num) + (a1 + a2) / num
            y = (dis_centre / 4) * math.sin(i * angle + math.pi / num + angle / num) + (b1 + b2) / num
            self.brush_activate=True
            points.extend((x, y))
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_polygon(points, outline=self.color_brush, fill='', wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)

    #  rectangle code
    def function_of_rectangle(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        a1, b1 = self.prev_a, self.prev_b
        num12 = 5
        a2, b2 = event.x, event.y
        self.brush_activate=True
        for _ in range(1):
                    pass
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_rectangle(a1, b1, a2, b2, outline=self.color_brush, wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
    
    # right triangle
    def function_of_Right(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        a1, b1 = self.prev_a, self.prev_b
        num = 10
        a,b,c = None,2,22
        a2, b2 = event.x, self.prev_b
        a3, b3 = self.prev_a, event.y
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_polygon(a1, b1, a2, b2, a3, b3, outline=self.color_brush, fill='', wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
        
    # octagon code
    def function_of_octagon(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        angle_ = 360
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        center_x, center_y = self.prev_a, self.prev_b
        side = abs(event.x - self.prev_a)
        dis_centre = side / (2 * math.sin(math.radians(angle_ / 8))) 
        angle = math.radians(-90)
        points = []
        for _ in range(8):
            x = center_x + dis_centre * math.cos(angle)
            y = center_y + dis_centre * math.sin(angle)
            points.append((x, y))
            angle += math.radians(angle_ / 8)
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_polygon(*points, outline=self.color_brush, fill='', wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
    
    #  n polygon
    def function_of_N_polygon(self, event):
        if self.shape_type is not None:
            self.canvas.delete(self.shape_type)
        side1 = 2
        if self.prev_a is None:
            self.prev_a, self.prev_b = event.x, event.y
            return
        center_x, center_y = self.prev_a, self.prev_b
        side_length = abs(event.x - self.prev_a)
        rot_angle = -90
        dis_centre = side_length / (side1 * math.sin(math.radians(360 / self.default_num_points)))
        rotation_angle = math.radians(rot_angle)
        n_points = []
        total_angle = 360
        for _ in range(self.default_num_points):
            x,y = center_x + dis_centre * math.cos(rotation_angle) ,center_y + dis_centre * math.sin(rotation_angle)
            n_points.append((x, y))
            rotation_angle += math.radians(total_angle / self.default_num_points)
        self.canvas["cursor"] = 'fleur'
        self.shape_type = self.canvas.create_polygon(*n_points, outline=self.color_brush, fill='', wid=self.outline_sz.get())
        self.undo_stack.append(self.shape_type)
    def update_default_num_points(self, event):
        try:
            self.default_num_points = int(self.entry_polygon.get())
        except ValueError:
            self.default_num_points = 7

    #===========================================
    # toogle magnify 
    #=========================================== 
    def magnify_tool(self, event):
        self.is_mag_active = not self.is_mag_active
        if self.is_mag_active:
            self.canvas.bind("<Motion>", self.mouse_move)
            self.canvas.bind("<Leave>", self.mouse_leave)
        else:
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Leave>")
            self.mouse_leave(None)
    def mouse_move(self, event):
        x, y = event.x, event.y
        mag_sz = 150  # Adjust the size as desired
        reg = (x - mag_sz, y - mag_sz, x + mag_sz, y + mag_sz)
        im = ImageGrab.grab(reg)
        self.magnifying_prompt(im)
    def magnifying_prompt(self, image):
        if not self.win_mag:
            # Create a new magnifying window
            self.win_mag = Toplevel()
            self.win_mag.overrideredirect(True)
            self.win_mag.geometry("200x200")  # Set the desired fixed size
            self.mag_label = Label(self.win_mag)
            self.mag_label.pack()
        width, height = self.win_mag.winfo_width(), self.win_mag.winfo_height()
        resized_image = image.resize((width, height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        self.mag_label.configure(image=photo)
        self.mag_label.image = photo
    def mouse_leave(self, event):
        if self.win_mag: # destroying window
            self.win_mag.destroy()
            self.win_mag ,self.mag_label = None, None
    
    #===========================================
    # undo and redo 
    #=========================================== 
    def on_undo(self):
        if self.undo_stack:
            last_action = self.undo_stack.pop()
            self.redo_stack.append(last_action)
            self.canvas.delete(last_action)

    def on_redo(self):
        if self.redo_stack:
            last_action = self.redo_stack.pop()
            self.undo_stack.append(last_action)
            line_id = self.canvas.create_line(*self.canvas.coords(last_action), fill=self.color_brush, wid=self.outline_sz.get())
            self.undo_stack[-1] = line_id

    def generic_end(self, event):
        self.prev_a, self.prev_b = None, None
        self.shape_type = None
        self.undo_stack.append(list(self.selected_objects))
        self.selected_objects1 = []
    
    #run mainloop code
    def runner(self):
        self.console.resizable(False , False)
        self.console.mainloop()

    #} end of class
#                                                 ===========main body============

screen_wid = 1405
screen_heg = 750
My_Paint(screen_wid, screen_heg, "PAINT").runner()

