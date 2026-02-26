from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3
import hashlib

PORT = 8000

# ==========================
# BASE DE DATOS
# ==========================

conn = sqlite3.connect("neocare.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# Crear usuario admin si no existe
cursor.execute("SELECT * FROM usuarios WHERE username='admin'")
if not cursor.fetchone():
    password = hashlib.sha256("1234".encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios (username,password) VALUES (?,?)", ("admin", password))
    conn.commit()

# ==========================
# HTML PAGES
# ==========================

def login_page():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

def dashboard_page(user):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/style.css">
        <title>Dashboard</title>
    </head>
    <body>
        <div class="box">
            <h2>Bienvenido {user}</h2>
            <p>Sistema Profesional Neonatal</p>
            <a href="/">Cerrar sesión</a>
        </div>
    </body>
    </html>
    """

# ==========================
# SERVIDOR
# ==========================

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):

        # Servir CSS
        if self.path == "/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            with open("style.css", "rb") as f:
                self.wfile.write(f.read())
            return

        # Ruta Dashboard
        if self.path.startswith("/dashboard"):
            username = self.path.split("?user=")[-1]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(dashboard_page(username).encode())
            return

        # Ruta Login
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(login_page().encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode())

        username = data.get("username", [""])[0]
        password = data.get("password", [""])[0]
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password_hash))
        user = cursor.fetchone()

        if user:
            # REDIRECCIÓN REAL
            self.send_response(303)
            self.send_header("Location", f"/dashboard?user={username}")
            self.end_headers()
        else:
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

# ==========================
# EJECUTAR
# ==========================

print(f"Servidor corriendo en http://localhost:{PORT}")
HTTPServer(("", PORT), MyServer).serve_forever()