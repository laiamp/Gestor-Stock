from frame_base import *

class Frame_Stock(Frame_Base):
    def __init__(self, window): #constructor
        super().__init__(window)
        self.widgets()
        self.crear_tabla()
        self.rellenar_tabla(self.sql.get_tabla("stock"))

    def widgets(self):
        '''crea todos los objetos del frame'''
        boton_nuevo_proveedor = ttk.Button(self, text="Añadir proveedor", width= 15, command=lambda: self.popup_input_categoria_proveedor("proveedores", "proveedor")).grid(row = 1, column = 0, columnspan=2, pady=5)
        boton_nueva_categoria = ttk.Button(self, text="Añadir categoría", width= 15, command=lambda: self.popup_input_categoria_proveedor("categorias", "categoria")).grid(row = 1, column=2, columnspan=2, pady=5, padx=10)

        boton_editar_proveedor = ttk.Button(self, text="Editar proveedor", width=15, command=lambda:self.popup_editar_categoria_proveedor("proveedores", "proveedor", self.sql.get_tabla("proveedores"))).grid(row=2, column=0, columnspan=2, pady=5)
        boton_editar_categoria = ttk.Button(self, text="Editar categoría", width=15, command=lambda:self.popup_editar_categoria_proveedor("categorias", "categoria", self.sql.get_tabla("categorias"))).grid(row=2, column=2, columnspan=2, pady=5)

        boton_borrar_proveedor = ttk.Button(self, text="Borrar proveedor", width=15, command=lambda:self.popup_borrar_categoria_proveedor("proveedores", "proveedor")).grid(row=3, column=0, columnspan=2, pady=5)
        boton_borrar_categoria = ttk.Button(self, text="Borrar categoría", width=15, command=lambda:self.popup_borrar_categoria_proveedor("categorias", "categoria")).grid(row=3, column=2, columnspan=2, pady=5)

        boton_anadir = ttk.Button(self, text='Añadir producto', width=17, command= self.popup_referencia).grid(row=4, column=0, columnspan=4, pady=30)

        label_categoria = Label(self, text="Filtrar categoría", width=14, anchor=W).grid(row=5, column=0, sticky="s")
        label_estatus = Label(self, text="Filtrar estatus", width=14, anchor=W).grid(row=7, column=0, sticky="s")

        self.seleccionar_categoria = ttk.Combobox(self, values=self.sql.get_tabla("categorias"), width=25, state="readonly")
        self.seleccionar_estatus = ttk.Combobox(self, values=("OK", "FALTA", "AGOTADO"), width=25, state="readonly")

        self.seleccionar_categoria.grid(row=6, column=0, columnspan=3)
        self.seleccionar_estatus.grid(row=8, column=0, columnspan=3)
        boton_clear_categoria = ttk.Button(self, text="Clear", width=5, command = self.clear_categoria)
        boton_clear_estatus = ttk.Button(self, text="Clear", width=5, command = self.clear_estatus)
        boton_update = ttk.Button(self, text="Actualizar", command = lambda: self.filtrar(self.seleccionar_categoria.get(), self.seleccionar_estatus.get()))

        boton_clear_categoria.grid(row=6, column=3)
        boton_clear_estatus.grid(row=8, column=3)
        boton_update.grid(row=9, column=0, columnspan=3, pady=5, padx=10)


    def crear_tabla(self):
        '''crea una tabla de stock vacía'''

        self.tabla_stock = ttk.Treeview(self, height = 20, selectmode=BROWSE, show="headings")
        self.tabla_stock['columns'] = ("Referencia", "Nombre", "Cantidad", "Categoría", "Estatus") #columnas de la tabla

        self.tabla_stock.column('Referencia', anchor = CENTER, width = 150) #configuración de las columnas
        self.tabla_stock.column('Nombre', anchor = CENTER, width = 360)
        self.tabla_stock.column('Cantidad', anchor = CENTER, width =120)
        self.tabla_stock.column('Categoría', anchor = CENTER, width = 160)
        self.tabla_stock.column('Estatus', anchor = CENTER, width = 100)

        self.tabla_stock.heading("Referencia", text = "Referencia", anchor = CENTER) #título de las columnas
        self.tabla_stock.heading("Nombre", text = "Nombre", anchor = CENTER)
        self.tabla_stock.heading("Cantidad", text = "Cantidad", anchor = CENTER)
        self.tabla_stock.heading("Categoría", text = "Categoría", anchor = CENTER)
        self.tabla_stock.heading("Estatus", text = "Estatus", anchor = CENTER)

        self.tabla_stock.grid(row=0, column=4, rowspan=10, columnspan=10, pady = 10, padx=10, sticky=E)
        self.tabla_stock.bind("<Double-1>", self.popup_tabla) #al hacer doble click, el método self.popup_tabla es llamado

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background='lightblue')
        style.configure('TButton', background='gray90')
        style.configure('Treeview', rowheight=30)


        #barra deslizante
        self.tabla_scroll = Scrollbar(self, orient="vertical")
        self.tabla_scroll.grid(row=0, column=16, rowspan=15, sticky='nse')

        self.tabla_stock.configure(yscrollcommand=self.tabla_scroll.set)
        self.tabla_scroll.config(command=self.tabla_stock.yview)

    def rellenar_tabla(self, rows):
        '''rellena tabla stock con contenido de la base de datos'''
        for i, row in enumerate(rows):
            self.tabla_stock.insert("", END, values=row, tag=i) #se añade una fila a la tabla
            if i % 2 == 0: #aplica un color distinto a las filas pares, de modo que se alterna el color de las tabla
                self.tabla_stock.tag_configure(i, background='white')

    def actualizar_tabla(self):
        '''destruye la tabla y la vuelve a crear'''
        self.tabla_stock.destroy()
        self.crear_tabla()
        self.rellenar_tabla(self.sql.get_tabla("stock"))

    def filtrar(self, categoria, estatus):
        '''permite filtrar los productos de la tabla según categoría y estatus'''
        self.tabla_stock.destroy()
        self.crear_tabla()

        if len(categoria) != 0 and len(estatus) != 0: #categoria estatus
            rows = self.sql.filtrar(nombre_tabla="stock", columna1="categoria", criterio1=categoria, columna2="estatus", criterio2=estatus)

        elif len(categoria) != 0 and len(estatus) == 0: #categoria
            rows = self.sql.filtrar(nombre_tabla="stock", columna1="categoria", criterio1=categoria)

        elif len(categoria) == 0 and len(estatus) != 0: #estatus
            rows = self.sql.filtrar(nombre_tabla="stock", columna1="estatus", criterio1=estatus)

        else:
            rows = self.sql.get_tabla("stock") #ningún filtro aplicado, se mostrarán todos los productos

        self.rellenar_tabla(rows) #se rellena la tabla con los productos seleccionados

    def clear_categoria(self):
        '''destruye el combobox categoría y lo vuelve a crear para limpiar su contenido'''
        self.seleccionar_categoria.destroy()
        self.seleccionar_categoria = ttk.Combobox(self, width=25, values=self.sql.get_tabla("categorias"), state="readonly")
        self.seleccionar_categoria.grid(row=6, column=0, columnspan=3)

    def clear_estatus(self):
        '''destruye el combobox estatus y lo vuelve a crear para limpiar su contenido'''
        self.seleccionar_estatus.destroy()
        self.seleccionar_estatus = ttk.Combobox(self, width=25, values=("OK", "FALTA", "AGOTADO"), state="readonly")
        self.seleccionar_estatus.grid(row=8, column=0, columnspan=3)

    def popup_tabla(self, e):
        '''abre un popup al hacer doble click sobre un elemento de la tabla. Botón para opciones gastar, reponer, editar y borrar
            dado que se llama al método mediante un event binding (doble click) hace falta pasar un parámetro extra (e)
        '''

        try:
            referencia = self.tabla_stock.item(self.tabla_stock.focus(), "values")[0]
            nombre = self.tabla_stock.item(self.tabla_stock.focus(), "values")[1]

            if self._popup_abierto == False: #comprueba que no haya ningún popup abierto
                self.crear_popup()
                self.popup.title("Opciones")

                #centrar popup
                width, height = 590, 80 #dimensiones popup
                x = (self.screen_width/2)-(width/2)
                y = (self.screen_height/2)-(height/2)
                self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

                boton_gastar = ttk.Button(self.popup, text="Gastar", command=lambda: self.popup_gastar(referencia))
                boton_reponer = ttk.Button(self.popup, text="Reponer", command=lambda: self.popup_reponer(referencia))
                boton_editar = ttk.Button(self.popup, text='Editar', width=10, command=lambda: self.popup_editar(referencia, nombre))
                boton_borrar = ttk.Button(self.popup, text='Eliminar', width=10, command=lambda: self.borrar_producto(referencia, nombre))

                boton_gastar.grid(row=0, column=0, pady=10, padx=20)
                boton_reponer.grid(row=0, column=1, pady=10)
                boton_editar.grid(row=0, column=2, pady=10, padx=20)
                boton_borrar.grid(row=0, column=3, pady=10)

        except IndexError:
            pass

    def borrar_producto(self, referencia, nombre):
        '''elimina definitivamente un producto de la base de datos y de la tabla según su referencia'''
        if messagebox.askyesno(message= f"¿Desea eliminar {nombre} permanentemente de Stock?", title="Advertencia") == True:
            self.sql.borrar_elemento(nombre_tabla="stock", columna_id="referencia", id=referencia)
            self.actualizar_tabla()
            self.quitar_popup()

    def popup_referencia(self):
        '''abre un popup para introducir una referencia'''
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title("Referencia")

            width, height = 400, 150
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            label_referencia = Label(self.popup, text = "Referencia").grid(row = 0, column = 0, pady=10, padx=10)
            e_referencia = Entry(self.popup)
            e_referencia.grid(row = 0, column = 1, pady = 5)
            e_referencia.focus()
            e_referencia.bind("<Return>", lambda event: self.input_referencia(e_referencia.get()))

            boton_enviar = ttk.Button(self.popup, text = "Confirmar", command = lambda:self.input_referencia(e_referencia.get()))
            boton_enviar.grid(row = 1, column = 1, pady = 5)

    def input_referencia(self, referencia):
        '''evalúa la referencia introducida y abre el popup que corresponda'''
        if len(referencia) != 0:
            if self.sql.existe("stock", "referencia", referencia) == True: #existe un producto con esa referencia
                self.quitar_popup()
                self.popup_reponer(referencia)
            else: #producto nuevo
                self.quitar_popup()
                self.popup_stock(referencia)
        else:
            messagebox.showwarning(message="No se ha introducido ninguna referencia", title="Error en la entrada")

    def popup_reponer(self, referencia, nombre=None):
        '''popup para introducir datos del producto a reponer'''
        self.popup.destroy()
        self.crear_popup()
        self.popup.title("Reponer producto")

        width, height = 400, 330
        x = (self.screen_width/2)-(width/2)
        y = (self.screen_height/2)-(height/2)
        self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        label_nombre = Label(self.popup, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        label_cantidad = Label(self.popup, text="Cantidad").grid(row=1, column=0, pady=10, padx=10)
        label_proveedor = Label(self.popup, text="Proveedor").grid(row=2, column=0, pady=10, padx=10)
        label_precio_unidad = Label(self.popup, text="Precio/u").grid(row=3, column=0, pady=10, padx=10)
        label_descuento = Label(self.popup, text="Descuento").grid(row=4, column=0, pady=10, padx=10)

        if nombre is None: #si no se ha obtenido el nombre mediante el treeview (se ha llamado el método desde input_referencia)
            nombre = self.sql.get_elemento_tabla("stock", referencia, "nombre")

        e_nombre = Entry(self.popup)
        e_nombre.insert(END, nombre)
        e_nombre.config(state=DISABLED)
        e_nombre.grid(row=0, column=1)

        e_cantidad = Entry(self.popup)
        c_proveedor = ttk.Combobox(self.popup, width=18, values= self.sql.get_tabla("proveedores"), state="readonly")
        e_precio_unidad = Entry(self.popup)
        e_descuento = Entry(self.popup)

        e_cantidad.grid(row=1, column=1)
        c_proveedor.grid(row=2, column=1)
        e_precio_unidad.grid(row=3, column=1)
        e_descuento.grid(row=4, column=1)

        boton_confirmar = ttk.Button(self.popup, text="Confirmar", command=lambda: self.input_reponer(referencia, nombre, c_proveedor.get(), e_cantidad.get(), e_precio_unidad.get(), e_descuento.get()))
        boton_confirmar.grid(row=5, column=1)

    def input_reponer(self, referencia, nombre, proveedor, cantidad, precio_unidad, descuento):
        '''repone la cantidad y añade la compra a stock'''
        if len(proveedor)!=0 and len(cantidad)!=0 and len(precio_unidad)!=0 and len(descuento)!=0: #valida que las entradas no estén vacías
            try:
                cantidad = int(cantidad)
                precio_unidad = float(precio_unidad)
                descuento = float(descuento)
                categoria = self.sql.get_elemento_tabla("stock", referencia, "categoria")
                if 0 <= descuento <= 100: #valida el rango del descuento
                    self.sql.guardar_elemento(nombre_tabla="historial", fecha=self.get_fecha(), referencia=referencia, nombre=nombre, proveedor=proveedor, precio_unidad=precio_unidad, cantidad=cantidad, descuento=descuento, categoria=categoria)
                    old_cantidad = self.sql.get_elemento_tabla("stock", referencia, "cantidad") #obtiene la anterior cantidad del producto
                    self.sql.set_valor_producto(nombre_tabla="stock", columna="cantidad", id=referencia, valor=cantidad+old_cantidad) #se le suma la nueva cantidad a la cantidad anterior

                    if self.sql.get_elemento_tabla("stock", referencia, "cantidad") > self.sql.get_elemento_tabla("stock", referencia, "stock_min"):
                        self.sql.set_valor_producto(nombre_tabla="stock", columna="estatus", id=referencia, valor="OK") #si la cantidad después de reponer supera el stock mínimo, el estatus se modifica
                    else:
                        self.sql.set_valor_producto(nombre_tabla="stock", columna="estatus", id=referencia, valor="FALTA")

                    self.actualizar_tabla()
                    self.quitar_popup()

                else:
                    messagebox.showwarning(message="El descuento debe situarse entre 0% y 100%", title="Error en la entrada")
            except ValueError:
                messagebox.showwarning(message="Asegúrese de que se introduzcan números donde corresponda", title="Error en la entrada")
        else:
            messagebox.showwarning(message="Asegúrese de haber rellenado todos los campos", title="Error en la entrada")

    def popup_gastar(self, referencia):
        '''popup para reducir la cantidad de un producto de stock'''
        self.popup.destroy()
        self.crear_popup()
        self.popup.title("Gastar producto")

        width, height = 430, 200
        x = (self.screen_width/2)-(width/2)
        y = (self.screen_height/2)-(height/2)
        self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        label_nombre = Label (self.popup, text="Nombre del producto").grid(row=0, column=0, padx=10, pady=10)
        label_cantidad = Label(self.popup, text="Cantidad retirada").grid(row=1, column=0, padx=10, pady=10)

        #la función item retorna una lista dado un id.
        #El id se obtiene con la función focus(), que retorna el id del elemento sobre el que se ha clicado en la tabla
        nombre = self.tabla_stock.item(self.tabla_stock.focus(), "values")[1]
        e_nombre = Entry(self.popup)
        e_nombre.insert(END, nombre)
        e_nombre.config(state=DISABLED)
        e_nombre.grid(row=0, column=1, pady=10, padx=10)

        s_gasto = ttk.Spinbox(self.popup, width=5, from_=1, to=9999)
        s_gasto.grid(row=1, column=1)
        s_gasto.focus()
        boton_confirmar = ttk.Button(self.popup, text="Confirmar", command = lambda: self.input_gastar(referencia, s_gasto.get()))
        boton_confirmar.grid(row=2, column=1, pady=10)

    def input_gastar(self, referencia, gasto):
        '''valida y gasta la cantidad del producto de stock'''
        cantidad = self.sql.get_elemento_tabla("stock", referencia, "cantidad")
        cantidad = int(cantidad)
        if len(gasto) != 0:
            try:
                gasto = int(gasto)
                stock_min = int(self.sql.get_elemento_tabla("stock", referencia, "stock_min"))

                if gasto > 0:
                    if gasto <= cantidad: #no se pueden gastar más unidades de las que se tienen
                        self.sql.set_valor_producto(nombre_tabla="stock", columna="cantidad", id=referencia, valor=cantidad-gasto)

                        self.actualizar_tabla()

                        if 0 < cantidad-gasto <= stock_min: #se ha alcanzado el stock mínimo
                            messagebox.showwarning(message="Se está agotando el producto", title="Advertencia")
                            self.sql.set_valor_producto(nombre_tabla="stock", columna="estatus", id=referencia, valor="FALTA")

                            self.actualizar_tabla()

                        if cantidad-gasto == 0: #producto agotado
                            messagebox.showwarning(message="Se ha agotado el producto", title="Advertencia")
                            self.sql.set_valor_producto(nombre_tabla="stock", columna="estatus", id=referencia, valor="AGOTADO")

                            self.actualizar_tabla()

                        self.quitar_popup()

                    else:
                        messagebox.showwarning(message="El gasto es mayor que el número de unidades existentes", title="Error en la entrada")
                else:
                    messagebox.showwarning(message="El gasto debe ser mayor que 0", title="Error en la entrada")
            except ValueError:
                messagebox.showwarning(message="Introduzca un número entero", title="Error en la entrada")
        else:
            messagebox.showwarning(message="No se ha introducido ninguna cantidad", title="Error en la entrada")

    def get_fecha(self):
        '''obtiene la fecha actual'''
        now = datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        return now

    def popup_stock(self, referencia):
        '''popup para añadir un nuevo producto'''
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title("Entrada de datos")

            width, height = 600, 600
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            label_fecha = Label(self.popup, text = "Fecha").grid(row = 0, column = 0, pady=10, padx=10)
            label_referencia = Label(self.popup, text = "Referencia").grid(row = 1, column = 0, pady=10, padx=10)
            label_nombre = Label(self.popup, text = "Nombre del producto").grid(row = 2, column = 0, pady=10, padx=10)
            label_proveedor = Label(self.popup, text = "Proveedor").grid(row = 3, column = 0, pady=10, padx=10)
            label_precio_unidad = Label(self.popup, text = "Precio/Unidad").grid(row = 4, column = 0, pady=10, padx=10)
            label_cantidad = Label(self.popup, text = "Cantidad").grid(row = 5, column = 0, pady=10, padx=10)
            label_descuento = Label(self.popup, text = "Descuento (%)").grid(row = 6, column = 0, pady=10, padx=10)
            label_stock_min = Label(self.popup, text = "Stock mínimo").grid(row = 7, column = 0, pady=10, padx=10)
            label_categoria = Label(self.popup, text = "Categoría").grid(row = 8, column = 0, pady=10, padx=10)

            e_fecha = Entry(self.popup, width=30)
            e_fecha.insert(END, self.get_fecha())
            e_fecha.config(state=DISABLED)

            e_referencia = Entry(self.popup, width=30)
            e_referencia.insert(END, referencia)
            e_referencia.config(state=DISABLED)

            e_nombre = Entry(self.popup, width=30)
            c_proveedor = ttk.Combobox(self.popup, width=28, values = self.sql.get_tabla("proveedores"), state = "readonly")
            e_precio_unidad = Entry(self.popup, width=30)
            e_cantidad = Entry(self.popup, width=30)
            e_descuento = Entry(self.popup, width=30)
            e_stock_min = Entry(self.popup, width=30)
            c_categoria = ttk.Combobox(self.popup, width=28, values = self.sql.get_tabla("categorias"), state="readonly")

            e_fecha.grid(row = 0, column = 1, pady=10, padx=10)
            e_referencia.grid(row=1, column=1, pady=10, padx=10)
            e_nombre.grid(row = 2, column = 1, pady=10, padx=10)
            c_proveedor.grid(row = 3, column = 1, pady=10, padx=10)
            e_precio_unidad.grid(row = 4, column = 1, pady=10, padx=10)
            e_cantidad.grid(row = 5, column = 1, pady=10, padx=10)
            e_descuento.grid(row = 6, column = 1, pady=10, padx=10)
            e_stock_min.grid(row = 7, column = 1, pady=10, padx=10)
            c_categoria.grid(row = 8, column = 1, pady=10, padx=10)

            boton_enviar = ttk.Button(self.popup, text = "Confirmar datos", command = lambda: self.input_stock(referencia, e_fecha.get(), e_nombre.get().upper(),e_precio_unidad.get(), e_cantidad.get(), e_stock_min.get(), e_descuento.get(), c_proveedor.get(), c_categoria.get()))
            boton_enviar.grid(row = 9, column = 1, pady = 5)

    def input_stock(self, referencia, fecha, nombre, precio_unidad, cantidad, stock_min, descuento, proveedor, categoria):
        '''valida la información del producto y lo guarda en la base de datos (stock e historial)'''
        if len(fecha)!=0 and len(referencia)!=0 and len(nombre)!=0 and len(precio_unidad)!=0 and len(cantidad)!=0 and len(stock_min)!=0 and len(descuento)!=0 and len(proveedor)!=0 and len(categoria)!=0:
            try:
                precio_unidad = float(precio_unidad)
                cantidad = int(cantidad)
                stock_min = int(stock_min)
                descuento = float(descuento)

                if self.sql.existe("stock", "nombre", nombre) == False:
                    if 0 <= descuento <= 100:
                        if stock_min < cantidad:
                            estatus="OK"
                        else:
                            estatus="FALTA"
                        self.sql.guardar_elemento(nombre_tabla="historial", fecha=fecha, referencia=referencia, nombre=nombre, proveedor=proveedor, precio_unidad=precio_unidad, cantidad=cantidad, descuento=descuento, categoria=categoria)
                        self.sql.guardar_elemento(nombre_tabla="stock", referencia=referencia, nombre=nombre, cantidad=cantidad, categoria=categoria, stock_min=stock_min, estatus=estatus)

                        self.quitar_popup()
                        self.actualizar_tabla()
                    else:
                        messagebox.showwarning(message="El descuento debe situarse entre 0% y 100%", title="Error en la entrada")
                else:
                    messagebox.showwarning(message="Este nombre ya existe", title="Error en la entrada")
            except ValueError:
                messagebox.showwarning(message="Asegúrese de haber introducido números donde corresponda", title="Error en la entrada")
        else:
            messagebox.showwarning(message="Asegúrese de haber rellenado todos los campos", title="Error en la entrada")

    def popup_editar(self, referencia, nombre_antiguo):
        '''abre un popup para editar nombre, stock_min y/o categoría'''
        self.popup.destroy()
        self.crear_popup()
        self.popup.title("Editar producto")

        width, height= 660, 230
        x = (self.screen_width/2)-(width/2)
        y = (self.screen_height/2)-(height/2)
        self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        label_nombre = Label(self.popup, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        label_stockmin = Label(self.popup, text="Stock mínimo").grid(row=1, column=0, pady=10, padx=10)
        label_categoria = Label(self.popup, text="Categoría").grid(row=2, column=0, pady=10, padx=10)

        stockmin_antiguo = self.sql.get_elemento_tabla("stock", referencia, "stock_min")
        categoria_antigua = self.sql.get_elemento_tabla("stock", referencia, "categoria")

        e_nombre_antiguo = Entry(self.popup)
        e_nombre_antiguo.insert(END, nombre_antiguo)
        e_nombre_antiguo.config(state=DISABLED)
        e_nombre_antiguo.grid(row=0, column=1, pady=10, padx=10)

        e_stockmin_antiguo = Entry(self.popup)
        e_stockmin_antiguo.insert(END, stockmin_antiguo)
        e_stockmin_antiguo.config(state=DISABLED)
        e_stockmin_antiguo.grid(row=1, column=1, pady=10, padx=10)

        e_categoria_antigua = Entry(self.popup)
        e_categoria_antigua.insert(END, categoria_antigua)
        e_categoria_antigua.config(state=DISABLED)
        e_categoria_antigua.grid(row=2, column=1, pady=10, padx=10)

        e_nombre_nuevo = Entry(self.popup)
        e_nombre_nuevo.grid(row=0, column=2, pady=10, padx=10) #comprobar que ese nombre no exista

        e_stockmin_nuevo = Entry(self.popup)
        e_stockmin_nuevo.grid(row=1, column=2, pady=10, padx=10)

        c_categoria_nueva = ttk.Combobox(self.popup, width=18, values=self.sql.get_tabla("categorias"), state="readonly")
        c_categoria_nueva.grid(row=2, column=2)

        boton_editar = ttk.Button(self.popup, text="Confirmar", command = lambda: self.input_editar(referencia, e_nombre_nuevo.get().upper(), e_stockmin_nuevo.get(), c_categoria_nueva.get()))
        boton_editar.grid(row=3, column=1)

    def input_editar(self, referencia, nombre, stock_min, categoria):
        error = False
        if len(stock_min) != 0:
            try:
                stock_min_num = int(stock_min)
                if int(self.sql.get_elemento_tabla("stock", referencia, "cantidad")) <= stock_min_num:
                    self.sql.set_valor_producto(nombre_tabla="stock",columna="estatus", id=referencia, valor="FALTA")
                    messagebox.showwarning(message="Se está agotando el producto", title="Advertencia")
                else:
                    self.sql.set_valor_producto(nombre_tabla="stock", columna="referencia", id=referencia, valor="OK")
            except ValueError:
                messagebox.showwarning(message="Asegúrese de que STOCK MÍNIMO sea un número entero", title="Error en la entrada")
                error = True
        if len(nombre) != 0:
            if self.sql.existe(nombre_tabla="historial", columna="nombre", elemento=nombre) == True:
                messagebox.showwarning(message="Este nombre ya existe", title="Error en la entrada")
                error = True

        if error == False:
            if len(nombre) != 0 and len(stock_min) != 0 and len(categoria) != 0: #nombre stock_min categoria
                    self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="nombre", columna2="stock_min", columna3="categoria", elemento1=nombre, elemento2=stock_min, elemento3=categoria)
                    self.sql.editar_from_stock(nombre_tabla="historial", id=referencia, columna1="nombre", columna2="categoria", elemento1=nombre, elemento2=categoria)

            elif len(nombre) != 0 and len(stock_min) != 0 and len(categoria) == 0: #nombre stock_min
                self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="nombre", columna2="stock_min", elemento1=nombre, elemento2=stock_min)
                self.sql.editar_from_stock(nombre_tabla="historial", id=referencia, columna1="nombre", elemento1=nombre)

            elif len(nombre) != 0 and len(stock_min) == 0 and len(categoria) != 0: #nombre categoria
                self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="nombre", columna2="categoria", elemento1=nombre, elemento2=categoria)
                self.sql.editar_from_stock(nombre_tabla="historial", id=referencia, columna1="nombre", columna2="categoria", elemento1=nombre, elemento2=categoria)

            elif len(nombre) != 0 and len(stock_min) == 0 and len(categoria) == 0: #nombre
                self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="nombre", elemento1=nombre)
                self.sql.editar_from_stock(nombre_tabla="historial", id=referencia, columna1="nombre", elemento1=nombre)

            elif len(nombre) == 0 and len(stock_min) != 0 and len(categoria) != 0: #stock_min categoria
                self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="stock_min", columna2="categoria", elemento1=stock_min, elemento2=categoria)
                self.sql.editar_from_stock(nombre_tabla="historial", id=referencia, columna1="categoria", elemento1=categoria)

            elif len(nombre) == 0 and len(stock_min) == 0 and len(categoria) != 0: #categoria
                self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="categoria", elemento1=categoria)
                self.sql.editar_from_stock(nombre_tabla="historial", id=referencia, columna1="categoria", elemento1=categoria)

            elif len(nombre) == 0 and len(stock_min) != 0 and len(categoria) == 0: #stock_min
                self.sql.editar_from_stock(nombre_tabla="stock", id=referencia, columna1="stock_min", elemento1=stock_min)

            else:
                messagebox.showwarning(message="No se ha rellenado ningún campo", title="Error en la entrada")

            self.quitar_popup()
            self.actualizar_tabla()

    def popup_input_categoria_proveedor(self, tabla, columna):
        '''popup para añadir categoría o proveedor (indicado por la variable columna)'''
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title(f"Añadir {columna.upper()}")

            width, height = 400, 100
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            e_nuevo = Entry(self.popup)
            e_nuevo.grid(row=1, column=0, pady=10, padx=10)
            e_nuevo.bind("<Return>", lambda event: self.input_categoria_proveedor(tabla, columna, e_nuevo.get().upper().replace(" ", "_")))
            e_nuevo.focus()

            boton_confirmar = ttk.Button(self.popup, text="Confirmar", command=lambda:self.input_categoria_proveedor(tabla, columna, e_nuevo.get().upper().replace(" ", "_")))
            boton_confirmar.grid(row=1, column=1, pady=10, padx=10)

    def input_categoria_proveedor(self, tabla, columna, nuevo):
        '''valida la categoría/proveedor y se almacena en al base de datos'''
        if len(nuevo) != 0:
            if self.sql.existe(nombre_tabla=tabla, columna=columna, elemento=nuevo) == False:
                if tabla=="categorias":
                    self.sql.guardar_elemento(nombre_tabla=tabla, categoria=nuevo)
                    self.clear_categoria()
                else:
                    self.sql.guardar_elemento(nombre_tabla=tabla, proveedor=nuevo)

                self.quitar_popup()

            else:
                messagebox.showwarning(message=f"{nuevo} ya existe", title="Error en la entrada")
        else:
            messagebox.showwarning(message="No se ha introducido ningún elemento", title="Error en la entrada")

    def popup_editar_categoria_proveedor(self, tabla, columna, valores):
        '''abre un popup para editar una categoría/proveedor'''
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title(f"Editar {columna.upper()}")

            width, height = 500, 150
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            c_antiguo = ttk.Combobox(self.popup, values=valores, state="readonly")
            c_antiguo.grid(row=1, column=1, pady=10, padx=10)

            e_nuevo = Entry(self.popup)
            e_nuevo.grid(row=1, column=2, pady=10, padx=10)
            e_nuevo.bind("<Return>", lambda event: self.editar_categoria_proveedor(tabla, columna, e_nuevo.get().upper().replace(" ", "_"), c_antiguo.get()))

            boton_confirmar = ttk.Button(self.popup, text="Confirmar", command=lambda:self.editar_categoria_proveedor(tabla, columna, e_nuevo.get().upper().replace(" ", "_"), c_antiguo.get()))
            boton_confirmar.grid(row=2, column=2, pady=10, padx=10)

    def editar_categoria_proveedor(self, tabla, columna, nuevo, old):
        '''valida la entrada y modifica esa categoría/proveedor de la base de datos (categorías/proveedores)'''
        if len(nuevo) != 0 and len(old) != 0:
            if self.sql.existe(nombre_tabla=tabla, columna=columna, elemento=nuevo) == False:
                if tabla == "categorias":
                    self.sql.set_valor_tabla(nombre_tabla="stock", columna="categoria", nuevo=nuevo, old=old)
                    self.sql.set_valor_tabla(nombre_tabla="historial", columna="categoria", nuevo=nuevo, old=old)
                    self.sql.set_valor_tabla(nombre_tabla=tabla, columna="categoria", nuevo=nuevo, old=old)
                    self.clear_categoria()
                else:
                    self.sql.set_valor_tabla(nombre_tabla="historial", columna="proveedor", nuevo=nuevo, old=old)
                    self.sql.set_valor_tabla(nombre_tabla=tabla, columna="proveedor", nuevo=nuevo, old=old)
                self.actualizar_tabla()
                self.quitar_popup()
            else:
                messagebox.showwarning(message=f"Ya existe {nuevo}", title="Error en la entrada")
        else:
            messagebox.showwarning(message="Rellene todos los campos", title="Error en la entrada")

    def popup_borrar_categoria_proveedor(self, tabla, columna):
        '''abre un popup para eliminar una categoria/proveedor'''
        if self._popup_abierto == False:
            self.crear_popup()
            self.popup.title(f"Eliminar {columna.upper()}")

            width, height = 400, 100
            x = (self.screen_width/2)-(width/2)
            y = (self.screen_height/2)-(height/2)
            self.popup.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

            valores = self.sql.get_tabla(tabla)
            self.c_borrar = ttk.Combobox(self.popup, values=valores, state="readonly")
            self.c_borrar.grid(row=1, column=0, pady=10, padx=10)

            boton_enviar_proveedor = ttk.Button(self.popup, text="Confirmar", command=lambda:self.borrar_categoria_proveedor(tabla, columna)).grid(row=1, column=1)

    def borrar_categoria_proveedor(self, tabla, columna):
        '''elimina esa categoría/proveedor de la base de datos (categorías/proveedores)'''
        borrar = self.c_borrar.get()
        if len(borrar) != 0:
            if self.sql.existe(nombre_tabla="historial", columna=columna, elemento=borrar) == False:
                if tabla=="categorias":
                    self.sql.borrar_elemento(nombre_tabla=tabla, columna_id=columna, id=borrar)
                    self.clear_categoria()
                else:
                     self.sql.borrar_elemento(nombre_tabla=tabla, columna_id= columna, id=borrar)
                messagebox.showwarning(message=f"{borrar} ha sido eliminado", title="Error en la entrada")
                self.quitar_popup()
            else:
                messagebox.showwarning(message=f"Existe una entrada en HISTORIAL con {borrar}.\n {borrar} no puede ser eliminado", title="Error en la entrada")
        else:
            messagebox.showwarning(message="No se ha introducido ningún elemento", title="Error en la entrada")
