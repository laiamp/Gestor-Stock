import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Grafico():
    def __init__(self, popup, dict, titulo):
        dict_porcentaje = self.get_porcentaje(dict)

        self.popup = popup
        self.labels = dict_porcentaje.keys()
        self.sizes = dict_porcentaje.values()

        self.fig = plt.figure(figsize=(5,3))
        plt.title(titulo, fontweight='bold')
        plt.pie(self.sizes, startangle=90)
        plt.legend(self.labels, loc="best")
        plt.axis('equal')


    def get_porcentaje(self, dict):
        '''convierte los totales de cada de cada categoría/proveedor del diccionario en porcentajes'''
        total = sum(dict.values())
        return {x: dict[x]/total*100 for x in dict}


    def mostrar(self, fila, columna):
        '''muestra el gráfico en el popup'''
        canvas = FigureCanvasTkAgg(self.fig, master=self.popup) #interficie entre la Figura de Matplotlib y canvas de Tkinter
        canvas.get_tk_widget().grid(row=fila, column=columna)
