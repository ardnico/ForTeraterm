
import os
import customtkinter
from .CTkMenuBar import *
from .util import messsagebox
from tkinter import filedialog
from .WindowAction.serveraccess import ServerAccess
from .WindowAction.editmacro import EditMacro
from .WindowAction.serverregist import ServerRegist
from .WindowSettings.edit import Edit
from .WindowSettings.theme import *
from .WindowSettings.conf import appconf
from .Language.apptext import AppText

class Mainmenu(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apptxt = AppText(appconf.get_data("lang"))
        self.call_mein_menu()
    
    @appconf.log_exception
    def call_mein_menu(self):
        width = appconf.get_data("width")
        height = appconf.get_data("height")
        self.geometry(f"{width}x{height}")
        self.title(self.apptxt.translate("TeratermAccessTool"))
        theme = ThemeManager()
        customtkinter.set_appearance_mode(theme.mode)
        font = theme.setfont
        
        menu = CTkMenuBar(self)
        self.button_1 = menu.add_cascade(self.apptxt.translate("Action"))
        self.button_2 = menu.add_cascade(self.apptxt.translate("Settings"))
        self.button_3 = menu.add_cascade(self.apptxt.translate("About"))
        
        self.dropdown1 = CustomDropdownMenu(
            widget          = self.button_1,
            border_color    = theme.back2,
            font            = font,
            bg_color        = "transparent",
            hover_color     = [theme.back1, theme.highlight],
            # fg_color        = [theme.back2,theme.back1],
            # text_color      = [ theme.font_color2 , theme.font_color1],
            )
        self.dropdown1.add_option(option=self.apptxt.translate("ServerAccess"),command=self.action_serveraccess)
        self.dropdown1.add_option(option=self.apptxt.translate("EditMacro"),command=self.action_editmacro)
        self.dropdown1.add_option(option=self.apptxt.translate("ServerRegist"),command=self.action_serverregist)
        
        self.dropdown2 = CustomDropdownMenu(
            widget=self.button_2,
            border_color    = theme.back2,
            font            = font,
            bg_color        = "transparent",
            hover_color     = [theme.back1, theme.highlight],
            # fg_color        = [theme.back2,theme.back1],
            # text_color      = [ theme.font_color2 , theme.font_color1],
            )
        self.dropdown2.add_option(option=self.apptxt.translate("Edit"),command=self.settings_edit)
        # self.dropdown2.add_option(option=self.apptxt.translate("Restart"),command=self.restart)
        
        self.dropdown3 = CustomDropdownMenu(
            widget=self.button_3,
            border_color    = theme.back2,
            font            = font,
            bg_color        = "transparent",
            hover_color     = [theme.back1, theme.highlight],
            # fg_color        = [theme.back2,theme.back1],
            # text_color      = [ theme.font_color2 , theme.font_color1],
            )
        self.dropdown3.add_option(option=self.apptxt.translate("Readme"),command=self.about_readme)
        self.dropdown3.add_option(option=self.apptxt.translate("Version"),command=self.about_version)
        # self.dropdown3.add_option(option=self.apptxt.translate("Restart"),command=self.restart)
        if appconf.get_data("dev_mode") == 1:
            self.dropdown3.add_option(option=self.apptxt.translate("Test"),command=self.test)
        
        self.menuframe = ThemeFrame1(
            master=self,
            fg_color = theme.back1,
            width = appconf.get_data("width"),
            height = appconf.get_data("height"),
            )
        self.menuframe.pack(fill="both")
        
        self.serveraccess = ServerAccess(self.menuframe)
        self.sub_frames = []
        self.mainloop()
    
    @appconf.log_exception
    def action_serveraccess(self):
        self.reset_frame()
        self.serveraccess = ServerAccess(self.menuframe)
        self.sub_frames.append(self.serveraccess)

    @appconf.log_exception
    def action_editmacro(self):
        self.reset_frame()
        self.editmacro = EditMacro(self.menuframe)
        
        self.sub_frames.append(self.editmacro)

    @appconf.log_exception
    def action_serverregist(self):
        self.reset_frame()
        self.serverregist = ServerRegist(self.menuframe)
        self.sub_frames.append(self.serverregist)

    @appconf.log_exception
    def settings_edit(self):
        self.reset_frame()
        self.edit = Edit(self.menuframe)
        self.sub_frames.append(self.edit)

    def reset_frame(self):
        for frame in self.sub_frames:
            frame.grid_forget()
        
    @appconf.log_exception
    def about_readme(self):
        file_path = os.path.join(os.getcwd(),"readme.pdf")
        import webbrowser
        webbrowser.open(file_path)
    
    @appconf.log_exception
    def about_version(self):
        version_txt = f"""
AppName:    {appconf.__name__}
Version:    {appconf.__version__}
License:    {appconf.__license__}
"""
        messsagebox.show_info(title="Version Information",message=version_txt)
    
    @appconf.log_exception
    def restart(self):
        self.destroy()
        return
        
    @appconf.log_exception
    def test(self):
        self.destroy()
        self.__init__()
    
    @staticmethod
    def open_file_dialog(filetypes,initialdir):
        # Open a file dialog and get the selected file path
        # [('data files','*.csv;*.txt')]
        file_path = filedialog.askopenfilename(filetypes=filetypes,initialdir=initialdir)
        if file_path:
            return file_path
    
    def restart(self):
        self.destroy()
        Mainmenu()