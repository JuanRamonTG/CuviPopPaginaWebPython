from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import json
from decimal import Decimal
from datetime import datetime
import crud_pedidos
import crud_empleados
import crud_productos

crudPedidos = crud_pedidos.crud_pedidos()
crudEmpleados = crud_empleados.crud_empleados()
crudProductos = crud_productos.crud_productos()

port = 3000

#Clase para convertir Decimal y datetime a JSON
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parseada = urlparse(self.path)
        path = url_parseada.path
        parametros = parse_qs(url_parseada.query)

        if self.path == "/":
            self.path = "index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

    # CRUD Pedidos
        if self.path == "/pedidos":
            try:
                pedidos = crudPedidos.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(pedidos, cls=CustomEncoder).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode('utf-8'))

    # CRUD Empleados
        elif self.path == "/empleados":
            try:
                empleados = crudEmpleados.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(empleados, cls=CustomEncoder).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode('utf-8'))

    # CRUD Productos
        elif self.path == "/productos":
            try:
                productos = crudProductos.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(productos, cls=CustomEncoder).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode('utf-8'))

        if path == "/vistas":
            self.path = '/modulos/' + parametros['form'][0] + '.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud)
            datos = datos.decode("utf-8")
            datos = parse.unquote(datos)
            datos = json.loads(datos)

            # Determinar a qué CRUD enviar los datos según la ruta
            path = urlparse(self.path).path
            if path == "/pedidos":
                resultado = crudPedidos.administrar(datos)
            elif path == "/empleados":
                resultado = crudEmpleados.administrar(datos)
            elif path == "/productos":
                resultado = crudProductos.administrar(datos)
            else:
                raise ValueError("Ruta no válida para POST")

            resp = {"msg": "ok" if resultado else "error"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp, cls=CustomEncoder).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode("utf-8"))


print("Servidor ejecutandose en el puerto", port)
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()
