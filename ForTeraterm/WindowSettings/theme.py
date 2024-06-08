
import customtkinter
from .conf import appconf

class ThemeManager:
    themes ={
        "default": {
            "font_color1": "#F2F2F2",
            "highlight": "#A6A6A6",
            "back2": "#595959",
            "back1": "#262626",
            "font_color2": "#0D0D0D",
            "mode": "light"
        },
        "deepgreen": {
            "font_color1": "#F2EFE9",
            "highlight": "#477346",
            "back2": "#224021",
            "back1": "#142615",
            "font_color2": "#010D00",
            "mode": "dark"
        },
        "felixblu": {
            "font_color1": "#6683D9",
            "highlight": "#577EF2",
            "back2": "#5068F2",
            "back1": "#262626",
            "font_color2": "#0D0D0D",
            "mode": "dark"
        },
        "retro": {
            "font_color1": "#8C8C8C",
            "highlight": "#454C59",
            "back2": "#595651",
            "back1": "#403F3C",
            "font_color2": "#262523",
            "mode": "dark"
        },
        "dolche": {
            "font_color1": "#F2E6CE",
            "highlight": "#D98C5F",
            "back2": "#D96236",
            "back1": "#593C2C",
            "font_color2": "#103B40",
            "mode": "light"
        },
        "brown": {
            "font_color1": "#F2F1F0",
            "highlight": "#D9D0C7",
            "back2": "#BFB4AA",
            "back1": "#73655D",
            "font_color2": "#8C8079",
            "mode": "light"
        },
        "royal": {
            "font_color1": "#F2F2F2",
            "highlight": "#F2A391",
            "back2": "#F28888",
            "back1": "#193540",
            "font_color2": "#011126",
            "mode": "dark"
        },
        "passionred": {
            "font_color1": "#D97C2B",
            "highlight": "#F24405",
            "back2": "#BF2604",
            "back1": "#731702",
            "font_color2": "#0D0D0D",
            "mode": "dark"
        },
        "cutepink": {
            "font_color1": "#EBEBF2",
            "highlight": "#F23D3D",
            "back2": "#D9328E",
            "back1": "#A63251",
            "font_color2": "#8C0712",
            "mode": "light"
        },
        "saler": {
            "font_color1": "#F2E7DC",
            "highlight": "#F2766B",
            "back2": "#F2766B",
            "back1": "#03258C",
            "font_color2": "#03178C",
            "mode": "light"
        },
        "neon": {
            "font_color1": "#F2E963",
            "highlight": "#DFF250",
            "back2": "#99A638",
            "back1": "#0D0D0D",
            "font_color2": "#0D0D0D",
            "mode": "light"
        },
        "logosmarks": {
            "font_color1": "#D90D32",
            "highlight": "#BF0404",
            "back2": "#D90416",
            "back1": "#F2E7DC",
            "font_color2": "#F2E7DC",
            "mode": "light"
        },
        "armageddon": {
            "font_color1": "#F25ECB",
            "highlight": "#3FBF77",
            "back2": "#6443D9",
            "back1": "#F2F2F2",
            "font_color2": "#F25ECB",
            "mode": "light"
        },
        "sunset": {
            "font_color1": "#FFD1DC",
            "highlight": "#FF69B4",
            "back2": "#8B0000",
            "back1": "#FF1493",
            "font_color2": "#4B0082",
            "mode": "dark"
        },
        "forest": {
            "font_color1": "#A8E6CF",
            "highlight": "#DCEDC1",
            "back2": "#004D40",
            "back1": "#FFD3B6",
            "font_color2": "#FF8B94",
            "mode": "light"
        },
        "ocean": {
            "font_color1": "#E0F7FA",
            "highlight": "#B2EBF2",
            "back2": "#004D40",
            "back1": "#4DD0E1",
            "font_color2": "#26C6DA",
            "mode": "light"
        },
        "lavender": {
            "font_color1": "#E1BEE7",
            "highlight": "#CE93D8",
            "back2": "#311B92",
            "back1": "#9C27B0",
            "font_color2": "#7B1FA2",
            "mode": "dark"
        },
        "midnight": {
            "font_color1": "#212121",
            "highlight": "#616161",
            "back2": "#212121",
            "back1": "#9E9E9E",
            "font_color2": "#BDBDBD",
            "mode": "dark"
        },
        "tropical": {
            "font_color1": "#FFECB3",
            "highlight": "#FF5722",
            "back2": "#FFEB3B",
            "back1": "#FFCA28",
            "font_color2": "#995400",
            "mode": "light"
        },
        "grayscale": {
            "font_color1": "#E0E0E0",
            "highlight": "#BDBDBD",
            "back2": "#212121",
            "back1": "#616161",
            "font_color2": "#424242",
            "mode": "dark"
        },
        "earth": {
            "font_color1":"#2D1007",
            "highlight": "#8D6E63",
            "back2": "#3E2723",
            "back1": "#6D4C41",
            "font_color2":  "#A1887F",
            "mode": "dark"
        },
        "sky": {
            "font_color1": "#B3E5FC",
            "highlight": "#81D4FA",
            "back2": "#01579B",
            "back1": "#0996d6",
            "font_color2": "#23c9F4",
            "mode": "light"
        },
        "berry": {
            "font_color1": "#F8BBD0",
            "highlight": "#C2185B",
            "back2": "#880E4F",
            "back1": "#EC407A",
            "font_color2": "#c90E43",
            "mode": "dark"
        }
    }
    def __init__(self) -> None:
        self.current_theme = appconf.get_data("Theme")
        self.load_theme(self.current_theme)
    
    def load_theme(self, theme_name: str):
        if theme_name not in list(self.themes.keys()):
            raise ValueError(f"Theme {theme_name} does not exist.")
        theme = self.themes[theme_name]
        self.font_color1 = theme["font_color1"]
        self.highlight = theme["highlight"]
        self.back2 = theme["back2"]
        self.back1 = theme["back1"]
        self.font_color2 = theme["font_color2"]
        self.mode = theme["mode"]
        self.setfont    = customtkinter.CTkFont(size=12,family=appconf.get_data("font"))
        self.setfont_b = customtkinter.CTkFont(size=12, weight="bold",family=appconf.get_data("font"))
        customtkinter.set_appearance_mode(self.mode)
    
    def set_theme(self, theme_name: str):
        self.load_theme(theme_name)
        self.current_theme = theme_name
        appconf.set_data("Theme",theme_name)
        customtkinter.set_appearance_mode(self.mode)


