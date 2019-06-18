import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": 
						["os","sys","threading","PyQt5","numpy",
						"tqdm","numpy","IPython","tifffile",
						"simulation","multispecies_simulation","molecule"], "excludes": ["tkinter"],
						'include_files': [os.path.join(sys.base_prefix, 'pkgs','sqlite-3.27.2-he774522_0','Library','bin', 'sqlite3.dll')]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
base = "Win32GUI"

setup(  name = "gui",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("gui.py", base=base)])