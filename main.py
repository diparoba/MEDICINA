from restricciones import *
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import webbrowser
import threading
import time

app = Flask(__name__)

# Base de datos
def init_db():
    conn = sqlite3.connect('neonatos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, puntaje INTEGER, estado TEXT, diagnostico TEXT, fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    puntaje = sum(int(v) for v in data.get('valores', {}).values())
    nombre = data.get('nombre') or "Paciente Anónimo"
    
    if puntaje >= 7:
        estado, diag, color = "VIGOROSO", "Bebé en excelentes condiciones.", "#27ae60"
    elif 4 <= puntaje <= 6:
        estado, diag, color = "DEPRESIÓN MODERADA", "Requiere estimulación y oxígeno.", "#f39c12"
    else:
        estado, diag, color = "DEPRESIÓN SEVERA", "¡EMERGENCIA! Iniciar reanimación.", "#c0392b"

    conn = sqlite3.connect('neonatos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO registros (nombre, puntaje, estado, diagnostico, fecha) VALUES (?, ?, ?, ?, ?)', 
                   (nombre, puntaje, estado, diag, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    return jsonify({'puntaje': puntaje, 'estado': estado, 'diagnostico': diag, 'color': color})

# FUNCIÓN MEJORADA PARA ABRIR EL NAVEGADOR
def open_browser():
    time.sleep(2) # Espera 2 segundos exactos
    url = "http://127.0.0.1:5000"
    webbrowser.open(url, new=2) # Fuerza la apertura en pestaña nueva

if __name__ == '__main__':
    init_db()
    # Iniciamos el hilo para abrir el navegador antes de arrancar Flask
    threading.Thread(target=open_browser).start()
    # Ejecutamos Flask sin el modo "reloader" (esto es clave para que no abra dos veces)
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)