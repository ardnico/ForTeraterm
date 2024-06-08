import customtkinter
from ForTeraterm.WindowSettings.theme import *

class ThemeSample(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry(f"1000x800")
        self.title("theme_sample")
        
        self.mainframe = ThemeFrame1(self)
        self.mainframe.pack()
        
        self.theme = ThemeManager()
        themelist = list(self.theme.themes.keys())
        self.setting = ThemeOptionMenuBold2(self.mainframe,values=themelist
            ,command=self.theme_set)
        self.setting.pack()
        
        self.sample_label = ThemeCTKLabel1(self.mainframe,text="Sample")
        self.sample_label.pack()
        self.sample_labe2 = ThemeCTKLabel2(self.mainframe,text="Sample")
        self.sample_labe2.pack()
        
        self.frame2 = ThemeCTKFrame2(self.mainframe)
        self.frame2.pack()
        
        self.a = ThemeTabview1(self.mainframe)
        self.a.pack()
        
        self.a.add("tab 1")  # add tab at the end
        self.a.add("tab 2")  # add tab at the end
        self.a.add("tab 3")  # add tab at the end
        self.a.set("tab 1")  # set currently visible tab

        self.button_1 = ThemeButton1(self.a.tab("tab 1"))
        self.button_1.pack(padx=20, pady=20)
        
        self.chkbox = ThemeCheckBox1(self.a.tab("tab 1"))
        self.chkbox.pack()
        self.cbox = ThemeComboBoxBold1(self.a.tab("tab 1"),values=["cb1","2,3,4","5"])
        self.cbox.pack()
        
        
        self.button_2 = ThemeButton2(self.a.tab("tab 1"),text="button2")
        self.button_2.pack(padx=20, pady=20)
        
        self.slider1 = ThemeSlider1(self.a.tab("tab 1"))
        self.slider1.pack(padx=20, pady=20)
        
        self.slider2 = ThemeSlider2(self.a.tab("tab 2"))
        self.slider2.pack(padx=20, pady=20)
        
        self.checkbox1 = ThemeCheckBox1(self.a.tab("tab 2"))
        self.checkbox1.pack(padx=20, pady=20)
        
        self.checkbox2 = ThemeCheckBox2(self.a.tab("tab 2"))
        self.checkbox2.pack(padx=20, pady=20)
        
        
        self.sw1 = ThemeSwitch1(self.a.tab("tab 2"))
        self.sw1.pack()
        
        self.sw2 = ThemeSwitch2(self.a.tab("tab 2"))
        self.sw2.pack()
        
        
        self.b = ThemeTabview2(self.a.tab("tab 2"))
        self.b.pack()
        self.b.add("tab 1")  # add tab at the end
        self.b.add("tab 2")  # add tab at the end
        self.b.set("tab 2")  # set currently visible tab
        
        self.sframe1 = ThemeScrollableFrame1(self.a.tab("tab 2"))
        self.sframe1.pack()
        
        self.sframe2 = ThemeScrollableFrame2(self.a.tab("tab 2"))
        self.sframe2.pack()
        
        self.cbox2 = ThemeComboBox2(self.a.tab("tab 2"),values=["cb2","2,3,4","5"])
        self.cbox2.pack()
        
        self.opm1 = ThemeOptionMenu1(self.a.tab("tab 2"),values=["op1","rsdrg"])
        self.opm1.pack()
        
        self.opm2 = ThemeOptionMenuBold2(self.a.tab("tab 3"),values=["op1","rsdrg"])
        self.opm2.pack()
        
        self.rb1 = ThemeRadioButton1(self.a.tab("tab 3"))
        self.rb1.pack()
        
        self.rb2 = ThemeRadioButton2(self.a.tab("tab 3"))
        self.rb2.pack()
        
        self.tbox1 = ThemeTextbox1(self.a.tab("tab 3"))
        self.tbox1.pack()
        
        self.tbox2 = ThemeTextbox2(self.a.tab("tab 3"))
        self.tbox2.pack()
        
        # self.td = ThemeInputDialog1()
        # self.td.get_input()
        
        # self.td = ThemeInputDialog2()
        # self.td.get_input()
        
        self.mainloop()

    def theme_set(self,tmp_val):
        self.theme.set_theme(tmp_val)
        self.destroy()
        self = ThemeSample()
        
