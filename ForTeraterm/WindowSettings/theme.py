
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