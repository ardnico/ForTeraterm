
import os
import pyautogui
import tkinter as tk
import customtkinter
from pathlib import Path
from .theme import theme
from tkinter import filedialog
from ..WindowSettings.conf import appconf
from ..WindowSettings.image import imginst
from ..util import messsagebox
from ..Language.apptext import AppText

class Edit(customtkinter.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs):
        self.trans = AppText(appconf.get_data("lang"))
        self.width = appconf.get_data("width")
        self.height = appconf.get_data("height")
        self.font = appconf.get_data("font")
        self.font = customtkinter.CTkFont(size=20,family=self.font)
        self.font_b = customtkinter.CTkFont(size=20, weight="bold",family=self.font)
        
        super().__init__(master,
            width                           = self.width
            ,height                         = self.height
            ,corner_radius                  = 0                            
            ,fg_color                       = theme.back1
            )
        
        self.grid(row=0, column=0, sticky="nw")
        self.call_edit_frame()
    
    def call_edit_frame(self):
        bar_width = 20
        padx = 5
        pady = 5
        row_i = 0
        label = self.trans.translate("EditSettings")
        
        self.title_label = customtkinter.CTkLabel(self
            ,text=label
            ,width = self.width-10
            ,height = 25
            ,corner_radius = 10
            ,bg_color = "transparent"
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_setting
            ,compound = "left"
            ,anchor = "center"
            ,wraplength = 0
            )
        self.title_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
        
        self.item_frame = customtkinter.CTkScrollableFrame(self
            , width             = self.width - bar_width * 2
            , height            = self.height * 12 / 15
            , fg_color          = theme.back2
            ,corner_radius=0                
            ,scrollbar_fg_color             = theme.back2            
            ,scrollbar_button_color         = theme.font_color2        
            ,scrollbar_button_hover_color   = theme.high_light 
        )
        
        self.item_frame.grid(row=row_i, column=0, padx=0, pady=pady*2,sticky='ew',columnspan=2)
        
        ###############################################################################################
        # select menu
        
        icon_frame_row_cell = 35
        
        row_i += 1
        
        # FilePathSettings
        self.FilePathSettings_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("FilePathSettings")
            ,width = self.width
            ,corner_radius = 0
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_file
            ,compound = "left"
            ,anchor = "center"
            )
        self.FilePathSettings_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=6)
        
        #######################################################################################################
        path_list = [
            ["data_path"        ,"dir"  ,self.trans.translate("DataPath")],
            ["log_path"         ,"dir"  ,self.trans.translate("LogPath")],
            ["macro_path"       ,"dir"  ,self.trans.translate("MacroPath")],
            ["TeratermPath"     ,"exe"  ,self.trans.translate("TeratermPath")],
            ["TeratermIniPath"  ,"ini"  ,self.trans.translate("TeratermIniPath")],
        ]
        self.path_data_label = []
        self.path_data_entry = []
        self.path_data_button = []
        cell = self.width / 9
        for i,key in enumerate(path_list):
            row_i += 1
            self.path_data_label.append(customtkinter.CTkLabel(self.item_frame
                ,text = key[2]
                ,width = cell
                ,corner_radius = 0
                ,fg_color = theme.back2
                ,text_color = theme.font_color2
                ,font = self.font_b
                ,image = imginst.image_file
                ,compound = "left"
                ,anchor = "w"
                )
            )
            self.path_data_label[i].grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
            
            self.path_data_entry.append(customtkinter.CTkEntry(self.item_frame
                ,font = self.font
                ,width = cell*4
                )
            )
            self.path_data_entry[i].grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew',columnspan=4)
            self.path_data_entry[i].insert(0,appconf.get_data(key[0]))
            
            if key[1]=="dir":
                tmp_img = imginst.image_directory
            else:
                tmp_img = imginst.image_file
            
            self.path_data_button.append(customtkinter.CTkButton(self.item_frame
                ,fg_color=theme.back1
                ,width=cell
                ,text=self.trans.translate("Open")
                ,font = self.font
                ,image=tmp_img
                ,text_color=theme.font_color1
                ,hover_color=theme.high_light
                ,command=lambda i=i,key=key: self.open_file(self.path_data_entry[i],key)
                )
            )
            self.path_data_button[i].grid(row=row_i, column=5, padx=padx, pady=pady,sticky='ew')
        
        #######################################################################################################
        
        row_i += 1
        
        # DisplaySettings
        self.DisplaySettings_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("DisplaySettings")
            ,width = self.width
            ,corner_radius = 0
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_icon_app_design
            ,compound = "left"
            ,anchor = "center"
            )
        self.DisplaySettings_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=6)
        
        row_i += 1
        
        self.Theme_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("Theme")
            ,width = cell
            ,corner_radius = 1
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_icon_color_wheel
            ,compound = "left"
            ,anchor = "w"
            )
        self.Theme_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.Theme_combobox = customtkinter.CTkComboBox(self.item_frame
            ,width=cell*4 - bar_width
            ,font = self.font
            ,values=list(theme.theme_dict.keys())
        )
        self.Theme_combobox.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew',columnspan=4)
        self.Theme_combobox.set(appconf.get_data("Theme"))
        
        row_i += 1
        
        self.lang_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("LanguageSelection")
            ,width = cell
            ,corner_radius = 1
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_lang
            ,compound = "left"
            ,anchor = "w"
            )
        self.lang_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.lang_combobox = customtkinter.CTkComboBox(self.item_frame
            ,width=cell*4 -bar_width
            ,font = self.font
            ,values=self.trans.lang_list()
        )
        self.lang_combobox.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew',columnspan=4)
        self.lang_combobox.set(appconf.get_data("lang"))
        
        row_i += 1
        
        self.font_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("Font")
            ,width = cell
            ,corner_radius = 1
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_font
            ,compound = "left"
            ,anchor = "w"
            )
        self.font_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.font_combobox = customtkinter.CTkComboBox(self.item_frame
            ,width=cell*4 -bar_width
            ,font = self.font
            ,values=tk.font.families()
        )
        self.font_combobox.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew',columnspan=4)
        self.font_combobox.set(appconf.get_data("font"))
        
        row_i += 1
        
        self.width_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("Width")
            ,width = cell
            ,corner_radius = 1
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_width
            ,compound = "left"
            ,anchor = "center"
            )
        self.width_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        self.height_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("Height")
            ,width = cell
            ,corner_radius = 1
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_height
            ,compound = "left"
            ,anchor = "center"
            )
        self.height_label.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i += 1
        scr_w,scr_h= pyautogui.size()
        self.sliderval_width = tk.IntVar(value=appconf.get_data("width"))
        self.slider_width = customtkinter.CTkSlider(self.item_frame
            ,from_=200
            ,number_of_steps=scr_h-199
            ,width=cell
            ,to=scr_w
            ,command=self.set_width
            ,button_color=theme.font_color2
            ,button_hover_color=theme.high_light
            ,variable=self.sliderval_width
        )
        self.slider_width.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        self.sliderval_height = tk.IntVar(value=appconf.get_data("height"))
        self.slider_height = customtkinter.CTkSlider(self.item_frame
            ,from_=200
            ,to=scr_h
            ,number_of_steps=scr_h-199
            ,width=cell
            ,command=self.set_height
            ,button_color=theme.font_color2
            ,button_hover_color=theme.high_light
            ,variable=self.sliderval_height
        )
        self.slider_height.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i += 1
        
        # FilePathSettings
        self.Other_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("Other")
            ,width = self.width
            ,corner_radius = 0
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_other
            ,compound = "left"
            ,anchor = "center"
            )
        self.Other_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=6)
        
        row_i += 1
        
        self.loglevel_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.trans.translate("LogLevel")
            ,width = cell * 3
            ,corner_radius = 0
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,image = imginst.image_pen
            ,compound = "left"
            ,anchor = "center"
            )
        self.loglevel_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i += 1
        self.log_species = {
            0:"DEBUG",
            1:"INFO",
            2:"WARNING",
            3:"ERROR",
            4:"CRITICAL",
        }
        self.loglevel_status_label = customtkinter.CTkLabel(self.item_frame
            ,text=self.log_species[appconf.get_data("loglevel")]
            ,width = cell * 3
            ,corner_radius = 0
            ,fg_color = theme.back2
            ,text_color = theme.font_color2
            ,font = self.font_b
            ,compound = "left"
            ,anchor = "center"
            )
        self.loglevel_status_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i += 1
        self.sliderval_loglevel = tk.IntVar(value=appconf.get_data("loglevel"))
        self.slider_loglevel = customtkinter.CTkSlider(self.item_frame
            ,from_=0
            ,to=4
            ,number_of_steps=4
            ,width = cell * 3
            ,command=self.set_loglevel
            ,button_color=theme.font_color2
            ,button_hover_color=theme.high_light
            ,variable=self.sliderval_loglevel
        )
        self.slider_loglevel.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i += 1
        
        self.update_button = customtkinter.CTkButton(self
            , width             = self.width - bar_width * 2
            , fg_color          = theme.back1
            ,corner_radius      = 1               
            ,hover_color        = theme.high_light
            ,text               = self.trans.translate("Save")
            ,command            = self.set_datas
        )
        
        self.update_button.grid(row=row_i, column=0, padx=0, pady=0,sticky='ew',columnspan=2)
        
    ###############################################################################################
    
    @staticmethod
    def open_file_dialog(filetypes,initialdir):
        # Open a file dialog and get the selected file path
        # [('data files','*.csv;*.txt')]
        file_path = filedialog.askopenfilename(filetypes=filetypes,initialdir=initialdir)
        if file_path:
            return file_path
        return None
    
    def open_file(self,data_path_obj,key):
        initialdir = data_path_obj.get()
        if key[1] == "dir":
            if initialdir is None:
                initialdir = Path(os.environ['USERPROFILE']) / 'Documents'
            file_path = filedialog.askdirectory(title=key[0],initialdir=initialdir)
        elif key[1] == "exe":
            filetypes = [('exe file','*.exe;')]
            if initialdir:
                initialdir = os.path.dirname(initialdir)
            else:
                initialdir = Path(os.environ['USERPROFILE']) / 'Documents'
            file_path = self.open_file_dialog(filetypes,initialdir)
        elif key[1] == "ini":
            filetypes = [('ini file','*.ini;')]
            if initialdir:
                initialdir = os.path.dirname(initialdir)
            else:
                initialdir = Path(os.environ['USERPROFILE']) / 'Documents'
            file_path = self.open_file_dialog(filetypes,initialdir)
        
        if file_path:
            data_path_obj.delete(0,"end")
            data_path_obj.insert(0,file_path.replace("/","\\"))
    
    def set_combobox(self,tmp_val,key):
        appconf.set_data(key,tmp_val)
        messsagebox.show_info(message=self.trans.translate("SettingsChangeReflect"))
    
    def set_loglevel(self,tmp_val):
        appconf.set_data("loglevel",int(tmp_val))
        self.loglevel_status_label.configure(text=self.log_species[int(tmp_val)])
    
    def set_width(self,tmp_val):
        appconf.set_data("width",int(tmp_val))
    
    def set_height(self,tmp_val):
        appconf.set_data("height",int(tmp_val))
    
    def set_datas(self):
        path_list = [
            "data_path"        ,
            "log_path"         ,
            "macro_path"       ,
            "TeratermPath"     ,
            "TeratermIniPath"  ,
        ]
        for i,key in enumerate(path_list):
            tmp_val = self.path_data_entry[i].get()
            if tmp_val:
                appconf.set_data(key,tmp_val)
        theme_val = self.Theme_combobox.get()
        appconf.set_data("Theme",theme_val)
        lang_val = self.lang_combobox.get()
        appconf.set_data("lang",lang_val)
        font_val = self.font_combobox.get()
        appconf.set_data("font",font_val)
        