class ThemeLabel1(customtkinter.CTkLabel):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 0,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkLabel",
    font: tuple | CTkFont | None = None,
    image: CTkImage | None = None,
    compound: str = "center",
    anchor: str = "center",
    wraplength: int = 0,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            text_color=kwargs.pop("text_color", theme.font_color1),
            font=kwargs.pop("font", theme.setfont),
            *args,
            **kwargs
        )

class ThemeLabelBold1(customtkinter.CTkLabel):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 0,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkLabel",
    font: tuple | CTkFont | None = None,
    image: CTkImage | None = None,
    compound: str = "center",
    anchor: str = "center",
    wraplength: int = 0,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            text_color=kwargs.pop("text_color", theme.font_color1),
            font=kwargs.pop("font", theme.setfont_b),
            *args,
            **kwargs
        )
        

class ThemeLabel2(customtkinter.CTkLabel):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 0,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkLabel",
    font: tuple | CTkFont | None = None,
    image: CTkImage | None = None,
    compound: str = "center",
    anchor: str = "center",
    wraplength: int = 0,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            text_color=kwargs.pop("text_color", theme.font_color2),
            font=kwargs.pop("font", theme.setfont),
            *args,
            **kwargs
        )

class ThemeLabelBold2(customtkinter.CTkLabel):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 0,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkLabel",
    font: tuple | CTkFont | None = None,
    image: CTkImage | None = None,
    compound: str = "center",
    anchor: str = "center",
    wraplength: int = 0,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            text_color=kwargs.pop("text_color", theme.font_color2),
            font=kwargs.pop("font", theme.setfont_b),
            *args,
            **kwargs
        )
        


