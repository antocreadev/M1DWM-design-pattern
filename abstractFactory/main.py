import platform
import tkinter as tk
from abc import ABC, abstractmethod

# ========== ABSTRACT FACTORY ==========
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self, master):
        pass

    @abstractmethod
    def create_menu(self, master):
        pass
    
    @abstractmethod
    def create_form(self, master):
        pass

# ========== CONCRETE FACTORIES ==========
class WinFactory(GUIFactory):
    def create_button(self, master):
        return WinButton(master)

    def create_menu(self, master):
        return WinMenu(master)
        
    def create_form(self, master):
        return WinForm(master)

class MacFactory(GUIFactory): 
    def create_button(self, master):
        return MacButton(master)

    def create_menu(self, master):
        return MacMenu(master)
        
    def create_form(self, master):
        return MacForm(master)

class LinuxFactory(GUIFactory): 
    def create_button(self, master):
        return LinuxButton(master)

    def create_menu(self, master):
        return LinuxMenu(master)
        
    def create_form(self, master):
        return LinuxForm(master)

# ========== ABSTRACT PRODUCTS ==========
class Button(ABC):
    def __init__(self, master):
        self.master = master

    @abstractmethod
    def render(self):
        pass

class Menu(ABC):
    def __init__(self, master):
        self.master = master

    @abstractmethod
    def render(self):
        pass
        
class Form(ABC):
    def __init__(self, master):
        self.master = master
        
    @abstractmethod
    def render(self):
        pass

# ========== CONCRETE PRODUCTS ==========
class WinButton(Button):
    def render(self):
        btn = tk.Button(self.master, text="Cliquez-moi", bg="lightblue", 
                      relief="raised", borderwidth=2)
        btn.pack(pady=10)
        return btn

class MacButton(Button):
    def render(self):
        btn = tk.Button(self.master, text="Cliquez-moi", bg="white", 
                      relief="flat", borderwidth=1)
        btn.pack(pady=10)
        return btn

class LinuxButton(Button):
    def render(self):
        btn = tk.Button(self.master, text="Cliquez-moi", bg="gray90", 
                      relief="ridge", borderwidth=1)
        btn.pack(pady=10)
        return btn

class WinMenu(Menu):
    def render(self):
        menu = tk.Menu(self.master)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Nouveau", command=lambda: print("Fonction appelée"))
        file_menu.add_command(label="Ouvrir", command=lambda: print("Fonction appelée"))
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.master.quit)
        menu.add_cascade(label="Fichier", menu=file_menu)
        self.master.config(menu=menu)
        return menu

class MacMenu(Menu):
    def render(self):
        menu = tk.Menu(self.master)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Nouveau", command=lambda: print("Fonction appelée"))
        file_menu.add_command(label="Ouvrir", command=lambda: print("Fonction appelée"))
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.master.quit)
        menu.add_cascade(label="Fichier", menu=file_menu)
        self.master.config(menu=menu)
        return menu

class LinuxMenu(Menu):
    def render(self):
        menu = tk.Menu(self.master)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Nouveau", command=lambda: print("Fonction appelée"))
        file_menu.add_command(label="Ouvrir", command=lambda: print("Fonction appelée"))
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.master.quit)
        menu.add_cascade(label="Fichier", menu=file_menu)
        self.master.config(menu=menu)
        return menu

class WinForm(Form):
    def render(self):
        form_frame = tk.Frame(self.master, relief="raised", borderwidth=2)
        tk.Label(form_frame, text="Nom:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(form_frame).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(form_frame).grid(row=1, column=1, padx=5, pady=5)
        form_frame.pack(padx=10, pady=10)
        return form_frame

class MacForm(Form):
    def render(self):
        form_frame = tk.Frame(self.master, relief="flat", borderwidth=1)
        tk.Label(form_frame, text="Nom:").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        tk.Entry(form_frame).grid(row=0, column=1, padx=8, pady=8)
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=8, pady=8)
        tk.Entry(form_frame).grid(row=1, column=1, padx=8, pady=8)
        form_frame.pack(padx=15, pady=15)
        return form_frame

class LinuxForm(Form):
    def render(self):
        form_frame = tk.Frame(self.master, relief="ridge", borderwidth=1)
        tk.Label(form_frame, text="Nom:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        tk.Entry(form_frame).grid(row=0, column=1, padx=6, pady=6)
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        tk.Entry(form_frame).grid(row=1, column=1, padx=6, pady=6)
        form_frame.pack(padx=12, pady=12)
        return form_frame

# ========== APPLICATION ==========
class Application:
    def __init__(self, master):
        self.master = master
        self.factory = Application.get_factory()
        self.setup_ui()

    @staticmethod
    def get_factory():
        sys_type = platform.system()
        if sys_type == "Windows":
            return WinFactory()
        elif sys_type == "Darwin":
            return MacFactory()
        else:  # Linux ou autre
            return LinuxFactory()
        
    def setup_ui(self):
        # Création des composants pour le système actuel
        self.menu = self.factory.create_menu(self.master)
        self.menu.render()
        
        self.button = self.factory.create_button(self.master)
        self.button.render()
        
        self.form = self.factory.create_form(self.master)
        self.form.render()

# ========== CLIENT CODE ==========
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interface adaptative")
    app = Application(root)
    root.mainloop()