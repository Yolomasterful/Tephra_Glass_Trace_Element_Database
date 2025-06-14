import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style, Frame, Button

class App:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='darkly')
        
        # Create container frame that will hold our sections
        self.container = Frame(root)
        self.container.pack(fill='both', expand=True)
        
        # Create navigation buttons
        nav_frame = Frame(root)
        nav_frame.pack(fill='x', pady=10)
        
        ttk.Button(nav_frame, text="Show Section 1", 
               command=lambda: self.show_section(self.section1),
               bootstyle="primary").pack(side='left', padx=5)
               
        ttk.Button(nav_frame, text="Show Section 2", 
               command=lambda: self.show_section(self.section2),
               bootstyle="success").pack(side='left', padx=5)
        
        # Create sections (but don't show them yet)
        self.create_sections()
        
        # Show first section by default
        self.show_section(self.section1)
    
    def create_sections(self):
        """Create all the sections/frames we might want to show"""
        # Section 1
        self.section1 = Frame(self.container)
        ttk.Label(self.section1, text="This is Section 1", bootstyle="info").pack(pady=20)
        ttk.Button(self.section1, text="Button in Section 1", bootstyle="warning").pack()
        
        # Section 2
        self.section2 = Frame(self.container)
        ttk.Label(self.section2, text="This is Section 2", bootstyle="danger").pack(pady=20)
        ttk.Entry(self.section2, bootstyle="primary").pack()
    
    def show_section(self, section):
        """Hide all sections, then show the requested one"""
        # Hide all sections
        for child in self.container.winfo_children():
            child.pack_forget()
        
        # Show the requested section
        section.pack(fill='both', expand=True)

# Create and run the application
root = tk.Tk()
app = App(root)
root.geometry("400x300")
root.title("Section Switcher")
root.mainloop()