class ThemeEntry1(customtkinter.CTkEntry):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    placeholder_text_color: str | Tuple[str, str] | None = None,
    textvariable: Variable | None = None,
    placeholder_text: str | None = None,
    font: tuple | CTkFont | None = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            text_color=kwargs.pop("text_color", theme.font_color1),
            font=kwargs.pop("font", theme.setfont),
            *args,
            **kwargs
        )

class ThemeEntryBold1(customtkinter.CTkEntry):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    placeholder_text_color: str | Tuple[str, str] | None = None,
    textvariable: Variable | None = None,
    placeholder_text: str | None = None,
    font: tuple | CTkFont | None = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            text_color=kwargs.pop("text_color", theme.font_color1),
            font=kwargs.pop("font", theme.setfont_b),
            *args,
            **kwargs
        )

class ThemeEntry2(customtkinter.CTkEntry):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    placeholder_text_color: str | Tuple[str, str] | None = None,
    textvariable: Variable | None = None,
    placeholder_text: str | None = None,
    font: tuple | CTkFont | None = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            text_color=kwargs.pop("text_color", theme.font_color2),
            font=kwargs.pop("font", theme.setfont),
            *args,
            **kwargs
        )

class ThemeEntryBold2(customtkinter.CTkEntry):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    placeholder_text_color: str | Tuple[str, str] | None = None,
    textvariable: Variable | None = None,
    placeholder_text: str | None = None,
    font: tuple | CTkFont | None = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            text_color=kwargs.pop("text_color", theme.font_color2),
            font=kwargs.pop("font", theme.setfont_b),
            *args,
            **kwargs
        )

class ThemeFrame1(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | str | None = None,
    border_width: int | str | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
    overwrite_preferred_drawing_method: str | None = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            *args,
            **kwargs
        )

class ThemeFrame2(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | str | None = None,
    border_width: int | str | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
    overwrite_preferred_drawing_method: str | None = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            *args,
            **kwargs
        )

