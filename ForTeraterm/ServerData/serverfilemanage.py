import os
import json
import dataclasses
from glob import glob
import subprocess
from .serverdata import ServerDatas
from .serverdata import MyEncoder
from .serverdata import server_datas_decoder
from ..WindowSettings.conf import appconf
from ..Language.apptext import AppText

class ServerFileManage:
    def __init__(self):
        self.datadir = "serverdata"
        os.makedirs(self.datadir,exist_ok=True)
        appconf.set_log()
    
    @appconf.log_exception
    def set_serverdata(
        self
        ,hostname            : str      = None
        ,user                : str      = None
        ,psw                 : str      = None
        ,hostname2           : str      = None
        ,user2               : str      = None
        ,psw2                : str      = None
        ,method              : str      = "passwd"
        ,optionsline         : str      = None
        ,teratermini         : str      = None
        ,filetransdir        : str      = None
        ,kanjicoder          : str      = None
        ,kanjicodet          : str      = None
        ,logfile             : str      = None
        ,language            : str      = "U"
        ,telnet              : bool     = False
        ,timeout             : int      = None
        ,windowhidden        : bool     = False
        ,windowtitle         : str      = None
        ,windowx             : int      = None
        ,windowy             : int      = None
        ,autowinclose        : bool     = False
        ):
        primaryno = self.get_primary_number()
        if primaryno is None:
            return
        if user:
            user = appconf.enc.encrypt(user)
        else:
            return
        if psw:
            psw = appconf.enc.encrypt(psw)
        if user2:
            user2 = appconf.enc.encrypt(user2)
        if psw2:
            psw2 = appconf.enc.encrypt(psw2)
        self.serverdata = ServerDatas(
            primaryno
            ,hostname
            ,user
            ,psw
            ,hostname2
            ,user2
            ,psw2
            ,method
            ,optionsline
            ,teratermini
            ,filetransdir
            ,kanjicoder
            ,kanjicodet
            ,logfile
            ,language
            ,telnet
            ,timeout
            ,windowhidden
            ,windowtitle
            ,windowx
            ,windowy
            ,autowinclose
        )
    
    @appconf.log_exception
    def get_primary_number(self):
        files = glob(os.path.join(self.datadir, "[0-9]" * 5 + ".json"))
        if len(files) == 0:
            return 0
        files = [int(os.path.basename(f).split(".")[0]) for f in files]
        for i in range(10**5 + 1):
            if i not in files:
                return i
        return None
    
    @appconf.log_exception
    def get_json(self):
        if self.serverdata:
            enc = MyEncoder()
            return enc.default(self.serverdata)
        return None
    
    @appconf.log_exception
    def get_serverdata(self, primary_number):
        filename = os.path.join(self.datadir, f"{str(primary_number).zfill(5)}.json")
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as tmp_json:
            self.serverdata = json.load(tmp_json, object_hook=server_datas_decoder)
        tmp_serverdata = dataclasses.replace(self.serverdata)
        if tmp_serverdata.user:
            tmp_serverdata.user = appconf.enc.decrypt(tmp_serverdata.user)
        if tmp_serverdata.psw:
            tmp_serverdata.psw = appconf.enc.decrypt(tmp_serverdata.psw)
        if tmp_serverdata.user2:
            tmp_serverdata.user2 = appconf.enc.decrypt(tmp_serverdata.user2)
        if tmp_serverdata.psw2:
            tmp_serverdata.psw2 = appconf.enc.decrypt(tmp_serverdata.psw2)
        return tmp_serverdata
    
    @appconf.log_exception
    def save_serverdata(self):
        if self.serverdata:
            filename = os.path.join(self.datadir, f"{str(self.serverdata.primaryno).zfill(5)}.json")
            with open(filename, 'w') as f:
                d = self.get_json()
                json.dump(d, f, indent=2)
    
    @appconf.log_exception
    def get_serverdatas(self):
        ret = []
        files = glob(os.path.join(self.datadir, "[0-9]" * 5 + ".json"))
        if len(files) == 0:
            return ret
        filenums = [int(os.path.basename(f).split(".")[0]) for f in files]
        for i in filenums:
            ret.append(self.get_serverdata(i))
        return ret
    
    def access_server(self,sdata:ServerDatas,macro_path):
        teraterm_command = [appconf.get_data("TeratermPath")]
        if sdata.telnet == True:
            teraterm_command.append(f"telnet://{sdata.hostname}")
            teraterm_command.append(f"/T=1")
        else:
            teraterm_command.append(sdata.hostname)
            teraterm_command.append(f"/T=0")
        teraterm_command.append(f"/auth={sdata.hostname}")
        teraterm_command.append(f"/user={sdata.user}")
        if sdata.method == "passwd":
            teraterm_command.append(f"/passwd={sdata.psw}")
        elif sdata.method == "publickey":
            teraterm_command.append(f"/keyfile={sdata.psw}")
        
        hostname2           : str   = None
        user2               : str   = None
        psw2                : str   = None

        if sdata.teratermini:
            teraterm_command.append(f"/F={sdata.teratermini}")
        if sdata.filetransdir:
            teraterm_command.append(f"/FD={sdata.filetransdir}")
        
        # kanjicoder          : str   = None
        # kanjicodet          : str   = None
        
        if sdata.logfile:
            teraterm_command.append(f"/FD={sdata.logfile}")
        if sdata.language:
            teraterm_command.append(f"/LA={sdata.language}")
        if macro_path:
            teraterm_command.append(f"/M={macro_path}")
        if sdata.timeout:
            teraterm_command.append(f"/TIMEOUT={sdata.timeout}")
        if sdata.windowhidden:
            teraterm_command.append(f"/V")
        if sdata.windowtitle:
            teraterm_command.append(f"/W={sdata.windowtitle}")
        if sdata.windowx:
            teraterm_command.append(f"/X={sdata.windowx}")
        if sdata.windowy:
            teraterm_command.append(f"/Y={sdata.windowy}")
        if sdata.autowinclose:
            teraterm_command.append("/AUTOWINCLOSE=on")
        if sdata.optionsline:
            teraterm_command.append(sdata.optionsline)
        subprocess.Popen(teraterm_command)
        
    def mk_ttl(self,title,commandline):
        self.trans = AppText(appconf.get_data("lang"))
        if title:
            file_path = os.path.join(appconf.get_data("macro_path"),f"{title}.ttl")
            if os.path.exists(file_path)==True:
                with open(file_path,"w",encoding="utf-8") as f:
                    f.write(commandline)
                return
            with open(file_path,"w",encoding="utf-8") as f:
                f.write(commandline)
    