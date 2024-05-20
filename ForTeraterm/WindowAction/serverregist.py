
import tkinter
from typing import Tuple
import customtkinter
from tkinter import filedialog
from ..WindowSettings.theme import theme
from ..WindowSettings.conf import appconf
from ..WindowSettings.image import imginst
from ..Language.apptext import AppText

class ServerRegist(customtkinter.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs):
        self.trans = AppText(appconf.get_data("lang"))
        label_text = ""
        border_width = 20
        self.width = appconf.get_data("width")
        self.height = appconf.get_data("height")
        self.macro_path = appconf.get_data("macro_path")
        
        self.font = customtkinter.CTkFont(size=12,family=appconf.get_data("font"))
        self.font_b = customtkinter.CTkFont(size=15, weight="bold",family=appconf.get_data("font"))
        
        super().__init__(master,
            width                           = self.width
            ,height                         = self.height
            ,corner_radius                  = 0                            
            ,fg_color                       = theme.back1
            # ,scrollbar_fg_color             = theme.back2           
            # ,scrollbar_button_color         = theme.font_color2       
            # ,scrollbar_button_hover_color   = theme.high_light               
            # ,label_text_color               = theme.font_color1              
            # ,label_text                     = label_text                   
            # ,label_font                     = label_font 
            )
        
        self.grid(row=0, column=0, sticky="nw")
        self.call_serverregist_frame()
    
    def call_serverregist_frame(self):
        bar_width = 20
        padx = 5
        pady = 5
        row_i = 0
        label = self.trans.translate("ServerAccess")
        
        self.title_label = customtkinter.CTkLabel(self
            ,text=label
            ,width = self.width - 10
            ,height = 25
            ,corner_radius = 10
            ,bg_color = "transparent"
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_server
            ,compound = "left"
            ,anchor = "center"
            ,wraplength = 0
            )
        self.title_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
        
        self.item_icons_frame = customtkinter.CTkFrame(self
            , width             = self.width
            , height            = 70
            , fg_color          = theme.back2
            ,corner_radius=0
        )
        
        self.item_icons_frame.grid(row=row_i, column=0, padx=0, pady=pady*2,sticky='ew',columnspan=2)
        
        ###############################################################################################
        
        icon_frame_row_cell = 35
        
        row_i += 1
        self.enry_ = customtkinter.CTkEntry(self.item_icons_frame
            ,variable=self.check_var_macro
            ,onvalue="on"
            ,offvalue="off"
            ,text_color=theme.font_color1
            ,hover_color=theme.high_light
            ,text=self.trans.translate("RunMacro")
        )
        self.checkbox_macro.grid(row=row_i, column=0,padx=padx, pady=pady,sticky='ew')
        self.checkbox_macro.place(x=self.width/5,y=icon_frame_row_cell,anchor=customtkinter.CENTER)
        
        row_i += 1
        
        files = glob(os.path.join(self.macro_path,"*.txt"))
        files = [os.path.basename(f) for f in files]
        self.macro_combobox = customtkinter.CTkComboBox(self.item_icons_frame
            ,font = font
            ,values=files
        )
        self.macro_combobox.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        self.macro_combobox.place(x=self.width/2,y=icon_frame_row_cell,anchor=customtkinter.CENTER)
        self.macro_combobox.set("")
        
        row_i += 1
        
        self.server_launch = customtkinter.CTkButton(self.item_icons_frame
            ,fg_color=theme.back1
            ,text=self.trans.translate("BatchServerAccess")
            ,font = font
            ,image=imginst.image_server
            ,text_color=theme.font_color1
            ,hover_color=theme.high_light
            ,command=self.launch_servers
        )
        self.server_launch.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        self.server_launch.place(x=self.width*4/5,y=icon_frame_row_cell,anchor=customtkinter.CENTER)
        
        ###############################################################################################
        
        row_i += 1
        
        self.Scroll_frame = customtkinter.CTkScrollableFrame(self
            ,width                           = self.width - padx * 2 - bar_width
            ,height                         = self.height  / 3
            ,corner_radius                  = 0                  
            ,fg_color                       = theme.back1                     
            ,scrollbar_fg_color             = theme.back2            
            ,scrollbar_button_color         = theme.font_color2        
            ,scrollbar_button_hover_color   = theme.high_light 
            )
        self.Scroll_frame.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
    
    @staticmethod
    def open_file_dialog(filetypes,initialdir):
        # Open a file dialog and get the selected file path
        # [('data files','*.csv;*.txt')]
        file_path = filedialog.askopenfilename(filetypes=filetypes,initialdir=initialdir)
        if file_path:
            return file_path
    