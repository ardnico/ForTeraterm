
import tkinter
from typing import Tuple
import customtkinter
from .theme import theme
from ..WindowSettings.conf import appconf
from ..Language.apptext import AppText

class Edit(customtkinter.CTkScrollableFrame):
    def __init__(
        self,
        master,
        **kwargs):
        self.trans = AppText(appconf.get_data("lang"))
        label_text = self.trans.translate("Settings")
        
        border_width = int(appconf.get_data("width")/9)
        self.width = appconf.get_data("width")-border_width*2
        self.height = appconf.get_data("height")
        self.font = appconf.get_data("font")
        
        corner_radius = 0
        border_width                 = None                 # : int | str | None = None,
        bg_color                     = "transparent"        # : str | Tuple[str, str] = "transparent",
        fg_color                     = theme.back1          # : str | Tuple[str, str] | None = None,
        border_color                 = None                 # : str | Tuple[str, str] | None = None,
        scrollbar_fg_color           = theme.back2          # : str | Tuple[str, str] | None = None,
        scrollbar_button_color       = theme.font_color2    # : str | Tuple[str, str] | None = None,
        scrollbar_button_hover_color = theme.high_light     # : str | Tuple[str, str] | None = None,
        label_fg_color               = None                 # : str | Tuple[str, str] | None = None,
        label_text_color             = theme.font_color1    # : str | Tuple[str, str] | None = None,
        label_anchor                 = "center"             # : str = "center"
        label_font                   = customtkinter.CTkFont(size=20, weight="bold",family=self.font)
        
        super().__init__(master,
            width                           = self.width
            ,height                         = self.height
            ,corner_radius                  = corner_radius
            ,border_width                   = border_width                 
            ,bg_color                       = bg_color                     
            ,fg_color                       = fg_color                     
            ,border_color                   = border_color                 
            ,scrollbar_fg_color             = scrollbar_fg_color           
            ,scrollbar_button_color         = scrollbar_button_color       
            ,scrollbar_button_hover_color   = scrollbar_button_hover_color 
            ,label_fg_color                 = label_fg_color               
            ,label_text_color               = label_text_color             
            ,label_text                     = label_text                   
            ,label_font                     = label_font                   
            ,label_anchor                   = label_anchor 
            **kwargs)
        
        self.grid(row=0, column=0, sticky="nw")
        self.call_edit_frame()
    
    def call_edit_frame(self):
        pass