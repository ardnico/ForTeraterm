del /q dist\main\
echo y|pyinstaller main.spec
mkdir .\dist\main\img
mkdir .\dist\main\locales
mkdir .\dist\main\icons
copy .\img\* .\dist\main\img\
copy .\locales\* .\dist\main\locales\
copy .\icons\* .\dist\main\icons\
copy .\README.pdf .\dist\main\

python write_mkinstiss.py
"C:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc mkinst.iss
