from tkinter import *
from tkinter import ttk
from sqlite import *

class Frame_Base(Frame):
    def __init__(self, window):
        Frame.__init__(self, window, width=2000, height=800)
        self.sql = SQLite()
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self._popup_abierto = False

    def crear_popup(self):
        '''abre un popup y modifica el atributo que indica que hay un popup abierto'''
        self._popup_abierto = True
        self.popup = Toplevel()
        self.popup.wm_protocol("WM_DELETE_WINDOW", self.quitar_popup) # si se cierra el popup se llama al método quitar_popup
        self.popup.transient(self) #superpone el popup

    def quitar_popup(self):
        '''elimina el popup abierto e indica que no hay ningún popup abierto'''
        self._popup_abierto = False
        self.popup.destroy()
