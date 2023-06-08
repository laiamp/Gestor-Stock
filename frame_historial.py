class Frame_Historial(Frame_Base):
    def __init__(self, window):
        super().__init__(window)
        self.crear_tabla()
        self.rellenar_tabla(self.sql.get_tabla("historial"))
        self.widgets()

    def widgets(self): #crea los objetos del frame
        self.c_mes = ttk.Combobox(self, width=20, values = self.sql.get_meses(), state="readonly")
        self.c_proveedor = ttk.Combobox(self, width=20, values = self.sql.get_tabla("proveedores"), state="readonly")
        self.c_categoria = ttk.Combobox(self, width=20, values = self.sql.get_tabla("categorias"), state="readonly")
        boton_clear_mes = ttk.Button(self, width=5, text="Clear", command = self.clear_mes)
        boton_clear_proveedor = ttk.Button(self, width=5, text="Clear", command = self.clear_proveedor)
        boton_clear_categoria = ttk.Button(self, width=5, text="Clear", command = self.clear_categoria)

        boton_update = ttk.Button(self, text="Actualizar", command = self.filtrar)
        boton_grafico = ttk.Button(self, text="Ver gráficos", command = self.popup_grafico)
        boton_descargar = ttk.Button(self, text="Descargar", command = self.popup_descargar)

        label_mes = Label(self, text="Mes", width= 15, anchor=E).grid(row=6, column=1)
        label_proveedor = Label(self, text="Proveedor", width=15, anchor=E).grid(row=7, column=1)
        label_categoria = Label(self, text="Categoría", width=15, anchor=E).grid(row=8, column=1)

        self.c_mes.grid(row=6, column=2)
        boton_clear_mes.grid(row=6, column=3)
        self.c_proveedor.grid(row=7, column=2)
        boton_clear_proveedor.grid(row=7, column=3)
        self.c_categoria.grid(row=8, column=2)
        boton_clear_categoria.grid(row=8, column=3)

        boton_update.grid(row=6, column=4)
        boton_grafico.grid(row=6, column=5)
        boton_descargar.grid(row=6, column=6)

    def crear_tabla(self): #crea una tabla de historial vacía
        self.tabla_historial = ttk.Treeview(self, height = 18, selectmode=BROWSE, show="headings")

        #columnas
        self.tabla_historial['columns'] = ("Fecha", "Mes", "Referencia", "Nombre", "Proveedor", "Precio_Unidad", "Cantidad", "Descuento", "Total", "Categoría")
        self.tabla_historial.column('Fecha', anchor = CENTER, width = 105)
        self.tabla_historial.column('Mes', anchor = CENTER, width = 80)
        self.tabla_historial.column('Referencia', anchor = CENTER, width = 140)
        self.tabla_historial.column('Nombre', anchor = CENTER, width = 300)
        self.tabla_historial.column('Proveedor', anchor = CENTER, width = 170)
        self.tabla_historial.column('Precio_Unidad', anchor = CENTER, width = 85)
        self.tabla_historial.column('Cantidad', anchor = CENTER, width = 85)
        self.tabla_historial.column('Descuento', anchor = CENTER, width = 95)
        self.tabla_historial.column('Total', anchor = CENTER, width = 90)
        self.tabla_historial.column('Categoría', anchor = CENTER, width = 140)

        #títulos de las columnas
        self.tabla_historial.heading("Fecha", text = "Fecha", anchor = CENTER)
        self.tabla_historial.heading("Mes", text = "Mes", anchor = CENTER)
        self.tabla_historial.heading("Referencia", text = "Referencia", anchor = CENTER)
        self.tabla_historial.heading("Nombre", text = "Nombre", anchor = CENTER)
        self.tabla_historial.heading("Proveedor", text = "Proveedor", anchor = CENTER)
        self.tabla_historial.heading("Precio_Unidad", text = "Precio/u", anchor = CENTER)
        self.tabla_historial.heading("Cantidad", text = "Cantidad comprada", anchor = CENTER)
        self.tabla_historial.heading("Descuento", text = "Descuento", anchor = CENTER)
        self.tabla_historial.heading("Total", text = "Total", anchor = CENTER)
        self.tabla_historial.heading("Categoría", text = "Categoría", anchor = CENTER)

        self.tabla_historial.grid(row=0, column=0, rowspan=5, columnspan=10, padx=5, pady = 10, sticky=W)
        self.tabla_historial.bind("<Double-1>", self.popup_tabla)

        #barra de scroll
        self.tabla_scroll = Scrollbar(self, orient="vertical")
        self.tabla_scroll.grid(row=0, column=16, rowspan=5, sticky='nse')
        self.tabla_historial.configure(yscrollcommand=self.tabla_scroll.set)
        self.tabla_scroll.config(command=self.tabla_historial.yview)

    def rellenar_tabla(self, rows): #rellena tabla historial con contenido de la base de datos
        #personaliza la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview', rowheight=30)

        for i, row in enumerate(rows): #itera sobre todas las filas
            self.tabla_historial.insert("", END, values=row, tag=i) #añade una fila a la tabla
            if i % 2 == 0: #las filas pares serán de otro color
                self.tabla_historial.tag_configure(i, background='white')

    def actualizar_tabla(self): #destruye la tabla y la vuelve a crear
        self.tabla_historial.destroy()
        self.crear_tabla()
        self.rellenar_tabla(self.sql.get_tabla("historial"))

    def popup_tabla(self, e): #como se llama al método mediante un event binding (doble click) hace falta pasar un parámetro extra (e)
        try:
            fecha = self.tabla_historial.item(self.tabla_historial.focus(), "values")[0]
            nombre = self.tabla_historial.item(self.tabla_historial.focus(), "values")[3]

            if self._popup_abierto == False: #comprueba que no haya ningún popup abierto
                self.crear_popup()
                self.popup.title("Opciones")

                #centrar popup
                width, height = 320, 80 #dimensiones popup
                x = (self.screen_width/2)-(width/2)
                y = (self.screen_height/2)-(height/2)
                self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

                boton_editar = ttk.Button(self.popup, text='Editar', width=10, command=lambda: self.popup_editar(fecha, nombre))
                boton_borrar = ttk.Button(self.popup, text='Eliminar', width=10, command=lambda: self.borrar(fecha, nombre))

                boton_editar.grid(row=0, column=0, pady=10, padx=20)
                boton_borrar.grid(row=0, column=1, pady=10, padx=20)

        except IndexError:
            pass

    def popup_editar(self, fecha, nombre): #abre un popup para editar descuento, precio y/o proveedor
        self.popup.destroy()
        self.crear_popup()
        self.popup.title("Editar producto")

        width, height= 660, 230
        x = (self.screen_width/2)-(width/2)
        y = (self.screen_height/2)-(height/2)
        self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        label_descuento = Label(self.popup, text="Descuento").grid(row=0, column=0, pady=10, padx=10)
        label_precio = Label(self.popup, text="Precio/unidad").grid(row=1, column=0, pady=10, padx=10)
        label_proveedor = Label(self.popup, text="Proveedor").grid(row=2, column=0, pady=10, padx=10)

        descuento_antiguo = self.sql.get_elemento_tabla("historial", fecha, "descuento")
        precio_antiguo = self.sql.get_elemento_tabla("historial", fecha, "precio_unidad")
        proveedor_antiguo = self.sql.get_elemento_tabla("historial", fecha, "proveedor")

        e_descuento_antiguo = Entry(self.popup)
        e_descuento_antiguo.insert(END, descuento_antiguo)
        e_descuento_antiguo.config(state=DISABLED)
        e_descuento_antiguo.grid(row=0, column=1, pady=10, padx=10)

        e_precio_antiguo = Entry(self.popup)
        e_precio_antiguo.insert(END, precio_antiguo)
        e_precio_antiguo.config(state=DISABLED)
        e_precio_antiguo.grid(row=1, column=1, pady=10, padx=10)

        e_proveedor_antiguo = Entry(self.popup)
        e_proveedor_antiguo.insert(END, proveedor_antiguo)
        e_proveedor_antiguo.config(state=DISABLED)
        e_proveedor_antiguo.grid(row=2, column=1, pady=10, padx=10)

        e_descuento_nuevo = Entry(self.popup)
        e_descuento_nuevo.grid(row=0, column=2, pady=10, padx=10)

        e_precio_nuevo = Entry(self.popup)
        e_precio_nuevo.grid(row=1, column=2, pady=10, padx=10)

        c_proveedor_nuevo = ttk.Combobox(self.popup, width=18, values=self.sql.get_tabla("proveedores"), state="readonly")
        c_proveedor_nuevo.grid(row=2, column=2)

        boton_confirmar = ttk.Button(self.popup, text="Confirmar", command = lambda: self.input_editar(fecha, e_descuento_nuevo.get(), e_precio_nuevo.get(), c_proveedor_nuevo.get()))
        boton_confirmar.grid(row=3, column=1)

    def input_editar(self, fecha, descuento, precio, proveedor): #modifica los valores en la base de datos historial y si es necesario recalcula el total
        if len(proveedor) != 0 or len(precio) != 0 or len(descuento) != 0:
            if len(descuento) == 0 and len(precio) == 0: #solo se ha modificado proveedor
                self.sql.set_valor_producto(nombre_tabla="historial", columna="proveedor", id=fecha, valor=proveedor)
            else:
                compra = [x for x in self.sql.get_editar(id=fecha)[0]] #proveedor, precio_unidad, descuento, total, cantidad

                if len(proveedor) != 0:
                    compra[0] = proveedor

                if len(precio) != 0:
                    try:
                        precio = float(precio)
                        compra[1] = precio
                        calcular_total = True
                    except ValueError:
                        messagebox.showwarning(message="Asegúrese de haber introducido números en PRECIO UNIDAD", title="Error en la entrada")
                else:
                    precio = compra[1]

                if len(descuento) != 0:
                    try:
                        descuento = float(descuento)
                        compra[2] = descuento
                        calcular_total = True
                    except ValueError:
                        messagebox.showwarning(message="Asegúrese de haber introducido números en DESCUENTO", title="Error en la entrada")
                else:
                    descuento = compra[2]

                cantidad = compra[-1]
                compra[-2] = cantidad*precio*(1-descuento/100)

                compra.pop() #no se editará el parámetro cantidad
                compra = tuple(compra)
                self.sql.editar_from_historial(fecha, compra)

            self.quitar_popup()
            self.actualizar_tabla()
        else:
            messagebox.showwarning(message="No se ha introducido ningún valor", title="Error en la entrada")

    def clear_mes(self): #destruye el combobox mes y lo vuelve a crear para limpiar su contenido
        self.c_mes.destroy()
        self.c_mes = ttk.Combobox(self, width=20, values = self.sql.get_meses(), state="readonly")
        self.c_mes.grid(row=6, column=2)

    def clear_proveedor(self): #destruye el combobox proveedor y lo vuelve a crear para limpiar su contenido
        self.c_proveedor.destroy()
        self.c_proveedor = ttk.Combobox(self, width=20, values = self.sql.get_tabla("proveedores"), state="readonly")
        self.c_proveedor.grid(row=7, column=2)

    def clear_categoria(self): #destruye el combobox categoría y lo vuelve a crear para limpiar su contenido
        self.c_categoria.destroy()
        self.c_categoria = ttk.Combobox(self, width=20, values = self.sql.get_tabla("categorias"), state="readonly")
        self.c_categoria.grid(row=8, column=2)

    def borrar(self, fecha, nombre): #elimina definitivamente una compra de la base de datos y de la tabla según su fecha
        if messagebox.askyesno(message= f"¿Desea eliminar {nombre} permanentemente del historial?", title="Advertencia") == True:
            self.sql.borrar_elemento(nombre_tabla="historial", columna_id="fecha", id=fecha)
            self.actualizar_tabla()
            self.quitar_popup()

    def filtrar(self): #permite filtrar las compras de la tabla según mes, categoría y/o proveedor
        self.tabla_historial.destroy()
        self.crear_tabla()
        mes = self.c_mes.get()
        categoria = self.c_categoria.get()
        proveedor = self.c_proveedor.get()

        if len(mes) != 0 and len(categoria) != 0 and len(proveedor) != 0: #mes categoria proveedor
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="mes", columna2="categoria", columna3="proveedor", criterio1=mes, criterio2=categoria, criterio3=proveedor)

        elif len(mes) != 0 and len(categoria) != 0 and len(proveedor) == 0: #mes categoria
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="mes", columna2="categoria", criterio1=mes, criterio2=categoria)

        elif len(mes) != 0 and len(categoria) == 0 and len(proveedor) != 0: #mes proveedor
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="mes", columna2="proveedor", criterio1=mes, criterio2=proveedor)

        elif len(mes) != 0 and len(categoria) == 0 and len(proveedor) == 0: #mes
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="mes", criterio1=mes)

        elif len(mes) == 0 and len(categoria) != 0 and len(proveedor) != 0: #categoria proveedor
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="categoria", columna2="proveedor", criterio1=categoria, criterio2=proveedor)

        elif len(mes) == 0 and len(categoria) == 0 and len(proveedor) != 0: #proveedor
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="proveedor", criterio1=proveedor)

        elif len(mes) == 0 and len(categoria) != 0 and len(proveedor) == 0: #categoria
            rows = self.sql.filtrar(nombre_tabla="historial", columna1="mes", criterio1=mes)

        else:
            rows = self.sql.get_tabla("historial")

        self.rellenar_tabla(rows)

    def popup_grafico(self): #abre popup para seleccionar mes y mostrar su gráfico
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title("Gráficos")

            width, height = 400, 150
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            mes_grafico = ttk.Combobox(self.popup, values = self.sql.get_meses(), state="readonly")
            mes_grafico.grid(row=0, column=0, pady=10, padx=10)
            boton_crear =  ttk.Button(self.popup, text = "Crear gráfico", command=lambda:self.ver_grafico(mes_grafico.get()))
            boton_crear.grid(row=0, column=1, pady=10, padx=10)

    def ver_grafico(self, mes):
        if len(mes) != 0:
            self.quitar_popup()
            dict_total_categorias = self.sql.get_total(mes, "categoria")
            dict_total_proveedores = self.sql.get_total(mes, "proveedor")

            self.crear_popup()
            width, height = 1450, 450
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            grafico_categorias = Grafico(self.popup, dict_total_categorias, "CATEGORÍAS")
            grafico_proveedores = Grafico(self.popup, dict_total_proveedores, "PROVEEDORES")

            grafico_categorias.mostrar(0, 0)
            grafico_proveedores.mostrar(0, 1)

        else:
            messagebox.showwarning(message="No se ha seleccionado ningún mes", title="Error en la entrada")

    def popup_descargar(self): #popup para seleccionar el mes a descargar
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title("Descarga")

            width, height = 400, 100
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            mes_descarga = ttk.Combobox(self.popup, values = self.sql.get_meses(), state="readonly")
            mes_descarga.grid(row=0, column=0, pady=10, padx=10)
            boton_descargar =  ttk.Button(self.popup, text = "Descargar", command=lambda:self.descargar_excel(mes_descarga.get()))
            boton_descargar.grid(row=0, column=1, pady=10, padx=10)

    def descargar_excel(self, id_mes): #descarga excel con las compras del mes de la base de datos (historial)
        if len(id_mes) != 0: #comprueba que se haya seleccionado algún mes
            mes = id_mes[0:2]
            año = id_mes[3:]

            try:
                workbook = Workbook(f"reporte_{mes}_{año}.xlsx") #crea el archivo en la carpeta  que contiene el programa
                worksheet = workbook.add_worksheet() #añade una hoja de cálculo
                datos = self.sql.get_descarga(id_mes) #obtiene los datos para la descarga
                columnas = ["FECHA", "REFERENCIA", "NOMBRE", "PROVEEDOR", "PRECIO/UNIDAD", "CANTIDAD", "DESCUENTO", "TOTAL", "CATEGORÍA"] #nombre columnas

                for j, titulo in enumerate(columnas): #itera sobre los nombres de las columnas
                    worksheet.write(0, j, titulo) #fila 0, columna = j y nombre correspondiente

                for i, row in enumerate(datos): #itera sobre filas de la tabla de excel
                    if i > 0 : #la fila 0 ya está ocupada por los nombres de las columnas
                        for j, valor in enumerate(row): #itera sobre las columnas
                            worksheet.write(i, j, valor) #i=fila, j=columnas, valor
                workbook.close()
                self.quitar_popup()

            except (PermissionError, xlsxwriter.exceptions.FileCreateError) as e: #si el archivo está en uso aparecerán estos dos errores
                messagebox.showwarning(message=f"El archivo reporte_{mes}_{año}.xlsx está abierto. Ciérrelo y vuelva a intentarlo.", title="Advertencia")
        else:
            messagebox.showwarning(message="No se ha seleccionado ningún mes", title="Error en la entrada")
