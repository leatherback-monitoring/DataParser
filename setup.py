from distutils.core import setup
import py2exe
import sys
from glob import glob

sys.setrecursionlimit(3000)

#dll wizardry: http://www.py2exe.org/index.cgi/Tutorial#Step5
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
#also: http://stackoverflow.com/questions/12127869/error-msvcp90-dll-no-such-file-or-directory-even-though-microsoft-visual-c
setup(
data_files=data_files,
    options = {
            "py2exe":{"dll_excludes": ["MSVCP90.dll", "HID.DLL", "w9xpopen.exe"]}
    },
    console = [{'script': 'basic.py'}]
)

sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")