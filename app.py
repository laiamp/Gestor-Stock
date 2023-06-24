from tkinter import*
from tkinter import ttk

import ctypes
from datetime import datetime
import xlsxwriter
from xlsxwriter.workbook import Workbook

#from sqlite import *
from frame_stock import *
from frame_historial import *

class App():
    def __init__(self):
        self.window = Tk() # ventana principal de tkinter
        self.window.title("Gestor de Stock")
        self.window.iconbitmap('pngdiente.ico') # añade un icono a la ventana

        # dimensiones de la ventana
        width, height = 1600, 800
        screen_width=self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width/2)-(width/2)
        y = (screen_height/2)-(height/2)
        self.window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.window.resizable(False, False)

        self.frame_stock = Frame_Stock(self.window) #crea el frame del stock
        self.frame_stock.grid(row=1, column=1, padx=10, pady=10)

        self.boton_ir_historial = ttk.Button(self.window, text="Ir a historial", command=self.ir_historial)
        self.boton_ir_historial.grid(row=0,column=0)

        self.text = StringVar()
        self.text.set("STOCK")
        self.label_titulo = Label(self.window, textvariable=self.text, height=1)
        self.label_titulo.grid(row=0, column=1, sticky="ew")
        self.label_titulo.config(bg="gray75", font=("Verdana",12))


    def ir_historial(self):
        '''destruye el frame stock y crea el frame historial'''

        self.frame_stock.destroy() # destruye el frame antiguo
        self.boton_ir_historial.destroy() # destruye el botón

        self.text.set("HISTORIAL") # cambia el título del frame
        self.frame_historial = Frame_Historial(self.window) # crea el frame historial
        self.frame_historial.grid(row=1, column=1, padx=10, pady=10)

        self.boton_ir_stock = ttk.Button(self.window, width=11, text = "Ir a stock", command=self.ir_stock)
        self.boton_ir_stock.grid(row=0, column=0)


    def ir_stock(self):
        '''destruye el frame historial y crea el frame stock'''
        self.frame_historial.destroy()
        self.boton_ir_stock.destroy()

        self.text.set("STOCK")
        self.frame_stock = Frame_Stock(self.window)
        self.frame_stock.grid(row=1,column=1, padx=10, pady=10)

        self.boton_ir_historial = ttk.Button(self.window, width=11, text = "Ir a historial", command=self.ir_historial)
        self.boton_ir_historial.grid(row=0, column=0)


if __name__=="__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1) #permite mantener la misma resolución al generar los gráficos
    app = App()
    app.window.mainloop()
