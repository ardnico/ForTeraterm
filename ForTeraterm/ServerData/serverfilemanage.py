import os
import json
import dataclasses
from glob import glob
import subprocess
import time
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
    
    # @appconf.log_exception
    def set_serverdata(
        self
        ,hostname            : str   = None
        ,user                : str   = None
        ,psw                 : str   = None
        ,usernameinput       : str   = "login:"
        ,pswinput            : str   = "Password:"
        ,consolesymbol       : str   = "$"
        ,hostname2           : str   = None
        ,user2               : str   = None
        ,psw2                : str   = None
        ,usernameinput2      : str   = "login:"
        ,pswinput2           : str   = "Password:"
        ,consolesymbol2      : str   = "$"
        ,optionsline         : str   = None
        ,teratermini         : str   = None
        ,filetransdir        : str   = None
        ,kanjicoder          : str   = None
        ,kanjicodet          : str   = None
        ,language            : str   = "U"
        ,telnet              : str  = "ssh"
        ,telnet2             : str  = "ssh"
        ,timeout             : int   = None
        ,windowhidden        : bool  = False
        ,windowtitle         : str   = None
        ,windowx             : int   = None
        ,windowy             : int   = None
        ,autowinclose        : bool  = False
        ,cdelayperchar       : int   = 5
        ,cdelayperline       : int   = 1
        ):
        primaryno = self.get_primary_number()
        if primaryno is None:
            return
        self.serverdata = ServerDatas(
            primaryno      
            ,hostname       
            ,user           
            ,psw            
            ,usernameinput  
            ,pswinput       
            ,consolesymbol  
            ,hostname2      
            ,user2          
            ,psw2           
            ,usernameinput2 
            ,pswinput2          
            ,consolesymbol2 
            ,optionsline    
            ,teratermini    
            ,filetransdir   
            ,kanjicoder     
            ,kanjicodet     
            ,language       
            ,telnet         
            ,telnet2        
            ,timeout        
            ,windowhidden   
            ,windowtitle    
            ,windowx        
            ,windowy        
            ,autowinclose   
            ,cdelayperchar
            ,cdelayperline
        )
    
    # @appconf.log_exception
    def get_primary_number(self):
        files = glob(os.path.join(self.datadir, "[0-9]" * 5 + ".json"))
        if len(files) == 0:
            return 0
        files = [int(os.path.basename(f).split(".")[0]) for f in files]
        for i in range(10**5 + 1):
            if i not in files:
                return i
        return None
    
    # @appconf.log_exception
    def get_json(self,sdata: ServerDatas):
        enc = MyEncoder()
        return enc.default(sdata)
    
    # @appconf.log_exception
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
    
    # @appconf.log_exception
    def delete_serverdata(self,primaryno):
        primaryno = str(primaryno)
        filename = os.path.join(self.datadir, f"{primaryno.zfill(5)}.json")
        if os.path.exists(filename)==True:
            os.remove(filename)
    
    # @appconf.log_exception
    def save_serverdata(self,sdata: ServerDatas):
        if sdata.user:
            sdata.user = appconf.enc.encrypt(sdata.user)
        if sdata.psw:
            sdata.psw = appconf.enc.encrypt(sdata.psw)
        if sdata.user2:
            sdata.user2 = appconf.enc.encrypt(sdata.user2)
        if sdata.psw2:
            sdata.psw2 = appconf.enc.encrypt(sdata.psw2)
        filename = os.path.join(self.datadir, f"{str(sdata.primaryno).zfill(5)}.json")
        with open(filename, 'w') as f:
            d = self.get_json(sdata)
            json.dump(d, f, indent=2)
    
    # @appconf.log_exception
    def get_serverdatas(self):
        ret = []
        files = glob(os.path.join(self.datadir, "[0-9]" * 5 + ".json"))
        if len(files) == 0:
            return ret
        filenums = [int(os.path.basename(f).split(".")[0]) for f in files]
        for i in filenums:
            ret.append(self.get_serverdata(i))
        return ret
    
    def tmp_macro_exec(self,sdata: ServerDatas,optionsline,macro_path):
        if macro_path is None or macro_path == "":
            macro_txt = ""
        else:
            with open(macro_path,"r",encoding="utf-8") as f:
                macro_txt = f.read()
        tmp_macro_path = os.path.join(os.getcwd(),f"tmp_macro_exec_txt{sdata.primaryno}.ttl")
        tmp_macro_txt = f"""
;Setting
hostname='{self.val_none_check(sdata.hostname)}'
user='{self.val_none_check(sdata.user)}'
psw='{self.val_none_check(sdata.psw)}'
usernameinput='{self.val_none_check(sdata.usernameinput)}'
pswinput='{self.val_none_check(sdata.pswinput)}'
consolesymbol='{self.val_none_check(sdata.consolesymbol)}'

sshtelnet='{self.val_none_check(sdata.telnet)}'
connectoptionline='{optionsline}'

hostname2='{self.val_none_check(sdata.hostname2)}'
user2='{self.val_none_check(sdata.user2)}'
psw2='{self.val_none_check(sdata.psw2)}'
usernameinput2='{self.val_none_check(sdata.usernameinput2)}'
pswinput2='{self.val_none_check(sdata.pswinput2)}'
consolesymbol2='{self.val_none_check(sdata.consolesymbol2)}'
telnet2='{self.val_none_check(sdata.telnet2)}'
consolesymbol2='{self.val_none_check(sdata.consolesymbol2)}'

;data check
strcompare hostname ''
if result=0 goto fail0
getdate logfile "log-%Y%m%d-%H%M%S-"
strconcat logfile hostname
strconcat logfile '-'
strconcat logfile hostname2
strconcat logfile '.log'


goto login
;Additional Process
:addprocess
timeout={sdata.timeout}

{macro_txt}

goto eol
;login process
:login
getdate datestr '%y%m%d'
connectline=hostname

strmatch 'ssh' sshtelnet
if result=1 goto setcline1

strmatch 'telnet' sshtelnet
if result=1 goto setcline2

strmatch 'con' sshtelnet
if result=1 goto setcline3


:setcline1
strconcat connectline ' /ssh'
strtrim sshtelnet 'ssh'
strcompare sshtelnet ''
if result=0 goto setcline11
strconcat connectline  ' /'
strconcat connectline sshtelnet
strconcat connectline ' '
:setcline11
goto setcline21

:setcline2
strconcat connectline ':23 /T=1 '
connect connectline
if result<>2 goto fail1
goto inputuser0

:setcline21
strconcat connectline ' /auth=password /user='
strconcat connectline user
strconcat connectline ' /passwd='
strconcat connectline psw
strconcat connectline ' /L='
strconcat connectline logfile
strconcat connectline ' '
strconcat connectline connectoptionline
timeout=3
connect connectline
if result<>2 goto fail1

goto setcline4

:inputuser0
wait usernameinput
sendln user
wait pswinput
if result=0 goto fail
sendln psw

goto setcline4
:setcline3
connectline=' /C='
strtrim sshtelnet 'con'
strcompare sshtelnet ''
if result=0 goto fail0

getdate dateline "log-%Y%m%d-%H%M%S-"
strconcat connectline ' /'
strconcat connectline sshtelnet
strconcat connectline ' /L='
strconcat connectline dateline
strconcat connectline 'COM'
strconcat connectline sshtelnet
strconcat connectline '.log '
strconcat connectline connectoptionline

connect connectline

:setcline4
wait consolesymbol

strcompare hostname2 ''
if result=0 goto addprocess

connectline2=telnet2
strconcat connectline2 ' '
strconcat connectline2 hostname2
connect connectline2
wait usernameinput2
sendln user2
wait pswinput2
if result=0 goto fail
sendln psw2
wait consolesymbol2

goto addprocess

:fail
titleline='Error'
failmsg='Please review the sending delay settings etc.'

goto msgbox
:fail0
titleline='Value error'
failmsg='No server was selected'
goto msgbox

:fail1
titleline=hostname
failmsg='Failed to connect bastion server'
goto msgbox

:fail2
titleline=hostname2
failmsg='Failed to connect target server'
:msgbox
messagebox failmsg titleline
:eol
        """
        with open(tmp_macro_path,"w",encoding="utf-8") as f:
            f.write(tmp_macro_txt)
        subprocess.Popen([appconf.get_data("TeratermPath"),f"/M={tmp_macro_path}"])
        time.sleep(3)
        os.remove(tmp_macro_path)
    
    def val_none_check(self,val):
        if val is None:
            return ""
        return val
    
    def access_server(self,sdata:ServerDatas,macro_path):
        optionsline = []
        if sdata.teratermini:
            optionsline.append(f'/F="{sdata.teratermini}"')
        if sdata.filetransdir:
            optionsline.append(f'/FD="{sdata.filetransdir}"')
        if sdata.kanjicoder:
            optionsline.append(f"/KR={sdata.kanjicoder}")
        if sdata.kanjicodet:
            optionsline.append(f"/KT={sdata.kanjicodet}")
        if sdata.language:
            optionsline.append(f"/LA={sdata.language}")
        if sdata.windowhidden:
            optionsline.append(f"/V")
        if sdata.windowtitle:
            optionsline.append(f"/W={sdata.windowtitle}")
        if sdata.windowx:
            optionsline.append(f"/X={str(sdata.windowx)}")
        if sdata.windowy:
            optionsline.append(f"/Y={str(sdata.windowy)}")
        if sdata.autowinclose:
            optionsline.append("/AUTOWINCLOSE=on")
        if sdata.cdelayperchar:
            optionsline.append(f"/CDELAYPERCHAR={str(sdata.cdelayperchar)}")
        if sdata.cdelayperline:
            optionsline.append(f"/CDELAYPERLINE={str(sdata.cdelayperline)}")
        if sdata.optionsline:
            optionsline.append(sdata.optionsline)
        
        optionsline = " ".join(optionsline)
        self.tmp_macro_exec(sdata,optionsline,macro_path)
        
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
    