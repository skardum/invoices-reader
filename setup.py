import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "QtWidgets", "sys", "cv2", "xlwt", "QFileDialog", "QMessageBox", "QtGui", "Qt", "QtCore", "QProgressBar", "main",
                                  "pyzbar.pyzbar", "base64", "string"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="invoices reader",
      version="0.1",
      description="invoices reader",
      options={"build_exe": build_exe_options},
      executables=[Executable("gui.py", base=base)])
