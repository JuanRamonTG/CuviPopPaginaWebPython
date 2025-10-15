import crud_cuvipopweb

db = crud_cuvipopweb.crud()

class crud_productos:
    def consultar(self, buscar):
        return db.consultar("SELECT * FROM productos WHERE nombre LIKE '%"+ buscar +"%'")
    
    def administrar(self, datos):
        if datos['accion'] == "nuevo":
            sql = """
                INSERT INTO productos (nombre, descripcion, precio, categoria, estado, imagen)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                datos['nombre'],
                datos['descripcion'],
                datos['precio'],
                datos['categoria'],
                datos['estado'],
                datos.get('imagen', None)
            )
        if datos['accion'] == "modificar":
            sql = """
                UPDATE productos 
                SET nombre=%s, descripcion=%s, precio=%s, categoria=%s, estado=%s, imagen=%s
                WHERE idProducto=%s
            """
            valores = (
                datos['nombre'],
                datos['descripcion'],
                datos['precio'],
                datos['categoria'],
                datos['estado'],
                datos.get('imagen', None),
                datos['idProducto']
            )
        if datos['accion'] == "eliminar":
            sql = "DELETE FROM productos WHERE idProducto=%s"
            valores = (datos['idProducto'],)
        return db.ejecutar(sql, valores)
