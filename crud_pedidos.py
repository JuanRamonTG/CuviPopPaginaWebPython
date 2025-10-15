import crud_cuvipopweb

db = crud_cuvipopweb.crud()

class crud_pedidos:
    def consultar(self, buscar):
        return db.consultar("SELECT * FROM pedidos WHERE idCliente LIKE '%"+ buscar +"%' OR productos LIKE '%"+ buscar +"%'")
    
    def administrar(self, datos):
        if datos['accion'] == "nuevo":
            sql = """
                INSERT INTO pedidos (idCliente, productos, total, fecha, estado, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                datos['idCliente'],
                datos['productos'],
                datos['total'],
                datos['fecha'],
                datos['estado'],
                datos.get('observaciones', None)
            )
        if datos['accion'] == "modificar":
            sql = """
                UPDATE pedidos 
                SET idCliente=%s, productos=%s, total=%s, fecha=%s, estado=%s, observaciones=%s
                WHERE idPedido=%s
            """
            valores = (
                datos['idCliente'],
                datos['productos'],
                datos['total'],
                datos['fecha'],
                datos['estado'],
                datos.get('observaciones', None),
                datos['idPedido']
            )
        if datos['accion'] == "eliminar":
            sql = "DELETE FROM pedidos WHERE idPedido=%s"
            valores = (datos['idPedido'],)
        return db.ejecutar(sql, valores)
