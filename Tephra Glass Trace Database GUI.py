import os, matplotlib, sqlite3
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.style import Style
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.constants import *

class ToolTip:
  def __init__(self, widget, text_var, bg_color="white", fg_color="black"):
    self.widget = widget
    self.text_var = text_var
    self.tooltip_window = None
    self.bg_color = bg_color
    self.fg_color = fg_color
    self.widget.bind("<Enter>", self.show_tooltip)
    self.widget.bind("<Leave>", self.hide_tooltip)

  def show_tooltip(self, event):
    x = event.x_root + 10  # Position tooltip slightly to the right
    y = event.y_root + 10  # Position tooltip slightly below
    self.tooltip_window = ttk.Toplevel(self.widget)
    self.tooltip_window.wm_overrideredirect(True)  # Remove window decorations
    self.tooltip_window.wm_geometry(f"+{x}+{y}")  # Position the tooltip
    label = ttk.Label(self.tooltip_window, text=self.text_var.get(), 
                      background=self.bg_color, foreground=self.fg_color, 
                      borderwidth=1, relief="solid")
    label.pack()

  def hide_tooltip(self, event):
    if self.tooltip_window:
      self.tooltip_window.destroy()
      self.tooltip_window = None

class App:

  def __init__(self, root):
    self._variables()

    self._root = root

    self._layout()
  
  def _variables(self):
    self._root = None
    self._tooltip = None
    self._style = Style(theme='darkly')

    self._files = {'Database':None, 'DataFile':None}

    self._database_filename = ttk.StringVar(value="None")
    self._data_filename = ttk.StringVar(value="None")

  def _layout(self):
    
    file_mgr_frame = ttk.Frame(self._root, relief='solid')

    imp_db = ttk.Button(file_mgr_frame, text="Import Database", command=lambda: self._set_file('Database', self._import_file((("Database", "*.db"),))))
    imp_db.grid(padx=(10,5), pady=10, column=0,row=0)

    crt_db = ttk.Button(file_mgr_frame, text="Create Database", command=lambda: self._set_file('Database', self._create_file()))
    crt_db.grid(padx=(5,5), pady=10, column=1, row=0)

    imp_df = ttk.Button(file_mgr_frame, text="Import Datafile", command=lambda: self._set_file('DataFile',self._import_file((("Excel Spreadsheet", "*.xlsx"), ("Comma Seperated Values", "*.csv"), ("Any Types", "*")))))
    imp_df.grid(padx=(5,5), pady=10, column=2, row=0)

    rmv = ttk.Button(file_mgr_frame, text="Remove Selected", style='TButtonDanger', command=lambda: self._reset_files())
    rmv.grid(padx=(5,10), pady=10, column=3, row=0)

    ToolTip(imp_db, self._database_filename)
    ToolTip(crt_db, self._database_filename)
    ToolTip(imp_df, self._data_filename)

    file_mgr_frame.grid()

  def _set_file(self, key, value):
    self._files.update({key:value})
    self._update_vars()

  def _import_file(self, extensions:tuple):
    return filedialog.askopenfile(title="Choose File...", initialdir=os.getcwd(), filetypes=extensions)
  
  def _create_file(self):
    return open(filedialog.asksaveasfilename(title="Save As...", initialdir=os.getcwd(), defaultextension=".db", filetypes=(("Database", "*.db"),)), "w")

  def _update_vars(self):
    if self._files['Database'] != None:
      self._database_filename.set(self._files['Database'].name)
    else: self._database_filename.set("None")
    
    if self._files['DataFile'] != None:
      self._data_filename.set(self._files['DataFile'].name)
    else: self._data_filename.set("None")

  def _reset_files(self):
    self._files = {'Database':None, 'DataFile':None}
    self._update_vars()


root = ttk.Window()
app = App(root)
root.title("Tephra Glass Trace Database GUI")
root.resizable(True, True)
root.minsize(16*50, 9*50)
root.geometry(f"{16*30}x{9*30}")

root.mainloop()

"""
style = Style()
    style.configure('CustomFrame.Main.TFrame',
                    background='#352F44',
                    foreground='#ffffff',
                    font=('Helvetica',14),
                    padding=20)
    
  
    style.configure('CustomNotebook.TNotebook',
                    background='#352F44',
                    foreground='#ffffff')
    
    style.configure('CustomNotebook.Tab.TNotebook',
                background='#4A3F5A',
                foreground='white',
                padding=10,
                font=('Helvetica', 12))
    
    style.map('CustomNotebook.Tab.TNotebook',
              background=[('active', '#ffffff')],
              foreground=[('active', '#000000')])
"""


#menu_bar = ttk.Menu(root)

#file_menu = ttk.Menu(menu_bar, tearoff=0)

#file_menu.add_command(label="Import Spreadsheet", command=lambda: self._import_file((("Excel Spreadsheet", "*.xlsx"), ("Comma Seperated Values", "*.csv"), ("Any Types", "*"))))
#file_menu.add_command(label="Import Database", command=lambda: self._import_file((("Database", "*.db"),)))

#menu_bar.add_cascade(label="File", menu=file_menu)

#self._root.config(menu=menu_bar)

#title = ttk.Label(self._root, text="Laser Abblation Database GUI", font=("Arial", 25), foreground='#ffffff', background='#352F44')
#title.grid(column=0, columnspan=2, row=0)

#button = ttk.Button(self._root, text="Import Unorganized Data", command=lambda: globals().update({'self._database_file': self._import_file((("Excel Spreadsheet", "*.xlsx"),))}))
#button.grid(column=0, row=1)

#ttk.Label(self._root, textvariable=self._database_file).grid(column=1, row=1)


""" button = ttk.Button(root, text="Import Database", command=lambda: (self._database := self._import_file((("Database", "*.db"),)))
button.grid(column=1, row=1) """