class ThemeScrollableFrame1(customtkinter.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | str | None = None,
    border_width: int | str | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    scrollbar_fg_color: str | Tuple[str, str] | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    label_fg_color: str | Tuple[str, str] | None = None,
    label_text_color: str | Tuple[str, str] | None = None,
    label_text: str = "",
    label_font: tuple | CTkFont | None = None,
    label_anchor: str = "center",
    orientation: Literal['vertical', 'horizontal'] = "vertical"
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.

        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            label_font=kwargs.pop("label_font", theme.setfont),
            scrollbar_fg_color=kwargs.pop("scrollbar_fg_color", theme.back2),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.font_color2),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeScrollableFrameBold1(customtkinter.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | str | None = None,
    border_width: int | str | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    scrollbar_fg_color: str | Tuple[str, str] | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    label_fg_color: str | Tuple[str, str] | None = None,
    label_text_color: str | Tuple[str, str] | None = None,
    label_text: str = "",
    label_font: tuple | CTkFont | None = None,
    label_anchor: str = "center",
    orientation: Literal['vertical', 'horizontal'] = "vertical"
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.

        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            label_font=kwargs.pop("label_font", theme.setfont_b),
            scrollbar_fg_color=kwargs.pop("scrollbar_fg_color", theme.back2),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.font_color2),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeScrollableFrame2(customtkinter.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | str | None = None,
    border_width: int | str | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    scrollbar_fg_color: str | Tuple[str, str] | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    label_fg_color: str | Tuple[str, str] | None = None,
    label_text_color: str | Tuple[str, str] | None = None,
    label_text: str = "",
    label_font: tuple | CTkFont | None = None,
    label_anchor: str = "center",
    orientation: Literal['vertical', 'horizontal'] = "vertical"
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.

        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            label_font=kwargs.pop("label_font", theme.setfont),
            scrollbar_fg_color=kwargs.pop("scrollbar_fg_color", theme.back1),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.font_color1),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeScrollableFrameBold2(customtkinter.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | str | None = None,
    border_width: int | str | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    scrollbar_fg_color: str | Tuple[str, str] | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    label_fg_color: str | Tuple[str, str] | None = None,
    label_text_color: str | Tuple[str, str] | None = None,
    label_text: str = "",
    label_font: tuple | CTkFont | None = None,
    label_anchor: str = "center",
    orientation: Literal['vertical', 'horizontal'] = "vertical"
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.

        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            label_font=kwargs.pop("font", theme.setfont_b),
            scrollbar_fg_color=kwargs.pop("scrollbar_fg_color", theme.back1),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.font_color1),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeComboBox1(customtkinter.CTkComboBox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: List[str] | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    variable: Variable | None = None,
    command: ((str) -> Any) | None = None,
    justify: str = "left",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            font=kwargs.pop("font", theme.setfont),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont),
            text_color=kwargs.pop("text_color", theme.font_color1),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color1),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back1),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            button_color=kwargs.pop("button_color", theme.back2),
            border_color=kwargs.pop("border_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeComboBoxBold1(customtkinter.CTkComboBox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: List[str] | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    variable: Variable | None = None,
    command: ((str) -> Any) | None = None,
    justify: str = "left",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            font=kwargs.pop("font", theme.setfont_b),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont_b),
            text_color=kwargs.pop("text_color", theme.font_color1),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color1),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back1),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            button_color=kwargs.pop("button_color", theme.back2),
            border_color=kwargs.pop("border_color", theme.highlight),
            *args,
            **kwargs
        )


class ThemeComboBox2(customtkinter.CTkComboBox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: List[str] | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    variable: Variable | None = None,
    command: ((str) -> Any) | None = None,
    justify: str = "left",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            font=kwargs.pop("font", theme.setfont),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont),
            text_color=kwargs.pop("text_color", theme.font_color1),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color2),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back2),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            button_color=kwargs.pop("button_color", theme.back1),
            border_color=kwargs.pop("border_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeComboBoxBold2(customtkinter.CTkComboBox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: List[str] | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    variable: Variable | None = None,
    command: ((str) -> Any) | None = None,
    justify: str = "left",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            font=kwargs.pop("font", theme.setfont_b),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont_b),
            text_color=kwargs.pop("text_color", theme.font_color1),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color2),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back2),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            button_color=kwargs.pop("button_color", theme.back1),
            border_color=kwargs.pop("border_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeButton1(customtkinter.CTkButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 2,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
    round_width_to_even_numbers: bool = True,
    round_height_to_even_numbers: bool = True,
    text: str = "CTkButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    image: CTkImage | Any | None = None,
    state: str = "normal",
    hover: bool = True,
    command: (() -> Any) | None = None,
    compound: str = "left",
    anchor: str = "center",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont),
            fg_color=kwargs.pop("fg_color", theme.back1),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )

class ThemeButtonBold1(customtkinter.CTkButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 2,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
    round_width_to_even_numbers: bool = True,
    round_height_to_even_numbers: bool = True,
    text: str = "CTkButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    image: CTkImage | Any | None = None,
    state: str = "normal",
    hover: bool = True,
    command: (() -> Any) | None = None,
    compound: str = "left",
    anchor: str = "center",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont_b),
            fg_color=kwargs.pop("fg_color", theme.back1),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )


