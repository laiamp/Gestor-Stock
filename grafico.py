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

    def get_porcentaje(self, dict): #convierte los totales de cada de cada categoría/proveedor del diccionario en porcentajes
        total = sum(dict.values()) #obtengo la suma de todos los totales
        dict = {x: dict[x]/total*100 for x in dict} #cambio cada total por el porcentaje correspondiente
        return dict

    def mostrar(self, fila, columna): #muestra el gráfico en el popup
        canvas = FigureCanvasTkAgg(self.fig, master=self.popup) #interficie entre la Figura de Matplotlib y canvas de Tkinter
        canvas.get_tk_widget().grid(row=fila, column=columna)
