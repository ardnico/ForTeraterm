import json
from dataclasses import dataclass
from dataclasses import asdict, is_dataclass

@dataclass
class ServerDatas:
    primaryno           : int   = None
    hostname            : str   = None
    user                : str   = None
    psw                 : str   = None
    usernameinput       : str   = "login:"
    pswinput            : str   = "Password:"
    consolesymbol       : str   = "$"
    hostname2           : str   = None
    user2               : str   = None
    psw2                : str   = None
    usernameinput2      : str   = "login:"
    pswinput2           : str   = "Password:"
    consolesymbol2      : str   = "$"
    optionsline         : str   = None
    teratermini         : str   = None
    filetransdir        : str   = None
    kanjicoder          : str   = None
    kanjicodet          : str   = None
    language            : str   = "U"
    telnet              : str  = "ssh"
    telnet2             : str  = "ssh"
    timeout             : int   = None
    windowhidden        : bool  = False
    windowtitle         : str   = None
    windowx             : int   = None
    windowy             : int   = None
    autowinclose        : bool  = False

def server_datas_decoder(data):
    return ServerDatas(**data)

# https://zenn.dev/tomlla/articles/542cc59cb0cc0b268ff9
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return json.JSONEncoder.default(self, obj)