class ThemeButton2(customtkinter.CTkButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 2,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
    round_width_to_even_numbers: bool = True,
    round_height_to_even_numbers: bool = True,
    text: str = "CTkButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    image: CTkImage | Any | None = None,
    state: str = "normal",
    hover: bool = True,
    command: (() -> Any) | None = None,
    compound: str = "left",
    anchor: str = "center",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont),
            fg_color=kwargs.pop("fg_color", theme.back2),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeButtonBold2(customtkinter.CTkButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 2,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
    round_width_to_even_numbers: bool = True,
    round_height_to_even_numbers: bool = True,
    text: str = "CTkButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    image: CTkImage | Any | None = None,
    state: str = "normal",
    hover: bool = True,
    command: (() -> Any) | None = None,
    compound: str = "left",
    anchor: str = "center",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont_b),
            fg_color=kwargs.pop("fg_color", theme.back2),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeSlider1(customtkinter.CTkSlider):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int | None = None,
    height: int | None = None,
    corner_radius: int | None = None,
    button_corner_radius: int | None = None,
    border_width: int | None = None,
    button_length: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] = "transparent",
    progress_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    from_: int = 0,
    to: int = 1,
    state: str = "normal",
    number_of_steps: int | None = None,
    hover: bool = True,
    command: ((float) -> Any) | None = None,
    variable: Variable | None = None,
    orientation: str = "horizontal",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            progress_color=kwargs.pop("progress_color", theme.back2),
            button_color=kwargs.pop("button_color", theme.font_color2),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeSlider2(customtkinter.CTkSlider):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int | None = None,
    height: int | None = None,
    corner_radius: int | None = None,
    button_corner_radius: int | None = None,
    border_width: int | None = None,
    button_length: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] = "transparent",
    progress_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    from_: int = 0,
    to: int = 1,
    state: str = "normal",
    number_of_steps: int | None = None,
    hover: bool = True,
    command: ((float) -> Any) | None = None,
    variable: Variable | None = None,
    orientation: str = "horizontal",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            progress_color=kwargs.pop("progress_color", theme.back1),
            button_color=kwargs.pop("button_color", theme.font_color1),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeCheckBox1(customtkinter.CTkCheckBox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 24,
    checkbox_width: int = 24,
    checkbox_height: int = 24,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    checkmark_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkCheckBox",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: (() -> Any) | None = None,
    onvalue: int | str = 1,
    offvalue: int | str = 0,
    variable: Variable | None = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            font=kwargs.pop("font", theme.setfont),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )

class ThemeCheckBox2(customtkinter.CTkCheckBox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 24,
    checkbox_width: int = 24,
    checkbox_height: int = 24,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    checkmark_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkCheckBox",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: (() -> Any) | None = None,
    onvalue: int | str = 1,
    offvalue: int | str = 0,
    variable: Variable | None = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            font=kwargs.pop("font", theme.setfont),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeInputDialog1(customtkinter.CTkInputDialog):
    def __init__(self, *args, **kwargs):
        """(method) def __init__(
    fg_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    button_fg_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    button_text_color: str | Tuple[str, str] | None = None,
    entry_fg_color: str | Tuple[str, str] | None = None,
    entry_border_color: str | Tuple[str, str] | None = None,
    entry_text_color: str | Tuple[str, str] | None = None,
    title: str = "CTkDialog",
    font: tuple | CTkFont | None = None,
    text: str = "CTkDialog"
) -> None
Construct a toplevel widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, menu, relief, screen, takefocus, use, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            fg_color=(kwargs.pop("fg_color", theme.back1)),
            text_color=(kwargs.pop("text_color", theme.font_color1)),
            font=kwargs.pop("font", theme.setfont),
            button_fg_color=(kwargs.pop("button_fg_color", theme.back2)),
            button_hover_color=(kwargs.pop("button_hover_color", theme.highlight)),
            button_text_color=(kwargs.pop("button_text_color", theme.font_color2)),
            *args,
            **kwargs
        )

class ThemeInputDialog2(customtkinter.CTkInputDialog):
    def __init__(self, *args, **kwargs):
        """(method) def __init__(
    fg_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    button_fg_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    button_text_color: str | Tuple[str, str] | None = None,
    entry_fg_color: str | Tuple[str, str] | None = None,
    entry_border_color: str | Tuple[str, str] | None = None,
    entry_text_color: str | Tuple[str, str] | None = None,
    title: str = "CTkDialog",
    font: tuple | CTkFont | None = None,
    text: str = "CTkDialog"
) -> None
Construct a toplevel widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, menu, relief, screen, takefocus, use, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            fg_color=(kwargs.pop("fg_color", theme.back2)),
            text_color=(kwargs.pop("text_color", theme.font_color2)),
            font=kwargs.pop("font", theme.setfont),
            button_fg_color=(kwargs.pop("button_fg_color", theme.back1)),
            button_hover_color=(kwargs.pop("button_hover_color", theme.highlight)),
            button_text_color=(kwargs.pop("button_text_color", theme.font_color1)),
            *args,
            **kwargs
        )

