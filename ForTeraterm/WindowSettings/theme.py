
import tkinter
from tkinter.constants import NORMAL
from typing import Any, Callable, List, Literal, Tuple
from typing_extensions import Literal
import customtkinter
from .conf import appconf

class Theme:
    def __init__(self) -> None:
        self.theme_dict = {
            "default":[
                "#F2F2F2",  # font color1
                "#A6A6A6",  # high light
                "#595959",  # back2
                "#262626",  # back1
                "#0D0D0D",  # font color2
                0,          # mode
            ],
            "deepgreen":[
                "#F2EFE9",  # font color1
                "#477346",  # high light
                "#224021",  # back2
                "#142615",  # back1
                "#010D00",  # font color2
                1,          # mode
            ],
            "felixblu":[
                "#6683D9",  # font color1
                "#577EF2",  # high light
                "#5068F2",  # back2
                "#262626",  # back1
                "#0D0D0D",  # font color2
                1,          # mode
            ],
            "retro":[
                "#8C8C8C",  # font color1
                "#454C59",  # high light
                "#595651",  # back2
                "#403F3C",  # back1
                "#262523",  # font color2
                1,          # mode
            ],
            "dolche":[
                "#F2E6CE",  # font color1
                "#D98C5F",  # high light
                "#D96236",  # back2
                "#593C2C",  # back1
                "#103B40",  # font color2
                0,          # mode
            ],
            "brown":[
                "#F2F1F0",  # font color1
                "#D9D0C7",  # high light
                "#BFB4AA",  # back2
                "#73655D",  # back1
                "#8C8079",  # font color2
                0,          # mode
            ],
            "royal":[
                "#F2F2F2",  # font color1
                "#F2A391",  # high light
                "#F28888",  # back2
                "#193540",  # back1
                "#011126",  # font color2
                1,          # mode
            ],
            "passionred":[
                "#D97C2B",  # font color1
                "#F24405",  # high light
                "#BF2604",  # back2
                "#731702",  # back1
                "#0D0D0D",  # font color2
                1,          # mode
            ],
            "cutepink":[
                "#EBEBF2",  # font color1
                "#F23D3D",  # high light
                "#D9328E",  # back2
                "#A63251",  # back1
                "#8C0712",  # font color2
                0,          # mode
            ],
            "saler":[
                "#F2E7DC",  # font color1
                "#F2766B",  # high light
                "#F2766B",  # back2
                "#03258C",  # back1
                "#03178C",  # font color2
                0,          # mode
            ],
            "neon":[
                "#F2E963",  # font color1
                "#DFF250",  # high light
                "#99A638",  # back2
                "#0D0D0D",  # back1
                "#0D0D0D",  # font color2
                0,          # mode
            ],
            "logosmarks":[
                "#D90D32",  # font color1
                "#BF0404",  # high light
                "#D90416",  # back2
                "#F2E7DC",  # back1
                "#F2E7DC",  # font color2
                0,          # mode
            ],
            "armageddon":[
                "#F25ECB",  # font color1
                "#3FBF77",  # high light
                "#6443D9",  # back2
                "#F2F2F2",  # back1
                "#F25ECB",  # font color2
                0,          # mode
            ],
            # "":[
            #     "",  # font color1
            #     "",  # high light
            #     "",  # back2
            #     "",  # back1
            #     "",  # font color2
            #     0,          # mode
            # ],
            # "":[
            #     "",  # font color1
            #     "",  # high light
            #     "",  # back2
            #     "",  # back1
            #     "",  # font color2
            #     0,          # mode
            # ],
            # "":[
            #     "",  # font color1
            #     "",  # high light
            #     "",  # back2
            #     "",  # back1
            #     "",  # font color2
            #     0,          # mode
            # ],
        }
        self.set_theme()
        
    def set_theme(self):
        self.theme_set = appconf.get_data("Theme")
        if self.theme_set not in self.theme_dict.keys():
            appconf.set_data("Theme",list(self.theme_dict.keys())[0])
            self.theme_set =  list(self.theme_dict.keys())[0]
        self.font_color1    = self.theme_dict[self.theme_set][0]
        self.high_light     = self.theme_dict[self.theme_set][1]
        self.back2          = self.theme_dict[self.theme_set][2]
        self.back1          = self.theme_dict[self.theme_set][3]
        self.font_color2    = self.theme_dict[self.theme_set][4]
        self.mode           = self.theme_dict[self.theme_set][5]
        self.mode = "light" if self.mode == 1 else "dark"
    

theme = Theme()
from typing import Union, Tuple, Callable, Optional, Any


setfont    = customtkinter.CTkFont(size=12,family=appconf.get_data("font"))
setfont_b = customtkinter.CTkFont(size=12, weight="bold",family=appconf.get_data("font"))


