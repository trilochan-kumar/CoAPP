Commands to know for executable file generation using pyinstaller:

# Build the .exe, .app, or linux executable distribution
PyInstaller hello.py

# Create only a single file (slower to run, easier to distribute)
PyInstaller hello.py -F

# Tell application not to launch console (e.g. PyQt5, GTK+, tkinter GUIs)
PyInstaller hello.py --noconsole

# Specify the icon file to use
PyInstaller hello.py --icon=path/to/icon.ico