class ThemeOptionMenu1(customtkinter.CTkOptionMenu):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: list | None = None,
    variable: Variable | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((str) -> Any) | None = None,
    dynamic_resizing: bool = True,
    anchor: str = "w",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            button_color=kwargs.pop("button_color", theme.back2),
            font=kwargs.pop("font", theme.setfont),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color1),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back2),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color2),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeOptionMenuBold1(customtkinter.CTkOptionMenu):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: list | None = None,
    variable: Variable | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((str) -> Any) | None = None,
    dynamic_resizing: bool = True,
    anchor: str = "w",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            button_color=kwargs.pop("button_color", theme.back2),
            font=kwargs.pop("font", theme.setfont_b),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont_b),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color1),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back2),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color2),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeOptionMenu2(customtkinter.CTkOptionMenu):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: list | None = None,
    variable: Variable | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((str) -> Any) | None = None,
    dynamic_resizing: bool = True,
    anchor: str = "w",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            button_color=kwargs.pop("button_color", theme.back1),
            font=kwargs.pop("font", theme.setfont),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color2),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back1),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color1),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeOptionMenuBold2(customtkinter.CTkOptionMenu):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 140,
    height: int = 28,
    corner_radius: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    dropdown_fg_color: str | Tuple[str, str] | None = None,
    dropdown_hover_color: str | Tuple[str, str] | None = None,
    dropdown_text_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    dropdown_font: tuple | CTkFont | None = None,
    values: list | None = None,
    variable: Variable | None = None,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((str) -> Any) | None = None,
    dynamic_resizing: bool = True,
    anchor: str = "w",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            button_color=kwargs.pop("button_color", theme.back1),
            font=kwargs.pop("font", theme.setfont_b),
            dropdown_font=kwargs.pop("dropdown_font", theme.setfont_b),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color2),
            dropdown_fg_color=kwargs.pop("dropdown_fg_color", theme.back1),
            dropdown_text_color=kwargs.pop("dropdown_text_color", theme.font_color1),
            dropdown_hover_color=kwargs.pop("dropdown_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeRadioButton1(customtkinter.CTkRadioButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 22,
    radiobutton_width: int = 22,
    radiobutton_height: int = 22,
    corner_radius: int | None = None,
    border_width_unchecked: int | None = None,
    border_width_checked: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkRadioButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    variable: Variable | None = None,
    value: int | str = 0,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            font=kwargs.pop("font", theme.setfont),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )

class ThemeRadioButtonBold1(customtkinter.CTkRadioButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 22,
    radiobutton_width: int = 22,
    radiobutton_height: int = 22,
    corner_radius: int | None = None,
    border_width_unchecked: int | None = None,
    border_width_checked: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkRadioButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    variable: Variable | None = None,
    value: int | str = 0,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            font=kwargs.pop("font", theme.setfont_b),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )

