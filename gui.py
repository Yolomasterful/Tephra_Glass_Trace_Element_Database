import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="darkly")
root.title("Laser Abblation GUI")
root.resizable(True, True)
#root.geometry(f"{16*30}x{9*30}")

title = ttk.Label(root, text="Laser Abblation Database GUI", font=("Arial", 25), bootstyle=(INFO))
title.pack(side=TOP, padx=20, pady=20)

b1 = ttk.Button(root, text="Button 1", bootstyle=(DARK))
b1.pack(side=TOP, padx=20, pady=20)

b2 = ttk.Checkbutton(root, bootstyle=(SUCCESS, ROUND, TOGGLE))
b2.pack(side=TOP, padx=20, pady=20)

root.mainloop()

