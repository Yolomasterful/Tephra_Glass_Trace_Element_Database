import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.constants import *

grey = {
    "name": "purple_cream",
    "colors": {
        # Basic colors
        "primary": "#5C5470",       # Button background
        "secondary": "#5C5470",     # Secondary elements
        "success": "#5C5470",       # Success state
        "info": "#5C5470",          # Info elements
        "warning": "#B9B4C7",       # Warning state
        "danger": "#B9B4C7",        # Danger state
        "light": "#B9B4C7",         # Light elements
        "dark": "#352F44",          # Dark elements (window bg)
        
        # Core application colors
        "bg": "#352F44",            # Window background
        "fg": "#FAF0E6",            # Text color
        "selectbg": "#B9B4C7",      # Selection background
        "selectfg": "#352F44",      # Selection text
        "border": "#5C5470",        # Border color
        "inputfg": "#FAF0E6",      # Input text
        "inputbg": "#5C5470",       # Input background
        
        # Button states
        "active": {
            "bg": "#B9B4C7",        # Active (clicked) background
            "fg": "#352F44"         # Active text
        },
        "disabled": {
            "fg": "#7A7289",        # Disabled text
            "bg": "#4A4458"         # Disabled background
        }
    }
}

root = ttk.Window()
root.title("Laser Abblation GUI")
root.resizable(True, True)
root.minsize(16*50, 9*50)
#root.geometry(f"{16*30}x{9*30}")

#root.configure(bg="#352F44")


title = ttk.Label(root, text="Laser Abblation Database GUI", font=("Arial", 25))
title.grid()



root.mainloop()