class ThemeRadioButton2(customtkinter.CTkRadioButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 22,
    radiobutton_width: int = 22,
    radiobutton_height: int = 22,
    corner_radius: int | None = None,
    border_width_unchecked: int | None = None,
    border_width_checked: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkRadioButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    variable: Variable | None = None,
    value: int | str = 0,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            font=kwargs.pop("font", theme.setfont),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeRadioButtonBold2(customtkinter.CTkRadioButton):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 22,
    radiobutton_width: int = 22,
    radiobutton_height: int = 22,
    corner_radius: int | None = None,
    border_width_unchecked: int | None = None,
    border_width_checked: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    hover_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkRadioButton",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    variable: Variable | None = None,
    value: int | str = 0,
    state: str = tkinter.NORMAL,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            hover_color=kwargs.pop("hover_color", theme.highlight),
            font=kwargs.pop("font", theme.setfont_b),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeSwitch1(customtkinter.CTkSwitch):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 24,
    switch_width: int = 36,
    switch_height: int = 18,
    corner_radius: int | None = None,
    border_width: int | None = None,
    button_length: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] = "transparent",
    progress_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkSwitch",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    onvalue: int | str = 1,
    offvalue: int | str = 0,
    variable: Variable | None = None,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont),
            fg_color=kwargs.pop("fg_color", theme.back1),
            progress_color=kwargs.pop("progress_color", theme.back2),
            button_color=kwargs.pop("button_color", theme.font_color1),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )

class ThemeSwitchBold1(customtkinter.CTkSwitch):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 24,
    switch_width: int = 36,
    switch_height: int = 18,
    corner_radius: int | None = None,
    border_width: int | None = None,
    button_length: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] = "transparent",
    progress_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkSwitch",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    onvalue: int | str = 1,
    offvalue: int | str = 0,
    variable: Variable | None = None,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont_b),
            fg_color=kwargs.pop("fg_color", theme.back1),
            progress_color=kwargs.pop("progress_color", theme.back2),
            button_color=kwargs.pop("button_color", theme.font_color1),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color1),
            *args,
            **kwargs
        )

class ThemeSwitch2(customtkinter.CTkSwitch):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 24,
    switch_width: int = 36,
    switch_height: int = 18,
    corner_radius: int | None = None,
    border_width: int | None = None,
    button_length: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] = "transparent",
    progress_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkSwitch",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    onvalue: int | str = 1,
    offvalue: int | str = 0,
    variable: Variable | None = None,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont),
            fg_color=kwargs.pop("fg_color", theme.back2),
            progress_color=kwargs.pop("progress_color", theme.back1),
            button_color=kwargs.pop("button_color", theme.font_color2),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeSwitchBold2(customtkinter.CTkSwitch):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 100,
    height: int = 24,
    switch_width: int = 36,
    switch_height: int = 18,
    corner_radius: int | None = None,
    border_width: int | None = None,
    button_length: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] = "transparent",
    progress_color: str | Tuple[str, str] | None = None,
    button_color: str | Tuple[str, str] | None = None,
    button_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    text: str = "CTkSwitch",
    font: tuple | CTkFont | None = None,
    textvariable: Variable | None = None,
    onvalue: int | str = 1,
    offvalue: int | str = 0,
    variable: Variable | None = None,
    hover: bool = True,
    command: ((...) -> Any) | Any = None,
    state: str = tkinter.NORMAL,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            font=kwargs.pop("font", theme.setfont_b),
            fg_color=kwargs.pop("fg_color", theme.back2),
            progress_color=kwargs.pop("progress_color", theme.back1),
            button_color=kwargs.pop("button_color", theme.font_color2),
            button_hover_color=kwargs.pop("button_hover_color", theme.highlight),
            text_color=kwargs.pop("text_color", theme.font_color2),
            *args,
            **kwargs
        )

