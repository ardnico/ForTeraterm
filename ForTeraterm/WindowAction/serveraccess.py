
import os
import tkinter
import customtkinter
from glob import glob
from ..Language.apptext import AppText
from ..WindowSettings.theme import theme
from ..WindowSettings.conf import appconf
from ..WindowSettings.image import imginst
from ..ServerData.serverfilemanage import ServerFileManage

class ServerAccess(customtkinter.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs):
        self.trans = AppText(appconf.get_data("lang"))
        
        self.width = appconf.get_data("width")
        self.height = appconf.get_data("height")
        self.font = appconf.get_data("font")
        self.macro_path = appconf.get_data("macro_path")
        self.font = customtkinter.CTkFont(size=12,family=self.font)
        self.font_b = customtkinter.CTkFont(size=15, weight="bold",family=self.font)
        
        super().__init__(master,
            width                           = self.width
            ,height                         = self.height
            ,corner_radius                  = 0                            
            ,fg_color                       = theme.back1
            )
        
        self.grid(row=0, column=0, sticky="nw")
        self.call_serveraccess_frame()
    
    def call_serveraccess_frame(self):
        sfm = ServerFileManage()
        bar_width = 20
        padx = 5
        pady = 5
        row_i = 0
        label = self.trans.translate("ServerAccess")
        
        self.title_label = customtkinter.CTkLabel(self
            ,text=label
            ,width = self.width-10
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
        # select menu
        
        icon_frame_row_cell = 35
        
        row_i += 1
        
        self.check_var_macro = tkinter.StringVar(self.item_icons_frame, 'off')
        self.checkbox_macro = customtkinter.CTkCheckBox(self.item_icons_frame
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
            ,font = self.font
            ,values=files
        )
        self.macro_combobox.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        self.macro_combobox.place(x=self.width/2,y=icon_frame_row_cell,anchor=customtkinter.CENTER)
        self.macro_combobox.set("")
        
        row_i += 1
        
        self.server_launch = customtkinter.CTkButton(self.item_icons_frame
            ,fg_color=theme.back1
            ,text=self.trans.translate("BatchServerAccess")
            ,font = self.font
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
        self.check_vars = []
        self.checkboxes = []
        self.serverlabels = []
        self.serveraccess_buttons = []
        self.detail_buttons = []
        for i,s in enumerate(sfm.get_serverdatas()):
            self.check_vars.append(tkinter.StringVar(self.Scroll_frame, 'off'))
            self.checkboxes.append(customtkinter.CTkCheckBox(self.Scroll_frame
                ,variable=self.check_vars[i]
                ,onvalue=s.primaryno
                ,offvalue=None
                ,text=''
                ,hover_color=theme.high_light
                ,width=30
            ))
            self.checkboxes[i].grid(row=row_i, column=0,padx=padx, pady=pady)
            self.serverlabels.append(customtkinter.CTkLabel(self.Scroll_frame
                ,width=self.width - padx * 2 - bar_width - padx * 8 - 340
                ,text=s.hostname
                ,anchor='w'
                ,font = self.font
                ,text_color=theme.font_color1
            ))
            self.serverlabels[i].grid(row=row_i, column=1, padx=padx, pady=pady,columnspan=2,sticky='w')
            self.serveraccess_buttons.append(customtkinter.CTkButton(self.Scroll_frame
                ,image=imginst.image_server
                ,width=250
                ,fg_color=theme.back1
                ,hover_color=theme.high_light
                ,text=self.trans.translate("ServerAccess")
            ))
            self.serveraccess_buttons[i].grid(row=row_i, column=3, padx=padx, pady=pady)
            self.detail_buttons.append( customtkinter.CTkButton(self.Scroll_frame
                ,width=60
                ,image=imginst.image_detail
                ,fg_color=theme.back1
                ,hover_color=theme.high_light
                ,text=""
            ))
            self.detail_buttons[i].grid(row=row_i, column=4, padx=padx, pady=pady)
            self.detail_buttons[i].configure(command=lambda s=s: self.show_detail(s.primaryno))
            row_i += 1
        
        row_i += 1
        self.item_icons_frame = customtkinter.CTkLabel(self
            , width             = self.width
            , fg_color          = theme.back1
            ,text=self.trans.translate("DetailedInfo")
            ,anchor="center"
            ,corner_radius=0
        )
        self.item_icons_frame.grid(row=row_i, column=0, padx=0, pady=0,sticky='ew',columnspan=2)
        
        row_i += 1
        self.detail_label = customtkinter.CTkTextbox(self
            ,width                           = self.width - padx * 2 - bar_width
            ,height                         = self.height / 3
            ,corner_radius                  = 0
            )
        self.detail_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
    
    def launch_servers(self):
        sfm = ServerFileManage()
        for i,s in enumerate(sfm.get_serverdatas()):
            tmp_flag = "off"
            tmp_flag = self.check_vars[i].get()
            if tmp_flag != "off":
                print(f"launch server {s.hostname}")
    
    def show_detail(self,i):
        if i is None:
            return
        sfm = ServerFileManage()
        server_info = sfm.get_serverdata(i)
        info_text = ""
        for key in server_info.__dict__.items():
            info_text += key[0] + ":    "
            if key[0]:
                if key[0] in ["psw","psw2"]:
                    info_text += "*" *len(str(key[1])) + "\n"
                else:
                    info_text += str(key[1]) + "\n"
        self.detail_label.delete("0.0","end")
        self.detail_label.insert("0.0",info_text)
    