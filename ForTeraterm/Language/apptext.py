
import json
import os
from glob import glob

class AppText:
    def __init__(self,current_language):
        self.translations = self.load_translations(current_language)
    
    def load_translations(self,language_code):
        with open(os.path.join(os.getcwd(),"locales",f"{language_code}.json"), 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def translate(self,text):
        return self.translations.get(text, text)
    
    def lang_list(self):
        file_path = glob(os.path.join(os.getcwd(),"locales","*.json"))
        file_path = [os.path.basename(f) for f in file_path]
        file_path = [f.split(".")[0] for f in file_path]
        return file_path