class ThemeTabview1(customtkinter.CTkTabview):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 300,
    height: int = 250,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    segmented_button_fg_color: str | Tuple[str, str] | None = None,
    segmented_button_selected_color: str | Tuple[str, str] | None = None,
    segmented_button_selected_hover_color: str | Tuple[str, str] | None = None,
    segmented_button_unselected_color: str | Tuple[str, str] | None = None,
    segmented_button_unselected_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    command: ((...) -> Any) | Any = None,
    anchor: str = "center",
    state: str = "normal",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            segmented_button_fg_color=kwargs.pop("segmented_button_fg_color", theme.back2),
            segmented_button_selected_color=kwargs.pop("segmented_button_selected_color", theme.font_color2),
            segmented_button_selected_hover_color=kwargs.pop("segmented_button_selected_hover_color", theme.highlight),
            segmented_button_unselected_color=kwargs.pop("segmented_button_unselected_color", theme.back1),
            segmented_button_unselected_hover_color=kwargs.pop("segmented_button_unselected_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeTabview2(customtkinter.CTkTabview):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 300,
    height: int = 250,
    corner_radius: int | None = None,
    border_width: int | None = None,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    segmented_button_fg_color: str | Tuple[str, str] | None = None,
    segmented_button_selected_color: str | Tuple[str, str] | None = None,
    segmented_button_selected_hover_color: str | Tuple[str, str] | None = None,
    segmented_button_unselected_color: str | Tuple[str, str] | None = None,
    segmented_button_unselected_hover_color: str | Tuple[str, str] | None = None,
    text_color: str | Tuple[str, str] | None = None,
    text_color_disabled: str | Tuple[str, str] | None = None,
    command: ((...) -> Any) | Any = None,
    anchor: str = "center",
    state: str = "normal",
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            segmented_button_fg_color=kwargs.pop("segmented_button_fg_color", theme.back1),
            segmented_button_selected_color=kwargs.pop("segmented_button_selected_color", theme.font_color1),
            segmented_button_selected_hover_color=kwargs.pop("segmented_button_selected_hover_color", theme.highlight),
            segmented_button_unselected_color=kwargs.pop("segmented_button_unselected_color", theme.back2),
            segmented_button_unselected_hover_color=kwargs.pop("segmented_button_unselected_hover_color", theme.highlight),
            *args,
            **kwargs
        )

class ThemeTextbox1(customtkinter.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 3,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    activate_scrollbars: bool = True,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            text_color=kwargs.pop("text_color", theme.font_color1),
            font=kwargs.pop("font", theme.setfont),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.back2),
            *args,
            **kwargs
        )

class ThemeTextboxBold1(customtkinter.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 3,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    activate_scrollbars: bool = True,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back1),
            text_color=kwargs.pop("text_color", theme.font_color1),
            font=kwargs.pop("font", theme.setfont_b),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.back2),
            *args,
            **kwargs
        )

class ThemeTextbox2(customtkinter.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 3,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    activate_scrollbars: bool = True,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            text_color=kwargs.pop("text_color", theme.font_color2),
            font=kwargs.pop("font", theme.setfont),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.back1),
            *args,
            **kwargs
        )

class ThemeTextboxBold2(customtkinter.CTkTextbox):
    def __init__(self, master, *args, **kwargs):
        """(method) def __init__(
    master: Any,
    width: int = 200,
    height: int = 200,
    corner_radius: int | None = None,
    border_width: int | None = None,
    border_spacing: int = 3,
    bg_color: str | Tuple[str, str] = "transparent",
    fg_color: str | Tuple[str, str] | None = None,
    border_color: str | Tuple[str, str] | None = None,
    text_color: str | None = None,
    scrollbar_button_color: str | Tuple[str, str] | None = None,
    scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
    font: tuple | CTkFont | None = None,
    activate_scrollbars: bool = True,
    **kwargs: Any
) -> None
Construct a frame widget with the parent MASTER.

Valid resource names: background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, relief, takefocus, visual, width.
        """
        theme = ThemeManager()
        super().__init__(
            master,
            fg_color=kwargs.pop("fg_color", theme.back2),
            text_color=kwargs.pop("text_color", theme.font_color2),
            font=kwargs.pop("font", theme.setfont_b),
            scrollbar_button_hover_color=kwargs.pop("scrollbar_button_hover_color", theme.highlight),
            scrollbar_button_color=kwargs.pop("scrollbar_button_color", theme.back1),
            *args,
            **kwargs
        )

