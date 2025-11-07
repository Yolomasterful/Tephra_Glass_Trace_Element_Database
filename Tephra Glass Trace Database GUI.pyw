import os, csv, time, matplotlib, sqlite3

from PIL import Image, ImageTk

from tkinter import filedialog
from tkinter import messagebox
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
    label = ttk.Label(self.tooltip_window, text=self.text_var, 
                      background=self.bg_color, foreground=self.fg_color, 
                      borderwidth=1, relief="solid")
    label.pack()

  def hide_tooltip(self, event):
    if self.tooltip_window:
      self.tooltip_window.destroy()
      self.tooltip_window = None

class Database:
  def __init__(self, database_file:str):
    self._con = sqlite3.connect(database_file)
    self._cur = self._con.cursor()

    self._cur.execute("""PRAGMA foreign_keys = ON;""")

    self._samples_table()
  
  def _samples_table(self):
    self._cur.execute(f"""PRAGMA table_info({"Samples"});""")
    exists = self._cur.fetchone() is not None

    if not exists:
      self._cur.execute("""CREATE TABLE "Samples" 
                        ("sID" INTEGER NOT NULL,
                        "sName" TEXT NOT NULL,
                        "IntStdWv" FLOAT,
                        PRIMARY KEY ("sID")
                        ); """)
      self._con.commit()

  def _raw_command(self, query):
    print(query)
    try:
      self._raw_command_output = self._cur.execute(query).fetchall()
      print(self._raw_command_output)
      return self._raw_command_output
    except Exception as e:
      print(e)
      return None

  def _export_selection(self):
    pass

  def _export_all(self):
    self._cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'Samples' """)
    for table in self._cur.fetchall():
      table = table[0]
      self._cur.execute(f"""SELECT * FROM "{table}" """)
      rows = self._cur.fetchall()
      headers = [d[0] for d in self._cur.description]
      headers = ["IntStdWv",] + ["Sample",] + headers[3:]

      with open(f"{table}.csv", "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(headers)
        self._cur.execute(f"""SELECT "IntStdWv" FROM "Samples" NATURAL JOIN "{table}" WHERE "sIteration" LIKE '%' || "sName" || '%' """)
        for row in rows:
          w.writerow([self._cur.fetchone()[0]]+list(row[2:]))

  def _auto_parse(self, datafile:str):
    with open(datafile, 'r') as file:
      headers = ["iID", "sID", "sIteration"] + file.readline().strip().strip(",").split(",")[2:]

      iID = None
      sID = None
      
      for pos, line in enumerate(file.readlines()):
        line = line.strip().strip(",").split(",")
        
        if len(line) == 0 or len(line) != len(headers) - 1: continue
        try:
          if not line[0].split(".")[0].isdigit(): continue
        except: continue
        
        #print(line[:5], line[-5:])

        sample_intstdwv = line[0]
        sample = line[1]
        line[1] = line[1].split(" - ")
        sample_name = line[1][0]
        sample_iteration = line[1][-1]
        data = line[2:]

        self._cur.execute(f"""SELECT MAX("sID") FROM "Samples" WHERE "sName" = ?""", (sample_name,))

        if not (sID := self._cur.fetchone()[0]):
          self._cur.execute("""SELECT MAX("sID") FROM "Samples" """)
          if not (sID := self._cur.fetchone()[0]):
            sID = 1
          else: sID += 1
        
        # Get all tables and check that a table matches headers
        self._cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'Samples' ORDER BY name;""")

        db_tables = [row[0] for row in self._cur.fetchall()]
        table = None
        for table in db_tables:
          self._cur.execute(f"""PRAGMA table_info("{table}")""")

          temp_headers = self._cur.fetchall()

          match = True
          
          if len(temp_headers) != len(headers): match = False
          for head in temp_headers:
            if head[1] not in headers: match = False; break
            
          if match: break
          else: table = None

        if table == None:
          table = f"SampleIterations-{int(time.time())}"
          cols = ', '.join((lambda hs: [f'\"{s.replace('\"','\"\"')}\" FLOAT' for s in hs])(headers[3:]))
          self._cur.execute(f"""CREATE TABLE "{table}" 
                            ("iID" INTEGER NOT NULL,
                            "sID" INTEGER NOT NULL,
                            "sIteration" TEXT,
                            {cols},
                            PRIMARY KEY ("iID", "sID"),
                            FOREIGN KEY ("sID") REFERENCES "Samples"("sID")
                            ); """)
        
        iID = int(sample_iteration)

        #self._cur.execute(f"""SELECT MAX("iID") FROM "{table}" WHERE "sID" = ?""", (sID,))
        #if not (iID := self._cur.fetchone()[0]):
        #  iID = 1
        #else: iID += 1

        row = tuple([iID, sID, sample]+data)
        try:
          if iID == 1:
            self._cur.execute(f"""INSERT INTO "Samples" VALUES ({",".join(["?"]*3)}); """, (sID, sample_name, sample_intstdwv))
          self._cur.execute(f"""INSERT INTO "{table}" VALUES ({",".join(["?"]*len(row))})""", row)
        except sqlite3.Error as e:
          print(f"Failed:{e}")
        
      self._con.commit()
        

class App:

  def __init__(self, root):
    self._variables()

    self._root = root

    self._layout()
  
  def _variables(self):
    self._root = None

    #Style(theme='darkly')

    self._info_icon = ImageTk.PhotoImage(Image.open("info_icon.png").resize((24,24), Image.LANCZOS))

    self._files = {'Database':ttk.StringVar(value="None"), 'DataFile':ttk.StringVar(value="None")}

    self._db = None

    self._database_filename = ttk.StringVar(value="None")
    self._data_filename = ttk.StringVar(value="None")

    self._query_command = ttk.StringVar()
    self._raw_command_output = None

    self._man_header = ttk.StringVar(value="0")
    self._man_upper = ttk.StringVar()
    self._man_lower = ttk.StringVar()

  def _layout(self):
    
    #File Manager Frame

    file_mgr_frame = ttk.Frame(self._root, relief='solid')

    imp_db = ttk.Button(file_mgr_frame, text="Import Database File", command=lambda: self._set_file('Database', self._import_file((("Database", "*.db"),))))
    imp_db.grid(padx=(10,5), pady=(10,5), column=0,row=0, sticky='EW')

    crt_db = ttk.Button(file_mgr_frame, text="Create Database", command=lambda: self._set_file('Database', self._create_file()))
    crt_db.grid(padx=(10,5), pady=(5,10), column=0, row=1, sticky='EW')

    imp_df = ttk.Button(file_mgr_frame, text="Import Datafile", command=lambda: self._set_file('DataFile',self._import_file((("Comma Seperated Values", "*.csv"), ("Any Types", "*")))))
    imp_df.grid(padx=(5,5), pady=(10,5), column=1, row=0, sticky='EW')

    imp_df_p = ttk.Button(file_mgr_frame, text="Standard Parse", command=lambda: self._standard_parse())
    imp_df_p.grid(padx=(5,5), pady=(5,10), column=1, row=1, sticky='EW')

    imp_dp = ttk.Button(file_mgr_frame, text="Direct Parse", command=lambda: self._direct_parse())

    exp_csv = ttk.Button(file_mgr_frame, text="Export Database", command=lambda: self._db._export_all() if self._db is not None else None)
    exp_csv.grid(padx=(5,10), pady=(10,5), column=3, row=0, sticky='EW')

    rmv = ttk.Button(file_mgr_frame, text="Remove Selected", style='TButtonDanger', command=lambda: self._reset_files())
    rmv.grid(padx=(5,10), pady=(5,10), column=3, row=1, sticky='EW')

    ToolTip(imp_db, self._files['Database'].get())
    ToolTip(crt_db, self._files['Database'].get())
    ToolTip(imp_df, self._files['DataFile'].get())

    file_mgr_frame.grid(pady=(0,2), column=0, row=0, sticky='EW')



    #RAW SQL Command Input

    query_frame = ttk.Frame(self._root, relief='solid')
    
    query_title = ttk.Label(query_frame, text="RAW SQL Command Input", font=('Arial',16), padding=5)
    query_title.grid(padx=(10,5), pady=(10,5), column=0, row=0, columnspan=3, sticky='W')

    query_info = ttk.Label(query_frame, image=self._info_icon)
    query_info.grid(padx=(5,5), pady=(10,5), column=3, row=0, sticky='W')

    query_preview = ttk.Button(query_frame, text="Preview Output", command=lambda: self._preview(self._raw_command_output))
    query_preview.grid(padx=(5,10), pady=(10,5), column=4, row=0, sticky='EW')

    query_label = ttk.Label(query_frame, text="SQL Query", style='inverse-secondary', padding=5)
    query_label.grid(padx=(10,5), pady=(5,10), column=0, row=1, sticky='EW')

    query_entrybox = ttk.Entry(query_frame, textvariable=self._query_command)
    query_entrybox.grid(padx=(5,5), pady=(5,10), column=1, columnspan=2, row=1, sticky='EW')

    query_submit = ttk.Button(query_frame, text="Submit", style='TButtonSuccess', command=lambda: self._custom_query())
    query_submit.grid(padx=(5,5), pady=(5,10), column=3, row=1, sticky='EW')

    query_export = ttk.Button(query_frame, text="Export")
    query_export.grid(padx=(5,10), pady=(5,10), column=4, row=1, sticky='EW')

    ToolTip(query_info, 
"""!!!WARNING!!! any SQL commands submitted are immediately commited and can erase data. Make sure you know what you are doing.
Uses a Generic SQL Query and executes upon submit.
E.X. SELECT * FROM {tablename} WHERE "{something}" = '{something}'""")

    query_frame.grid(pady=(2,2), column=0, row=2, sticky='EW')

    #Manual Data Selection Bounding Box

    man_select = ttk.Frame(self._root, relief='solid')

    man_select_title = ttk.Label(man_select, text="Manual Data Selection Bounding Box", font=('Arial',16), padding=5)
    man_select_title.grid(padx=(10,5), pady=(10,5), column=0, row=0, columnspan=2, sticky='W')

    man_select_info = ttk.Label(man_select, image=self._info_icon)
    man_select_info.grid(padx=(5,10), pady=(10,5), column=2, row=0, sticky='W')

    man_select_header_l = ttk.Label(man_select, text="Headers Row Coordinate", style='inverse-secondary', padding=5)
    man_select_header_l.grid(padx=(10,5), pady=(5,5), column=0, row=1, sticky='EW')

    man_select_upper_l = ttk.Label(man_select, text="Upper Left Coordinate", style='inverse-secondary', padding=5)
    man_select_upper_l.grid(padx=(10,5), pady=(5,5), column=0, row=2, sticky='EW')

    man_select_lower_l = ttk.Label(man_select, text="Lower Right Coordinate", style='inverse-secondary', padding=5)
    man_select_lower_l.grid(padx=(10,5), pady=(5,10), column=0, row=3, sticky='EW')

    man_select_header_e = ttk.Entry(man_select, textvariable=self._man_header)
    man_select_header_e.grid(padx=(5,5), pady=(5,5), column=1, row=1)

    man_select_upper_e = ttk.Entry(man_select, textvariable=self._man_upper)
    man_select_upper_e.grid(padx=(5,5), pady=(5,5), column=1, row=2)

    man_select_lower_e = ttk.Entry(man_select, textvariable=self._man_lower)
    man_select_lower_e.grid(padx=(5,5), pady=(5,10), column=1, row=3)

    man_select_preview_h = ttk.Button(man_select, text="Preview Headers")
    man_select_preview_h.grid(padx=(5,10), pady=(5,5), column=2, row=1)

    man_select_preview_c = ttk.Button(man_select, text="Preview Selection")
    man_select_preview_c.grid(padx=(5,10), pady=(5,5), column=2, row=2)

    man_select_submit = ttk.Button(man_select, text="Import", style='TButtonSuccess')
    man_select_submit.grid(padx=(5,10), pady=(5,10), column=2, row=3, sticky='EW')

    ToolTip(man_select_info, 
"""Header row is just the number starting from 0 to n .
E.X. 0 is the first row in the csv.
Takes Coordinates in Excel format. Uses a upper and lower coordinate to form a rectangle selection.
E.X. upper: A2, lower: G8 will give you everything within that range A2:G8 """)

    #man_select.grid(pady=(2,0), column=0, row=3, sticky='EW')

  def _global_refresh(self):
    """
    Globally refreshes variables to make sure displays are up to date.
    """
    #self._update_vars()
    self._load_database()
    #self._load_datafile()

  def _set_file(self, key, value):
    self._files[key].set(value)
    # Old Ver -> self._files.update({key:value})
    self._global_refresh()

  def _import_file(self, extensions:tuple):
    f = filedialog.askopenfile(title="Choose File...", initialdir=os.getcwd(), filetypes=extensions)
    return f.name if f != None else "None"
  
  def _create_file(self):
    return filedialog.asksaveasfilename(title="Save As...", initialdir=os.getcwd(), defaultextension=".db", filetypes=(("Database", "*.db"),))

  def _update_vars(self):
    if self._files['Database'] != None:
      self._database_filename.set(self._files['Database'].name)
    else: self._database_filename.set("None")
    
    if self._files['DataFile'] != None:
      self._data_filename.set(self._files['DataFile'].name)
    else: self._data_filename.set("None")

  def _reset_files(self):
    for key in self._files:
      try: self._files[key].set("None")
      except: pass
    self._files = {'Database':ttk.StringVar(value="None"), 'DataFile':ttk.StringVar(value="None")}
    self._global_refresh()

  def _load_database(self):
    if self._files['Database'].get() != "None":
      self._db = Database(self._files['Database'].get())
  
  def _standard_parse(self):
    
    if (self._files['DataFile'].get() != "None") and (self._db != None):
      if not messagebox.askyesno(title="Auto Import Data Warning", 
                                message=
"""!!WARNING!!
Datafile has to be the same format as the Standard Template
Otherwise Data may be overwritten or not inputted correctly.
Proceed?""",
                                icon='warning'): return
      self._db._auto_parse(self._files['DataFile'].get())

  def _custom_query(self):
    if (self._files['Database'] != None) and (self._db != None):
      if messagebox.askyesno(title="Confirmation", message="Are you sure you want to use a SQL Query?\n(Can be Dangerous for Database)", icon='warning'):
        self._raw_command_output = self._db._raw_command(self._query_command.get())

  def _preview(self, item):
    if item == None: return

    win = ttk.Toplevel(self._root)
    win.title("Preview")
    win.resizable(True, True)

    canvas = ttk.Canvas(win)
    vbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    hbar = ttk.Scrollbar(win, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    vbar.grid(row=0, column=1, sticky="ns")
    hbar.grid(row=1, column=0, sticky="ew")

    inner = ttk.Frame(canvas)
    inner_id = canvas.create_window((0,0), window=inner, anchor="nw")

    for y in range(len(item)):
      ttk.Label(inner, text=y+1).grid(row=y, column=0, sticky='W')
      for x in range(len(item[y])):
        ttk.Label(inner, text=item[y][x]).grid(row=y, column=x+1, sticky='W')

    def _on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner.bind("<Configure>", _on_configure)

    def _on_canvas_resize(event):
        canvas.itemconfig(inner_id, width=event.width)
    canvas.bind("<Configure>", _on_canvas_resize)

    def _on_mousewheel(event):
        # For Windows and Mac (shift for horizontal)
        if event.state & 0x1:  # shift pressed -> horizontal
            canvas.xview_scroll(-1 * int(event.delta / 120), "units")
        else:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel)


root = ttk.Window(themename="darkly")
app = App(root)
root.title("Tephra Glass Trace Database GUI")
root.resizable(False, False)

root.update_idletasks()
w, h = root.winfo_width(), root.winfo_height()
root.minsize(w, h)
#root.geometry(f"{16*30}x{9*30}")

root.mainloop()