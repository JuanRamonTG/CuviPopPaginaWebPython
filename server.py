from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
from http import cookies
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

# Credenciales en memoria (simple)
USERS = {"admin": "admin"}

#Clase para convertir Decimal y datetime a JSON
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class miServidor(SimpleHTTPRequestHandler):
    def parse_cookies(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return {}
        c = cookies.SimpleCookie()
        c.load(cookie_header)
        return {k: v.value for k, v in c.items()}

    def is_logged(self):
        c = self.parse_cookies()
        return 'session' in c and c['session'] in USERS

    def do_GET(self):
        url_parseada = urlparse(self.path)
        path = url_parseada.path
        # Normalizar: quitar slash final salvo en la raíz
        if path != '/' and path.endswith('/'):
            path = path.rstrip('/')
        parametros = parse_qs(url_parseada.query)

        # Ruta de login (mostrar formulario)
        if path == "/login":
            # servir login.html (se puede añadir ?error=1 para mostrar mensaje)
            self.path = "login.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        # Proteger la raíz: si no está logueado, redirigir a /login
        if path == "/":
            if not self.is_logged():
                self.send_response(303)
                self.send_header('Location', '/login')
                self.end_headers()
                return
            self.path = "index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

    # CRUD Pedidos
        if path == "/pedidos":
            try:
                pedidos = crudPedidos.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(pedidos, cls=CustomEncoder).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode('utf-8'))
                return

    # CRUD Empleados
        elif path == "/empleados":
            try:
                empleados = crudEmpleados.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(empleados, cls=CustomEncoder).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode('utf-8'))
                return

    # CRUD Productos
        elif path == "/productos":
            try:
                productos = crudProductos.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(productos, cls=CustomEncoder).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "error": str(e)}).encode('utf-8'))
                return

        if path == "/vistas":
            self.path = '/modulos/' + parametros['form'][0] + '.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        # Fallback: servir archivos estáticos (ej. /menu.html, /styles.css)
        # Log de depuración para identificar peticiones que llegan aquí
        print(f"Fallback estático para path: {self.path} -> parseado: {path} - User-Agent: {self.headers.get('User-Agent')}")
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            path = urlparse(self.path).path

            # Manejar login separadamente (acepta form-urlencoded o json)
            if path == "/login":
                longitud = int(self.headers.get('Content-Length', 0))
                datos = self.rfile.read(longitud).decode('utf-8')
                ctype = self.headers.get('Content-Type', '')
                username = None
                password = None
                if 'application/json' in ctype:
                    try:
                        payload = json.loads(parse.unquote(datos))
                        username = payload.get('username')
                        password = payload.get('password')
                    except Exception:
                        pass
                else:
                    # form-urlencoded
                    parsed = parse.parse_qs(datos)
                    username = parsed.get('username', [None])[0]
                    password = parsed.get('password', [None])[0]

                if username and password and USERS.get(username) == password:
                    # cookie muy simple
                    self.send_response(303)
                    self.send_header('Set-Cookie', f'session={username}; Path=/')
                    self.send_header('Location', '/')
                    self.end_headers()
                    return
                else:
                    # redirigir de nuevo al login con error
                    self.send_response(303)
                    self.send_header('Location', '/login?error=1')
                    self.end_headers()
                    return

            # Si no es login, procesar como antes (JSON esperado)
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud)
            datos = datos.decode("utf-8")
            datos = parse.unquote(datos)
            datos = json.loads(datos)

            # Determinar a qué CRUD enviar los datos según la ruta
            if path == "/pedidos":
                resultado = crudPedidos.administrar(datos)
            elif path == "/empleados":
                resultado = crudEmpleados.administrar(datos)
            elif path == "/productos":
                resultado = crudProductos.administrar(datos)
                print(f"POST /productos -> administrar result: {resultado}")
            else:
                raise ValueError("Ruta no válida para POST")

            # Interpretar resultado: si es entero >0 -> ok, si es string (error) o 0 -> error
            ok = False
            if isinstance(resultado, int) and resultado > 0:
                ok = True
            if isinstance(resultado, str):
                print(f"Error desde CRUD al administrar: {resultado}")

            resp = {"msg": "ok" if ok else "error", "detail": str(resultado)}
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