class ThemeCTKLabel_1(customtkinter.CTkLabel):
    def __init__(self,
            master: Any,
            width: int = 0,
            height: int = 28,
            corner_radius: Optional[int] = 10,

            bg_color: Union[str, Tuple[str, str]] = "transparent",
            fg_color: Optional[Union[str, Tuple[str, str]]] = theme.back1,
            text_color: Optional[Union[str, Tuple[str, str]]] = theme.font_color1,
            text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

            text: str = "",
            font: Optional[Union[tuple, CTkFont]] = setfont,
            image: Union[CTkImage, None] = None,
            compound: str = "left",
            anchor: str = "center",  # label anchor: center, n, e, s, w
            wraplength: int = 0,
            **kwargs):
        super().__init__(
            master
            , width
            , height
            , corner_radius
            , bg_color
            , fg_color
            , text_color
            , text_color_disabled
            , text
            , font
            , image
            , compound
            , anchor
            , wraplength
            , **kwargs)


class ThemeCTKLabel_1b(customtkinter.CTkLabe1):
    def __init__(self
            , master: Any
            , width: int = 0
            , height: int = 28
            , corner_radius: int | None = 10
            , bg_color: str | Tuple[str, str] = "transparent"
            , fg_color: str | Tuple[str, str] | None = theme.back1
            , text_color: str | Tuple[str, str] | None = theme.font_color1
            , text_color_disabled: str | Tuple[str, str] | None = None
            , text: str = ""
            , font: tuple | customtkinter.CTkFont | None = setfont_b
            , image: customtkinter.CTkImage | None = None
            , compound: str = "left"
            , anchor: str = "center"
            , wraplength: int = 0
            , **kwargs):
        super().__init__(
            master
            , width
            , height
            , corner_radius
            , bg_color
            , fg_color
            , text_color
            , text_color_disabled
            , text
            , font
            , image
            , compound
            , anchor
            , wraplength
            , **kwargs)
        
        
class ThemeCTKLabel_2(customtkinter.CTkLabel):
    def __init__(self
            , master: Any
            , width: int = 0
            , height: int = 28
            , corner_radius: int | None = 10
            , bg_color: str | Tuple[str, str] = "transparent"
            , fg_color: str | Tuple[str, str] | None = theme.back2
            , text_color: str | Tuple[str, str] | None = theme.font_color2
            , text_color_disabled: str | Tuple[str, str] | None = None
            , text: str = ""
            , font: tuple | customtkinter.CTkFont | None = setfont
            , image: customtkinter.CTkImage | None = None
            , compound: str = "left"
            , anchor: str = "center"
            , wraplength: int = 0
            , **kwargs):
        super().__init__(
            master
            , width
            , height
            , corner_radius
            , bg_color
            , fg_color
            , text_color
            , text_color_disabled
            , text
            , font
            , image
            , compound
            , anchor
            , wraplength
            , **kwargs)


class ThemeCTKLabel_2b(customtkinter.CTkLabel):
    def __init__(self
            , master: Any
            , width: int = 0
            , height: int = 28
            , corner_radius: int | None = 10
            , bg_color: str | Tuple[str, str] = "transparent"
            , fg_color: str | Tuple[str, str] | None = theme.back2
            , text_color: str | Tuple[str, str] | None = theme.font_color2
            , text_color_disabled: str | Tuple[str, str] | None = None
            , text: str = "CTkLabel"
            , font: tuple | customtkinter.CTkFont | None = setfont_b
            , image: customtkinter.CTkImage | None = None
            , compound: str = "left"
            , anchor: str = "center"
            , wraplength: int = 0
            , **kwargs):
        super().__init__(
            master
            , width
            , height
            , corner_radius
            , bg_color
            , fg_color
            , text_color
            , text_color_disabled
            , text
            , font
            , image
            , compound
            , anchor
            , wraplength
            , **kwargs)
        
        
        

class ThemeCTKScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self
            , master: Any
            , width: int = 200
            , height: int = 200
            , corner_radius: int | str | None = None
            , border_width: int | str | None = None
            , bg_color: str | Tuple[str] = "transparent"
            , fg_color: str | Tuple[str] | None = theme.back1
            , border_color: str | Tuple[str] | None = None
            , scrollbar_fg_color: str | Tuple[str] | None = None
            , scrollbar_button_color: str | Tuple[str] | None = None
            , scrollbar_button_hover_color: str | Tuple[str] | None = None
            , label_fg_color: str | Tuple[str] | None = None
            , label_text_color: str | Tuple[str] | None = None
            , label_text: str = ""
            , label_font: Tuple | customtkinter.CTkFont | None = None
            , label_anchor: str = "center"
            , orientation: Literal['vertical'] | Literal['horizontal'] = "vertical"):
        super().__init__(master
            , width
            , height
            , corner_radius
            , border_width
            , bg_color
            , fg_color
            , border_color
            , scrollbar_fg_color
            , scrollbar_button_color
            , scrollbar_button_hover_color
            , label_fg_color
            , label_text_color
            , label_text
            , label_font
            , label_anchor
            , orientation)


