
import os
import tkinter as tk
import customtkinter
import pyautogui
from tkinter import filedialog
from pathlib import Path
from glob import glob
from ..Language.apptext import AppText
from ..WindowSettings.theme import *
from ..WindowSettings.conf import appconf
from ..WindowSettings.image import imginst
from ..ServerData.serverfilemanage import ServerFileManage

class ServerRegist(ThemeFrame1):
    def __init__(
        self,
        master,
        **kwargs):
        self.trans = AppText(appconf.get_data("lang"))
        self.sfm = ServerFileManage()
        label_text = ""
        border_width = 20
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
        self.call_serverregist_frame()
    
    def call_serverregist_frame(self):
        bar_width = 20
        padx = 5
        pady = 5
        cell = self.width  / 3 - padx * 6
        row_i_p = 0
        label = self.trans.translate("ServerRegist")
        
        self.title_label = ThemeLabelBold2(self
            ,text=label
            ,width = self.width - 10
            ,height = 25
            ,corner_radius = 10
            ,bg_color = "transparent"
            ,image = imginst.image_server
            ,compound = "left"
            ,anchor = "center"
            ,wraplength = 0
            )
        self.title_label.grid(row=row_i_p, column=0, padx=padx, pady=pady,sticky='ew',columnspan=3)
        
        row_i_p += 1
        
        self.item_icons_frame = ThemeFrame2(self
            , width             = self.width
            ,corner_radius      = 0
        )
        
        self.item_icons_frame.grid(row=row_i_p, column=0, padx=0, pady=pady,sticky='ew',columnspan=3)
        
        ###############################################################################################
        # select menu
        
        icon_frame_row_cell = 35
        
        row_i_p += 1
        
        self.cell_keep = ThemeLabel1(self.item_icons_frame
            ,width=15
            ,text=""
        )
        self.cell_keep.grid(row=row_i_p, column=4,padx=padx, pady=pady,sticky='w')
        self.serverregist_label = ThemeLabel1(self.item_icons_frame
            ,width=cell
            ,text=self.trans.translate("Hostname")
        )
        self.serverregist_label.grid(row=row_i_p, column=0,padx=padx, pady=pady,sticky='ew')
        self.serverregist_entry = ThemeEntry1(self.item_icons_frame
            ,width=cell
        )
        self.serverregist_entry.grid(row=row_i_p, column=1,padx=padx, pady=pady,sticky='ew')
        self.serverregist_button = ThemeButton2(self.item_icons_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Register")
            ,image = imginst.image_add_file
            ,command=self.regist_server
        )
        self.serverregist_button.grid(row=row_i_p, column=2,padx=padx, pady=pady,sticky='ew')
        
        row_i_p += 1
        
        self.edit_serverregist_label = ThemeLabel1(self.item_icons_frame
            ,width=cell
            ,text=self.trans.translate("Hostname")
        )
        self.edit_serverregist_label.grid(row=row_i_p, column=0,padx=padx, pady=pady,sticky='ew')
        
        server_settings = self.sfm.get_serverdatas()
        server_settings = [str(s.primaryno)+"_"+self.none_chk(s.hostname)+"_"+self.none_chk(s.hostname2) for s in server_settings]
        self.edit_serverregist_optionmenu = ThemeOptionMenu2(self.item_icons_frame
            ,width=cell
            ,corner_radius=1
            ,values=server_settings
            ,command=self.set_edit_serverregist_optionmenu
        )
        self.edit_serverregist_optionmenu.grid(row=row_i_p, column=1,padx=padx, pady=pady,sticky='ew')
        self.edit_serverregist_optionmenu.set("")
        self.edit_serverregist_button = ThemeButton2(self.item_icons_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Save")
            ,image = imginst.image_add_file
            ,command=self.edit_server
        )
        self.edit_serverregist_button.grid(row=row_i_p, column=2,padx=padx, pady=pady,sticky='ew')
        
        row_i_p += 1
        
        self.del_serverregist_label = ThemeLabel1(self.item_icons_frame
            ,width=cell
            ,text=self.trans.translate("Hostname")
        )
        self.del_serverregist_label.grid(row=row_i_p, column=0,padx=padx, pady=pady,sticky='ew')
        
        self.del_serverregist_optionmenu = ThemeOptionMenu2(self.item_icons_frame
            ,width=cell
            ,corner_radius=1
            ,values=server_settings
            ,command=self.set_del_serverregist_optionmenu
        )
        self.del_serverregist_optionmenu.grid(row=row_i_p, column=1,padx=padx, pady=pady,sticky='ew')
        self.del_serverregist_optionmenu.set("")
        self.del_serverregist_button = ThemeButton2(self.item_icons_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Delete")
            ,image = imginst.image_add_file
            ,command=self.del_serverregist_optionmenu
        )
        self.del_serverregist_button.grid(row=row_i_p, column=2,padx=padx, pady=pady,sticky='ew')
        
        row_i_p += 1
        
        ###############################################################################################
        
        
        self.Scroll_frame = ThemeScrollableFrame1(self
            ,width                           = self.width - padx * 2 - bar_width 
            ,height                         = self.height * 6 /  8
            ,corner_radius                  = 0             
            )
        self.Scroll_frame.grid(row=row_i_p, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        col_max = 4
        dcrlcell = self.width / (col_max + 1)
        
        row_i = 0
        
        ##### data
        
        # sdata.telnet
        
        row_i += 1
        
        
        self.scroll_span = ThemeLabel1(master=self.Scroll_frame
            ,text=""
            ,width=bar_width
        )
        self.scroll_span.grid(row=row_i, column=4, padx=padx, pady=pady,sticky='ew')
        
        
        self.username_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("Username")
            ,width=dcrlcell
        )
        self.username_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.username_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.username_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        
        
        self.telnet_switch_label = ThemeLabel2(master=self.Scroll_frame
            ,corner_radius=10
            ,text="Telnet/SSH"
            ,width=dcrlcell
        )
        self.telnet_switch_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.telnet_optionmenu = ThemeOptionMenu1(master=self.Scroll_frame
            ,values=[
                "telnet"
                ,"ssh"
                ,"ssh1"
                ,"ssh2"
                ,"com1"
                ,"com2"
                ,"com3"
                ,"com4"
                ,"com5"
            ]
        )
        self.telnet_optionmenu.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        self.telnet_optionmenu.set("ssh")
        
        row_i += 1
        
        self.passwd_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("Password")
            ,width=dcrlcell
        )
        self.passwd_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.passwd_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.passwd_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        
        
        self.consolesymbol_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("LineStartCharacter")
            ,width=dcrlcell
        )
        self.consolesymbol_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.consolesymbol_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.consolesymbol_entry.grid(row=row_i, column=3,padx=padx, pady=pady,sticky='ew')
        self.consolesymbol_entry.insert(0,"$")
        
        
        row_i += 1
        
        self.usernameinput_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("LoginWaitString")
            ,width=dcrlcell
        )
        self.usernameinput_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.usernameinput_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.usernameinput_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        self.usernameinput_entry.insert(0,"login:")
        
        self.pswinput_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("PasswordWaitString")
            ,width=dcrlcell
        )
        self.pswinput_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.pswinput_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.pswinput_entry.grid(row=row_i, column=3,padx=padx, pady=pady,sticky='ew')
        self.pswinput_entry.insert(0,"Password:")
        
        row_i += 1
        
        self.hostname2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("SecondServer")
            ,width=dcrlcell
        )
        self.hostname2_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=4)
        
        row_i += 1
        
        self.hostname2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("Hostname")
            ,width=dcrlcell
        )
        self.hostname2_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.hostname2_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.hostname2_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        self.username2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("Username")
            ,width=dcrlcell
        )
        self.username2_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.username2_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.username2_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        
        
        self.telnet2_label = ThemeLabel2(master=self.Scroll_frame
            ,corner_radius=10
            ,text="Telnet/SSH"
            ,width=dcrlcell
        )
        self.telnet2_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.telnet2_optionmenu = ThemeOptionMenu1(master=self.Scroll_frame
            ,values=[
                "telnet"
                ,"ssh"
            ]
        )
        self.telnet2_optionmenu.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        self.telnet2_optionmenu.set("ssh")
        
        row_i += 1
        
        self.passwd2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("Password")
            ,width=dcrlcell
        )
        self.passwd2_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.passwd2_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.passwd2_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        
        
        self.consolesymbol2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("LineStartCharacter")
            ,width=dcrlcell
        )
        self.consolesymbol2_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.consolesymbol2_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.consolesymbol2_entry.grid(row=row_i, column=3,padx=padx, pady=pady,sticky='ew')
        self.consolesymbol2_entry.insert(0,"$")
        
        row_i += 1
        
        self.usernameinput2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("LoginWaitString")
            ,width=dcrlcell
        )
        self.usernameinput2_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.usernameinput2_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.usernameinput2_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        self.usernameinput2_entry.insert(0,"login:")
        
        self.pswinput2_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("PasswordWaitString")
            ,width=dcrlcell
        )
        self.pswinput2_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.pswinput2_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.pswinput2_entry.grid(row=row_i, column=3,padx=padx, pady=pady,sticky='ew')
        self.pswinput2_entry.insert(0,"Password:")
        
        row_i += 1
        
        # kanjicoder          : str   = None
        self.kanjicoder_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("KanjiCodeReceive")
            ,width=dcrlcell
        )
        self.kanjicoder_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.kanjicoder_optionmenu = ThemeOptionMenu1(master=self.Scroll_frame
            ,values=[
                "UTF8",
                "UTF8m",
                "SJIS",
                "EUC",
                "JIS",
                "KS5601",
            ]
        )
        self.kanjicoder_optionmenu.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew')
        self.kanjicoder_optionmenu.set("UTF8")
        
        # kanjicodet          : str   = None
        self.kanjicodet_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("KanjiCodeSend")
            ,width=dcrlcell
        )
        self.kanjicodet_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.kanjicodet_optionmenu = ThemeOptionMenu1(master=self.Scroll_frame
            ,values=[
                "UTF8",
                "SJIS",
                "EUC",
                "JIS",
                "KS5601",
            ]
        )
        self.kanjicodet_optionmenu.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        self.kanjicodet_optionmenu.set("UTF8")
        
        row_i += 1
        
        self.windowtitle_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("WindowTitleName")
            ,width=dcrlcell
        )
        self.windowtitle_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.windowtitle_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.windowtitle_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew')
        
        
        self.windowhidden_switch_val = tk.StringVar(value="off")
        self.windowhidden_switch = ThemeSwitch1(self.Scroll_frame
            ,width=dcrlcell
            ,variable=self.windowhidden_switch_val
            ,onvalue="on"
            ,offvalue="off"
            ,text=self.trans.translate("WindowShowHide")
            ,command=self.windowhidden_switch_event
        )
        self.windowhidden_switch.grid(row=row_i, column=2,padx=padx, pady=pady,sticky='ew')
        
        self.windowhidden_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("Show")
        )
        self.windowhidden_label.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        
        self.windowx_title_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("PositionX")
        )
        self.windowx_title_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        
        self.windowy_title_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("PositionY")
        )
        self.windowy_title_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
        
        scr_w,scr_h= pyautogui.size()
        self.sliderval_windowx = tk.IntVar(value=200)
        self.slider_windowx = ThemeSlider2(self.Scroll_frame
            ,from_=0
            ,to=scr_w
            ,number_of_steps=scr_w
            ,width = dcrlcell
            ,command=self.set_windowx
            ,variable=self.sliderval_windowx
        )
        self.slider_windowx.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.windowx_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=200
        )
        self.windowx_label.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew')
        
        
        self.sliderval_windowy = tk.IntVar(value=200)
        self.slider_windowy = ThemeSlider2(self.Scroll_frame
            ,from_=0
            ,to=scr_h
            ,number_of_steps=scr_h
            ,width = dcrlcell
            ,command=self.set_windowy
            ,variable=self.sliderval_windowy
        )
        self.slider_windowy.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.windowy_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=200
        )
        self.windowy_label.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        
        
        row_i += 1
        
        
        self.cdelayperchar_title_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("SendDelayPerCharacter")
        )
        self.cdelayperchar_title_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        
        self.cdelayperline_title_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("SendDelayPerLine")
        )
        self.cdelayperline_title_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
        
        self.sliderval_cdelayperchar = tk.IntVar(value=5)
        self.slider_cdelayperchar = ThemeSlider2(self.Scroll_frame
            ,from_=0
            ,to=60
            ,number_of_steps=60
            ,width = dcrlcell
            ,command=self.set_cdelayperchar
            ,variable=self.sliderval_cdelayperchar
        )
        self.slider_cdelayperchar.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.cdelayperchar_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=5
        )
        self.cdelayperchar_label.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew')
        
        
        self.sliderval_cdelayperline = tk.IntVar(value=1)
        self.slider_cdelayperline = ThemeSlider2(self.Scroll_frame
            ,from_=0
            ,to=60
            ,number_of_steps=60
            ,width = dcrlcell
            ,command=self.set_cdelayperline
            ,variable=self.sliderval_cdelayperline
        )
        self.slider_cdelayperline.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.cdelayperline_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=1
        )
        self.cdelayperline_label.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        
        self.windowx_title_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("LanguageSelection")
        )
        self.windowx_title_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        
        self.cdelayperline_title_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("Timeout")
        )
        self.cdelayperline_title_label.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew',columnspan=2)
        
        row_i += 1
        
        
        language_dic = {
            "U" :self.trans.translate("U")
            ,"E" :self.trans.translate("E")
            ,"J" :self.trans.translate("J")
            ,"K" :self.trans.translate("K")
            ,"R" :self.trans.translate("R")
        }
        
        self.language_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=language_dic["U"]
        )
        
        self.language_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        self.language_optionmenu = ThemeOptionMenu1(master=self.Scroll_frame
            ,values=[
                "U","E","J","K","R"
            ]
            ,command=self.set_language_optionmenu
        )
        self.language_optionmenu.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew')
        self.language_optionmenu.set("U")
        
        self.sliderval_timeout = tk.IntVar(value=15)
        self.slider_timeout = ThemeSlider2(self.Scroll_frame
            ,from_=0
            ,to=60
            ,number_of_steps=60
            ,width = dcrlcell
            ,command=self.set_timeout
            ,variable=self.sliderval_timeout
        )
        self.slider_timeout.grid(row=row_i, column=2, padx=padx, pady=pady,sticky='ew')
        
        self.timeout_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=15
        )
        self.timeout_label.grid(row=row_i, column=3, padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
        
        self.autowinclose_switch_val = customtkinter.StringVar(value="off")
        self.autowinclose_switch = ThemeSwitch1(self.Scroll_frame
            ,width=dcrlcell
            ,variable=self.autowinclose_switch_val
            ,onvalue="on"
            ,offvalue="off"
            ,text=self.trans.translate("AutoWindowClose")
            ,command=self.autowinclose_switch_event
        )
        self.autowinclose_switch.grid(row=row_i, column=0,padx=padx, pady=pady,sticky='ew')
        
        self.autowinclose_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,width=dcrlcell
            ,text=self.trans.translate("DoNotClose")
        )
        self.autowinclose_label.grid(row=row_i, column=1, padx=padx, pady=pady,sticky='ew')
        
        
        row_i += 1
        
        
        self.optionsline_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("OtherOptions")
            ,width=dcrlcell
            ,anchor="center"
        )
        self.optionsline_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew',columnspan=4)
        
        row_i += 1
        
        self.optionsline_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.optionsline_entry.grid(row=row_i, column=0,padx=padx, pady=pady,sticky='ew',columnspan=4)
        
        
        row_i += 1
        
        self.filetransdir_label = ThemeLabel1(master=self.Scroll_frame
            ,corner_radius=1
            ,text=self.trans.translate("FileTransferFolder")
            ,width=dcrlcell
        )
        self.filetransdir_label.grid(row=row_i, column=0, padx=padx, pady=pady,sticky='ew')
        
        
        self.filetransdir_entry = ThemeEntry1(self.Scroll_frame
            ,width=dcrlcell
        )
        self.filetransdir_entry.grid(row=row_i, column=1,padx=padx, pady=pady,sticky='ew',columnspan=2)
        self.filetransdir_entry.delete(0,"end")
        self.filetransdir_entry.insert(0,os.path.join(Path.home(), 'Documents'))
        self.filetransdir_button = ThemeButton2(self.Scroll_frame
            ,width=cell
            ,corner_radius = 1
            ,text = self.trans.translate("Open")
            ,image = imginst.image_add_file
            ,command=self.open_filetransdir
        )
        self.filetransdir_button.grid(row=row_i, column=3,padx=padx, pady=pady,sticky='ew')
        
        row_i += 1
        
    def get_value_from_ctk(self,inputobj,type="entry",val=[True,False]):
        tmp_val = inputobj.get()
        if type == "switch":
            if tmp_val == "on":
                return val[0]
            else:
                return val[1]
        if type == "filepath":
            tmp_val = tmp_val.rstrip("\n").rstrip('"').lstrip('"').replace("/","\\")
        if tmp_val == "":
            tmp_val = None
        return tmp_val
        
    def regist_server(self):
        tmp_hostname = self.serverregist_entry.get()
        if tmp_hostname == "":
            tmp_hostname = None
        if tmp_hostname:
            self.sfm.set_serverdata(
                hostname        =   self.get_value_from_ctk(self.serverregist_entry )
                ,user           =   self.get_value_from_ctk(self.username_entry )
                ,psw            =   self.get_value_from_ctk(self.passwd_entry )
                ,usernameinput  =   self.get_value_from_ctk(self.usernameinput_entry )
                ,pswinput       =   self.get_value_from_ctk(self.pswinput_entry )
                ,consolesymbol  =   self.get_value_from_ctk(self.consolesymbol_entry )
                ,hostname2      =   self.get_value_from_ctk(self.hostname2_entry )
                ,user2          =   self.get_value_from_ctk(self.username2_entry )
                ,psw2           =   self.get_value_from_ctk(self.passwd2_entry )
                ,usernameinput2 =   self.get_value_from_ctk(self.usernameinput2_entry )
                ,pswinput2      =   self.get_value_from_ctk(self.pswinput2_entry )
                ,consolesymbol2 =   self.get_value_from_ctk(self.consolesymbol2_entry )
                ,optionsline    =   self.get_value_from_ctk(self.optionsline_entry )
                ,filetransdir   =   self.get_value_from_ctk(self.filetransdir_entry ,type="filepath")
                ,kanjicoder     =   self.get_value_from_ctk(self.kanjicoder_optionmenu )
                ,kanjicodet     =   self.get_value_from_ctk(self.kanjicodet_optionmenu )
                ,language       =   self.get_value_from_ctk(self.language_optionmenu )
                ,telnet         =   self.get_value_from_ctk(self.telnet_optionmenu )
                ,telnet2        =   self.get_value_from_ctk(self.telnet2_optionmenu )
                ,timeout        =   self.get_value_from_ctk(self.sliderval_timeout )
                ,windowhidden   =   self.get_value_from_ctk(self.windowhidden_switch_val ,type="switch")
                ,windowtitle    =   self.get_value_from_ctk(self.windowtitle_entry )
                ,windowx        =   self.get_value_from_ctk(self.sliderval_windowx )
                ,windowy        =   self.get_value_from_ctk(self.sliderval_windowy )
                ,autowinclose   =   self.get_value_from_ctk(self.autowinclose_switch_val,type="switch" )
                ,cdelayperchar  =   self.get_value_from_ctk(self.sliderval_cdelayperchar )
                ,cdelayperline  =   self.get_value_from_ctk(self.sliderval_cdelayperline )
            )
            self.sfm.save_serverdata(self.sfm.serverdata)
            self.reset_optionmenu()
    
    def edit_server(self):
        tmp_val = self.edit_serverregist_optionmenu.get()
        if tmp_val == "" or tmp_val is None:
            return
        pri_num = tmp_val.split("_")[0]
        sdata = self.sfm.get_serverdata(pri_num)
        sdata.hostname       =   self.get_value_from_ctk(self.serverregist_entry )
        sdata.user           =   self.get_value_from_ctk(self.username_entry )
        sdata.psw            =   self.get_value_from_ctk(self.passwd_entry )
        sdata.usernameinput  =   self.get_value_from_ctk(self.usernameinput_entry )
        sdata.pswinput       =   self.get_value_from_ctk(self.pswinput_entry )
        sdata.consolesymbol  =   self.get_value_from_ctk(self.consolesymbol_entry )
        sdata.hostname2      =   self.get_value_from_ctk(self.hostname2_entry )
        sdata.user2          =   self.get_value_from_ctk(self.username2_entry )
        sdata.psw2           =   self.get_value_from_ctk(self.passwd2_entry )
        sdata.usernameinput2 =   self.get_value_from_ctk(self.usernameinput2_entry )
        sdata.pswinput2      =   self.get_value_from_ctk(self.pswinput2_entry )
        sdata.consolesymbol2 =   self.get_value_from_ctk(self.consolesymbol2_entry )
        sdata.optionsline    =   self.get_value_from_ctk(self.optionsline_entry )
        sdata.filetransdir   =   self.get_value_from_ctk(self.filetransdir_entry ,type="filepath")
        sdata.kanjicoder     =   self.get_value_from_ctk(self.kanjicoder_optionmenu )
        sdata.kanjicodet     =   self.get_value_from_ctk(self.kanjicodet_optionmenu )
        sdata.language       =   self.get_value_from_ctk(self.language_optionmenu )
        sdata.telnet         =   self.get_value_from_ctk(self.telnet_optionmenu )
        sdata.telnet2        =   self.get_value_from_ctk(self.telnet2_optionmenu )
        sdata.timeout        =   self.get_value_from_ctk(self.sliderval_timeout )
        sdata.windowhidden   =   self.get_value_from_ctk(self.windowhidden_switch_val ,type="switch")
        sdata.windowtitle    =   self.get_value_from_ctk(self.windowtitle_entry )
        sdata.windowx        =   self.get_value_from_ctk(self.sliderval_windowx )
        sdata.windowy        =   self.get_value_from_ctk(self.sliderval_windowy )
        sdata.autowinclose   =   self.get_value_from_ctk(self.autowinclose_switch_val,type="switch" )
        sdata.cdelayperchar  =   self.get_value_from_ctk(self.sliderval_cdelayperchar )
        sdata.cdelayperline  =   self.get_value_from_ctk(self.sliderval_cdelayperline )
        self.sfm.save_serverdata(sdata)
        self.reset_optionmenu()
    
    def replace_entry_optionmenu(self,targetobj,val,type="entry"):
        if type=="optionmenu":
            if val is None:
                val = ""
            targetobj.set(val)
        elif type=="entry":
            if val is None:
                val = ""
            targetobj.delete(0,"end")
            targetobj.insert(0,val)
        elif type=="switch":
            if val is None:
                val = False
            if val==True:
                targetobj.select()
            else:
                targetobj.deselect()
    
    def fill_entry_optionmenu(self,sdata):
        self.replace_entry_optionmenu( self.serverregist_entry,sdata.hostname)
        self.replace_entry_optionmenu( self.username_entry,sdata.user)
        self.replace_entry_optionmenu( self.passwd_entry,sdata.psw)
        self.replace_entry_optionmenu( self.usernameinput_entry,sdata.usernameinput)
        self.replace_entry_optionmenu( self.pswinput_entry,sdata.pswinput)
        self.replace_entry_optionmenu( self.consolesymbol_entry,sdata.consolesymbol)
        self.replace_entry_optionmenu( self.hostname2_entry,sdata.hostname2)
        self.replace_entry_optionmenu( self.username2_entry,sdata.user2)
        self.replace_entry_optionmenu( self.passwd2_entry,sdata.psw2)
        self.replace_entry_optionmenu( self.usernameinput2_entry,sdata.usernameinput2)
        self.replace_entry_optionmenu( self.pswinput2_entry,sdata.pswinput2)
        self.replace_entry_optionmenu( self.consolesymbol2_entry,sdata.consolesymbol2)
        self.replace_entry_optionmenu( self.optionsline_entry,sdata.optionsline)
        self.replace_entry_optionmenu( self.filetransdir_entry,sdata.filetransdir)
        self.replace_entry_optionmenu( self.kanjicoder_optionmenu,sdata.kanjicoder,type="optionmenu")
        self.replace_entry_optionmenu( self.kanjicodet_optionmenu,sdata.kanjicodet,type="optionmenu")
        self.replace_entry_optionmenu( self.language_optionmenu,sdata.language,type="optionmenu")
        self.replace_entry_optionmenu( self.telnet_optionmenu,sdata.telnet,type="optionmenu")
        self.replace_entry_optionmenu( self.telnet2_optionmenu,sdata.telnet2,type="optionmenu")
        self.replace_entry_optionmenu( self.slider_timeout,sdata.timeout,type="optionmenu")
        self.replace_entry_optionmenu( self.windowhidden_switch,sdata.windowhidden,type="switch")
        self.replace_entry_optionmenu( self.windowtitle_entry,sdata.windowtitle)
        self.replace_entry_optionmenu( self.slider_windowx,sdata.windowx,type="optionmenu")
        self.replace_entry_optionmenu( self.slider_windowy,sdata.windowy,type="optionmenu")
        self.replace_entry_optionmenu( self.autowinclose_switch,sdata.autowinclose,type="switch")
        self.replace_entry_optionmenu( self.slider_cdelayperchar,sdata.cdelayperchar,type="optionmenu")
        self.replace_entry_optionmenu( self.slider_cdelayperline,sdata.cdelayperline,type="optionmenu")
        
    
    def set_edit_serverregist_optionmenu(self,tmp_val):
        self.serverregist_entry.delete(0,"end")
        self.del_serverregist_optionmenu.set("")
        tmp_val = self.edit_serverregist_optionmenu.get()
        if tmp_val == "" or tmp_val is None:
            return
        pri_num = tmp_val.split("_")[0]
        sdata = self.sfm.get_serverdata(pri_num)
        self.fill_entry_optionmenu(sdata)
    
    def set_del_serverregist_optionmenu(self,tmp_val):
        self.serverregist_entry.delete(0,"end")
        self.edit_serverregist_optionmenu.set("")
        tmp_val = self.edit_serverregist_optionmenu.get()
        if tmp_val == "" or tmp_val is None:
            return
        pri_num = tmp_val.split("_")[0]
        sdata = self.sfm.get_serverdata(pri_num)
        self.fill_entry_optionmenu(sdata)
    
    def del_serverregist_optionmenu(self):
        tmp_val = self.del_serverregist_optionmenu.get()
        if tmp_val == "" or tmp_val is None:
            return
        pri_num = tmp_val.split("_")[0]
        self.sfm.delete_serverdata(pri_num)
        self.reset_optionmenu()
        
    def none_chk(self,val):
        if val is None:
            return ""
        return val
        
    def reset_optionmenu(self):
        server_settings = self.sfm.get_serverdatas()
        server_settings = [str(s.primaryno)+"_"+self.none_chk(s.hostname)+"_"+self.none_chk(s.hostname2) for s in server_settings]
        self.edit_serverregist_optionmenu.configure(values=server_settings)
        self.del_serverregist_optionmenu.configure(values=server_settings)
        self.edit_serverregist_optionmenu.set("")
        self.del_serverregist_optionmenu.set("")
        self.serverregist_entry.delete(0,"end")
        self.username_entry.delete(0,"end")
        self.passwd_entry.delete(0,"end")
        self.usernameinput_entry.delete(0,"end")
        self.usernameinput_entry.insert(0,"login:")
        self.pswinput_entry.delete(0,"end")
        self.pswinput_entry.insert(0,"Password:")
        self.consolesymbol_entry.delete(0,"end")
        self.consolesymbol_entry.insert(0,"$")
        self.hostname2_entry.delete(0,"end")
        self.username2_entry.delete(0,"end")
        self.passwd2_entry.delete(0,"end")
        self.usernameinput2_entry.delete(0,"end")
        self.usernameinput2_entry.insert(0,"login:")
        self.pswinput2_entry.delete(0,"end")
        self.pswinput2_entry.insert(0,"Password:")
        self.consolesymbol2_entry.delete(0,"end")
        self.consolesymbol2_entry.insert(0,"$")
        self.optionsline_entry.delete(0,"end")
        self.filetransdir_entry.delete(0,"end")
        self.kanjicoder_optionmenu.set("")
        self.kanjicodet_optionmenu.set("")
        self.language_optionmenu.set("U")
        self.telnet_optionmenu.set("ssh")
        self.telnet2_optionmenu.set("ssh")
        self.slider_timeout.set(15)
        self.windowhidden_switch.deselect()
        self.windowtitle_entry.delete(0,"end")
        self.slider_windowx.set(200)
        self.slider_windowy.set(200)
        self.autowinclose_switch.deselect()
        self.slider_cdelayperchar.set(5)
        self.slider_cdelayperline.set(1)
    
    def set_auth_optionmenu(self,tmp_val):
        if tmp_val == "passwd":
            self.passwd_label.configure(text=self.trans.translate("Password"))
        elif tmp_val == "publickey":
            self.passwd_label.configure(text=self.trans.translate("PublicKey"))
    
    def set_language_optionmenu(self,tmp_val):
        language_dic = {
            "U" :self.trans.translate("U")
            ,"E" :self.trans.translate("E")
            ,"J" :self.trans.translate("J")
            ,"K" :self.trans.translate("K")
            ,"R" :self.trans.translate("R")
        }
        self.language_label.configure(text=language_dic[tmp_val])
    
    def open_filetransdir(self):
        initialdir = os.path.dirname(self.filetransdir_entry.get())
        title = self.trans.translate("FileTransferFolder")
        file_path = filedialog.askdirectory(title=title,initialdir=initialdir)
        if file_path:
            self.filetransdir_entry.delete(0,"end")
            self.filetransdir_entry.insert(0,file_path)
    
    def set_windowx(self,tmp_val):
        self.windowx_label.configure(text=tmp_val)
    
    def set_windowy(self,tmp_val):
        self.windowy_label.configure(text=tmp_val)
    
    def set_cdelayperchar(self,tmp_val):
        self.cdelayperchar_label.configure(text=tmp_val)
    
    def set_cdelayperline(self,tmp_val):
        self.cdelayperline_label.configure(text=tmp_val)
    
    def set_timeout(self,tmp_val):
        self.timeout_label.configure(text=tmp_val)
    
    def windowhidden_switch_event(self):
        if self.windowhidden_switch_val.get() == "on":
            tmp_text = self.trans.translate("Hide")
        else:
            tmp_text = self.trans.translate("Show")
        self.windowhidden_label.configure(text=tmp_text)
    
    def autowinclose_switch_event(self):
        if self.autowinclose_switch_val.get() == "on":
            tmp_text = self.trans.translate("Close")
        else:
            tmp_text = self.trans.translate("DoNotClose")
        self.autowinclose_label.configure(text=tmp_text)
    
    @staticmethod
    def open_file_dialog(filetypes,initialdir):
        # Open a file dialog and get the selected file path
        # [('data files','*.csv;*.txt')]
        file_path = filedialog.askopenfilename(filetypes=filetypes,initialdir=initialdir)
        if file_path:
            return file_path
        return None
    