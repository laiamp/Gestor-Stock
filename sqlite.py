class SQLite():
    def __init__(self):
        self.con = sqlite3.connect('Gestor_Stock.db') #establece la conexión entre la aplicación y la base de datos
        self.cursor = self.con.cursor() #permite interactuar con la base de datos
        #se crean las tablas si no existen
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stock(referencia text PRIMARY KEY, nombre text, cantidad real, stock_min real, categoria text, estatus text)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categorias(categoria text PRIMARY KEY)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS proveedores (proveedor text PRIMARY KEY)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS historial(fecha text PRIMARY KEY, mes text, referencia text, nombre text, proveedor text, precio_unidad real, cantidad real, descuento real, total real, categoria text)")
        self.con.commit() #guarda los cambios

    def guardar_elemento(self, nombre_tabla, fecha=None, referencia=None, nombre=None, proveedor=None, precio_unidad=None, cantidad=None, descuento=None, categoria=None, stock_min=None, estatus=None):
        if nombre_tabla == "stock": #guardar elementos en stock
            data = (referencia, nombre, cantidad, stock_min, categoria, estatus)
            self.cursor.execute(f"INSERT INTO {nombre_tabla}(referencia, nombre, cantidad, stock_min, categoria, estatus) VALUES (?,?,?,?,?,?)", data)

        elif nombre_tabla == "historial":
            data = (fecha, fecha[3:10],referencia, nombre, proveedor, precio_unidad, cantidad, descuento, round(cantidad*precio_unidad*(1-descuento/100),2), categoria)
            self.cursor.execute(f"INSERT INTO {nombre_tabla}(fecha, mes, referencia, nombre, proveedor, precio_unidad, cantidad, descuento, total, categoria) VALUES (?,?,?,?,?,?,?,?,?,?)", data)

        elif nombre_tabla == "categorias":
            self.cursor.execute(f"INSERT INTO {nombre_tabla} (categoria) VALUES(?)", (categoria,))

        else:
            self.cursor.execute(f"INSERT INTO {nombre_tabla} (proveedor) VALUES(?)", (proveedor,))
        self.con.commit()

    def get_tabla(self, nombre_tabla): #obtiene todos los valores de una tabla
        if nombre_tabla != "stock":
            self.cursor.execute(f"SELECT * FROM {nombre_tabla}")
        else:
            self.cursor.execute("SELECT referencia, nombre, cantidad, categoria, estatus FROM stock")
        return self.cursor.fetchall()

    def get_meses(self): #obtiene todos los meses en los que se haya añadido algún producto
        self.cursor.execute("SELECT mes FROM historial") #algunos meses pueden estar repetidos
        lista = self.cursor.fetchall()
        lista = list(dict.fromkeys(lista)) #elimino duplicados conviertiendo la lista en un diccionario
        return lista

    def get_descarga(self, id): #obtiene todos los parámetros (menos el mes y el año) pertenecientes al mes seleccionado
        self.cursor.execute("SELECT fecha, referencia, nombre, proveedor, precio_unidad, cantidad, descuento, total, categoria from historial WHERE mes = ?", (id,))
        return self.cursor.fetchall()

    def get_editar(self, id): #obtener valores de stock/historial para editar
        self.cursor.execute("SELECT proveedor, precio_unidad, descuento, total, cantidad FROM historial WHERE fecha=?", (id,))
        return self.cursor.fetchall()

    def get_elemento_tabla(self, nombre_tabla, id, elemento): #obtiene un elemento específico de stock en base a su referencia
        if nombre_tabla == "stock":
            self.cursor.execute(f"SELECT {elemento} FROM stock WHERE referencia =?", (id,))

        else:
            self.cursor.execute(f"SELECT {elemento} FROM historial WHERE fecha = ?", (id,))

        return self.cursor.fetchone()[0]

    def get_total(self, mes, columna): #obtiene un diccionario que agrupe cada categoría/proveedor con su gasto correspondiente
        self.cursor.execute(f"SELECT {columna}, total FROM historial WHERE mes = ?", (mes,))
        lista = self.cursor.fetchall()
        dictionary = {} #creo un diccionario vacío
        for i in lista:
            #i[0] es la categoría del producto e i[1] es su gasto total
            if i[0] in dictionary: #si la categoría ya la habíamos encontrado
                 dictionary[i[0]] += i[1] #se suma el gasto de ese producto al gasto total de la categoría

            else: #si la categoría no estaba aún se crea un nuevo par en dictionary con la categoría y el gasto del producto
                dictionary.update({i[0]: i[1]})

        return dictionary

    def borrar_elemento(self, nombre_tabla, columna_id, id): #elimina un elemento de una tabla
        self.cursor.execute(f"DELETE FROM {nombre_tabla} WHERE {columna_id} = ?", (id,))
        self.con.commit()

    def editar_from_stock(self, nombre_tabla, id, columna1=None, columna2=None, columna3=None, elemento1=None, elemento2=None, elemento3=None): #editar nombre, categoria y/o stock_mín desde el frame stock
        if columna2 is None and columna3 is None: #1 elemento a editar
            self.cursor.execute(f"UPDATE {nombre_tabla} SET {columna1} = ? WHERE referencia = ?", (elemento1, id))

        elif columna2 is not None and columna3 is None: #2 elementos a editar
            self.cursor.execute(f"UPDATE {nombre_tabla} SET {columna1} = ?, {columna2}=? WHERE referencia=?", (elemento1, elemento2, id))

        else: #3 elementos a editar
            self.cursor.execute(f"UPDATE {nombre_tabla} SET {columna1}=?, {columna2}=?, {columna3}=? WHERE referencia=?", (elemento1, elemento2, elemento3, id))

        self.con.commit()

    def editar_from_historial(self, id, datos): #edita proveedor precio descuento y total de historial
        self.cursor.execute("UPDATE historial SET proveedor=?, precio_unidad=?, descuento=?, total=? WHERE fecha=?", datos + (id,))
        self.con.commit()

    def existe(self, nombre_tabla, columna, elemento): #comprueba la existencia de un elemento concreto en una tabla concreta
        self.cursor.execute(f"SELECT {columna} FROM {nombre_tabla} WHERE {columna} =?", (elemento,))
        lista = self.cursor.fetchall() #lista con todos los elementos de la tabla que correspondan con el elemento escogido
        if len(lista) != 0: #si la lista contiene elementos se retorna True
            return True
        else: #si la lista está vacía significa que ese elemento no aparece y se retorna False
            return False

    def set_valor_producto(self, nombre_tabla, columna, id, valor): #cambia el valor de un único parámetro de un producto concreto en base a su id
        if nombre_tabla == "stock":
            self.cursor.execute(f"UPDATE stock SET {columna}=? WHERE referencia=?", (valor, id))
        else:
            self.cursor.execute(f"UPDATE historial SET {columna}=? WHERE fecha=?", (valor, id))
        self.con.commit()

    def set_valor_tabla(self, nombre_tabla, columna, nuevo, old): #cambia un único valor todas las veces que aparezca en una tabla
        self.cursor.execute(f"UPDATE {nombre_tabla} SET {columna} = ? WHERE {columna} = ?", (nuevo, old))
        self.con.commit()

    def filtrar(self, nombre_tabla, columna1, criterio1, columna2=None, criterio2=None, columna3=None, criterio3=None): #selecciona los productos/compras que cumplan con X criterios
        if nombre_tabla == "historial":
            if columna2 is None and columna3 is None: #1 elemento seleccionado como criterio
                self.cursor.execute(f"SELECT * FROM historial WHERE {columna1} = ?", (criterio1,))

            elif columna2 is not None and columna3 is None: #2 elementos seleccionados como criterio
                self.cursor.execute(f"SELECT * FROM historial WHERE {columna1} = ? AND {columna2} = ?", (criterio1, criterio2))

            else: #3 elementos seleccionados como criterio
                self.cursor.execute(f"SELECT * FROM historial WHERE {columna1} = ? AND {columna2} = ? AND {columna3} = ?", (criterio1, criterio2, criterio3))

        else: #stock
            if columna2==None: #1 elemento
                self.cursor.execute(f"SELECT referencia, nombre, cantidad, categoria, estatus FROM stock WHERE {columna1} = ?", (criterio1,))

            else: #2 elementos
                self.cursor.execute(f"SELECT referencia, nombre, cantidad, categoria, estatus FROM stock WHERE {columna1} = ? AND {columna2}=?", (criterio1, criterio2))

        return self.cursor.fetchall()
