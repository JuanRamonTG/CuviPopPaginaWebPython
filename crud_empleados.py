import crud_cuvipopweb

db = crud_cuvipopweb.crud()

class crud_empleados:
    def consultar(self, buscar):
        return db.consultar("SELECT * FROM empleados WHERE nombre LIKE '%"+ buscar +"%'")
    
    def administrar(self, datos):
        if datos['accion'] == "nuevo":
            sql = """
                INSERT INTO empleados (nombre, cargo, email, telefono, usuario, contrasena, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                datos['nombre'],
                datos['cargo'],
                datos['email'],
                datos['telefono'],
                datos['usuario'],
                datos['contrasena'],
                datos['estado']
            )
        if datos['accion'] == "modificar":
            sql = """
                UPDATE empleados 
                SET nombre=%s, cargo=%s, email=%s, telefono=%s, usuario=%s, contrasena=%s, estado=%s
                WHERE idEmpleado=%s
            """
            valores = (
                datos['nombre'],
                datos['cargo'],
                datos['email'],
                datos['telefono'],
                datos['usuario'],
                datos['contrasena'],
                datos['estado'],
                datos['idEmpleado']
            )
        if datos['accion'] == "eliminar":
            sql = "DELETE FROM empleados WHERE idEmpleado=%s"
            valores = (datos['idEmpleado'],)
        return db.ejecutar(sql, valores)