class ThemeCTKFrame_1(customtkinter.CTkFrame):
    def __init__(self
            , master: Any
            , width: int = 200
            , height: int = 200
            , corner_radius: int | str | None = None
            , border_width: int | str | None = None
            , bg_color: str | Tuple[str] = "transparent"
            , fg_color: str | Tuple[str] | None = theme.back1
            , border_color: str | Tuple[str] | None = None
            , background_corner_colors: Tuple[str | Tuple[str]] | None = None
            , overwrite_preferred_drawing_method: str | None = None
            , **kwargs):
        super().__init__(master
            , width
            , height
            , corner_radius
            , border_width
            , bg_color
            , fg_color
            , border_color
            , background_corner_colors
            , overwrite_preferred_drawing_method
            , **kwargs)
        

class ThemeCTKComboBox_1(customtkinter.CTkComboBox):
    def __init__(self
            , master: Any
            , width: int = 140
            , height: int = 28
            , corner_radius: int | None = None
            , border_width: int | None = None
            , bg_color: str | Tuple[str] = "transparent"
            , fg_color: str | Tuple[str] | None = theme.back1
            , border_color: str | Tuple[str] | None = None
            , button_color: str | Tuple[str] | None = None
            , button_hover_color: str | Tuple[str] | None = None
            , dropdown_fg_color: str | Tuple[str] | None = None
            , dropdown_hover_color: str | Tuple[str] | None = None
            , dropdown_text_color: str | Tuple[str] | None = None
            , text_color: str | Tuple[str] | None = theme.font_color1
            , text_color_disabled: str | Tuple[str] | None = None
            , font: Tuple | customtkinter.CTkFont | None = setfont
            , dropdown_font: Tuple | customtkinter.CTkFont | None = None
            , values: List[str] | None = None
            , state: str = tkinter.NORMAL
            , hover: bool = True
            , variable: customtkinter.Variable | None = None
            , command: Callable[[str]
            , Any] | None = None
            , justify: str = "left"
            , **kwargs):
        super().__init__(master
            , width
            , height
            , corner_radius
            , border_width
            , bg_color
            , fg_color
            , border_color
            , button_color
            , button_hover_color
            , dropdown_fg_color
            , dropdown_hover_color
            , dropdown_text_color
            , text_color
            , text_color_disabled
            , font
            , dropdown_font
            , values
            , state
            , hover
            , variable
            , command
            , justify
            , **kwargs)

class ThemeCTKButton(customtkinter.CTkButton):
    def __init__(self
            , master: Any
            , width: int = 140
            , height: int = 28
            , corner_radius: int | None = None
            , border_width: int | None = None
            , border_spacing: int = 2
            , bg_color: str | Tuple[str] = "transparent"
            , fg_color: str | Tuple[str] | None = theme.back1
            , hover_color: str | Tuple[str] | None = None
            , border_color: str | Tuple[str] | None = None
            , text_color: str | Tuple[str] | None = theme.font_color1
            , text_color_disabled: str | Tuple[str] | None = None
            , background_corner_colors: Tuple[str | Tuple[str]] | None = None
            , round_width_to_even_numbers: bool = True
            , round_height_to_even_numbers: bool = True
            , text: str = ""
            , font: Tuple | customtkinter.CTkFont | None = setfont
            , textvariable: customtkinter.Variable | None = None
            , image: customtkinter.CTkImage | Any | None = None
            , state: str = "normal"
            , hover: bool = True
            , command: Callable[[]
            , Any] | None = None
            , compound: str = "left"
            , anchor: str = "center"
            , **kwargs):
        super().__init__(master
            , width
            , height
            , corner_radius
            , border_width
            , border_spacing
            , bg_color
            , fg_color
            , hover_color
            , border_color
            , text_color
            , text_color_disabled
            , background_corner_colors
            , round_width_to_even_numbers
            , round_height_to_even_numbers
            , text
            , font
            , textvariable
            , image
            , state
            , hover
            , command
            , compound
            , anchor
            , **kwargs)

class ThemeCTKSlider(customtkinter.CTkSlider):
    def __init__(self
            , master: Any
            , width: int | None = None
            , height: int | None = None
            , corner_radius: int | None = None
            , button_corner_radius: int | None = None
            , border_width: int | None = None
            , button_length: int | None = None
            , bg_color: str | Tuple[str] = "transparent"
            , fg_color: str | Tuple[str] | None = theme.back1
            , border_color: str | Tuple[str] = "transparent"
            , progress_color: str | Tuple[str] | None = theme.back2
            , button_color: str | Tuple[str] | None = theme.font_color2
            , button_hover_color: str | Tuple[str] | None = theme.high_light
            , from_: int = 0
            , to: int = 1
            , state: str = "normal"
            , number_of_steps: int | None = None
            , hover: bool = True
            , command: Callable[[float], Any] | None = None
            , variable: customtkinter.Variable | None = None
            , orientation: str = "horizontal"
            , **kwargs):
        super().__init__(master
            , width
            , height
            , corner_radius
            , button_corner_radius
            , border_width
            , button_length
            , bg_color
            , fg_color
            , border_color
            , progress_color
            , button_color
            , button_hover_color
            , from_
            , to
            , state
            , number_of_steps
            , hover
            , command
            , variable
            , orientation
            , **kwargs
        )


