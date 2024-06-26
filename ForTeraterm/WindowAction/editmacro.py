
import os
import customtkinter
from glob import glob
from ..WindowSettings.theme import *
from ..WindowSettings.conf import appconf
from ..WindowSettings.image import imginst
from ..Language.apptext import AppText
from ..ServerData.serverfilemanage import ServerFileManage

class EditMacro(ThemeFrame1):
    def __init__(
        self,
        master,
        **kwargs):
        self.trans = AppText(appconf.get_data("lang"))
        self.sfm = ServerFileManage()
        self.width = appconf.get_data("width")
        self.height = appconf.get_data("height")
        self.macro_path = appconf.get_data("macro_path")
        os.makedirs(self.macro_path,exist_ok=True)
        
        super().__init__(master,
            width                           = self.width
            ,height                         = self.height
            ,corner_radius                  = 0             
            )
        
        self.grid(row=0, column=0, sticky="nw")
        self.call_editmacro_frame()
    
    def call_editmacro_frame(self):
        bar_width = 20
        padx = 5
        pady = 5
        cell = self.width / 3 - padx * 2 -bar_width
        row_i = 0
        label = self.trans.translate("EditMacro")
        
        self.title_label = ThemeLabelBold2(self
            ,text=label
            ,width = self.width - 10
            ,height = 25
            ,bg_color = "transparent"
            ,image = imginst.image_server
            ,wraplength = 0
            )
        self.title_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i += 1
        
        self.item_icons_frame = ThemeFrame2(self
            , width             = self.width
            , height            = 70
            ,corner_radius=0
        )
        
        self.item_icons_frame.grid(row=row_i, column=0, padx=0, pady=pady*2,sticky='ew',columnspan=3)
        
        ###############################################################################################
        # select menu
        
        icon_frame_row_cell = 35
        
        row_i += 1
        
        self.macroname_label = ThemeLabel1(self.item_icons_frame
            ,width=cell
            ,text=self.trans.translate("MacroName")
        )
        self.macroname_label.grid(row=row_i, column=0,padx=padx, pady=pady,sticky='ew')
        
        self.macroname_entry = ThemeEntry1(self.item_icons_frame
            ,width=cell
        )
        self.macroname_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        self.macroname_button = ThemeButton2(self.item_icons_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Register")
            ,image = imginst.image_add_file
            ,command=self.regist_macro
        )
        self.macroname_button.grid(row=row_i, column=2,padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        self.edit_macroname_label = ThemeLabel1(self.item_icons_frame
            ,width=cell
            ,text=self.trans.translate("MacroName")
        )
        self.edit_macroname_label.grid(row=row_i, column=0,padx=padx, pady=pady,sticky='ew')
        
        macro_files = glob(os.path.join(self.macro_path,"*.ttl"))
        macro_files = [os.path.basename(f) for f in macro_files]
        self.edit_macroname_combobox = ThemeComboBox2(self.item_icons_frame
            ,width=cell
            ,corner_radius=1
            ,values=macro_files
            ,command=self.set_edit_macroname_combobox
        )
        self.edit_macroname_combobox.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        self.edit_macroname_combobox.set("")
        self.edit_macroname_button = ThemeButton2(self.item_icons_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Save")
            ,image = imginst.image_add_file
            ,command=self.edit_macro
        )
        self.edit_macroname_button.grid(row=row_i, column=2,padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        self.del_macroname_label = ThemeLabel1(self.item_icons_frame
            ,width=cell
            ,text=self.trans.translate("MacroName")
        )
        self.del_macroname_label.grid(row=row_i, column=0,padx=padx, pady=pady,sticky='ew')
        
        macro_files = glob(os.path.join(self.macro_path,"*.ttl"))
        macro_files = [os.path.basename(f) for f in macro_files]
        self.del_macroname_comcocox = ThemeComboBox2(self.item_icons_frame
            ,width=cell
            ,corner_radius=1
            ,values=macro_files
            ,command=self.set_del_macroname_combobox
        )
        self.del_macroname_comcocox.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        self.del_macroname_comcocox.set("")
        self.del_macroname_button = ThemeButton2(self.item_icons_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Delete")
            ,image = imginst.image_add_file
            ,command=self.del_macroname_combobox
        )
        self.del_macroname_button.grid(row=row_i, column=2,padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        ###############################################################################################
        
        self.Scroll_frame = ThemeScrollableFrame2(self
            ,width                           = self.width - padx * 2 - bar_width
            ,height                         = self.height * 2  / 3
            ,corner_radius                  = 0  
            )
        self.Scroll_frame.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
        
        self.edit_textbox = ThemeTextbox1(self.Scroll_frame
            ,width                           = self.width - padx * 2 - bar_width
            ,height                         = self.height * 3 
            ,corner_radius                  = 0    
            )
        self.edit_textbox.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        self.edit_textbox.insert("0.0",self.trans.translate("CreateTTLFile") )
        row_i += 1
    
    def regist_macro(self):
        tmp_title = self.macroname_entry.get()
        if tmp_title == "":
            tmp_title = None
        if tmp_title:
            content = self.edit_textbox.get("0.0","end").rstrip("\n")
            self.sfm.mk_ttl(tmp_title,content)
            self.reset_combobox()
    
    def edit_macro(self):
        tmp_val = self.edit_macroname_combobox.get()
        if tmp_val == "":
            tmp_val = None
        if tmp_val:
            file_path = os.path.join(self.macro_path,tmp_val)
            content = self.edit_textbox.get("0.0","end")
            with open(file_path,"w",encoding="utf-8") as f:
                f.write(content)
            self.reset_combobox()
    
    def set_edit_macroname_combobox(self,tmp_val):
        self.macroname_entry.delete(0,"end")
        self.del_macroname_comcocox.set("")
        file_path = os.path.join(self.macro_path,tmp_val)
        with open(file_path,"r",encoding="utf-8") as f:
            txt = f.read()
        self.edit_textbox.delete("0.0","end")
        self.edit_textbox.insert("0.0",txt)
    
    def set_del_macroname_combobox(self,tmp_val):
        self.macroname_entry.delete(0,"end")
        self.edit_macroname_combobox.set("")
        file_path = os.path.join(self.macro_path,tmp_val)
        with open(file_path,"r",encoding="utf-8") as f:
            txt = f.read()
        self.edit_textbox.delete("0.0","end")
        self.edit_textbox.insert("0.0",txt)
    
    def del_macroname_combobox(self):
        tmp_val = self.del_macroname_comcocox.get()
        file_path = os.path.join(self.macro_path,tmp_val)
        os.remove(file_path)
        self.reset_combobox()
        
    def reset_combobox(self):
        macro_files = glob(os.path.join(self.macro_path,"*.ttl"))
        macro_files = [os.path.basename(f) for f in macro_files]
        self.edit_macroname_combobox.configure(values=macro_files)
        self.del_macroname_comcocox.configure(values=macro_files)
        self.edit_macroname_combobox.set("")
        self.del_macroname_comcocox.set("")
        self.macroname_entry.delete(0,"end")
        self.edit_textbox.delete("0.0","end")
        self.edit_textbox.insert("0.0",self.trans.translate("CreateTTLFile"))
    