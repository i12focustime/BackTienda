import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de conexión usando variables de entorno
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(productos)

@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    nombre = data.get('nombre')
    precio = data.get('precio')
    imagen = data.get('imagen')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, imagen) VALUES (%s, %s, %s)",
        (nombre, precio, imagen)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Producto agregado'}), 201

@app.route('/check-env')
def check_env():
    return {
        'DB_HOST': os.environ.get('DB_HOST', 'No definido'),
        'DB_USER': os.environ.get('DB_USER', 'No definido'),
        'DB_NAME': os.environ.get('DB_NAME', 'No definido')
    }
@app.route('/productos', methods=['POST'])
def agregar_producto():
    if not request.is_json:
        return jsonify({'error': 'Se esperaba JSON'}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido o vacío'}), 400

    nombre = data.get('nombre')
    precio = data.get('precio')
    imagen = data.get('imagen')

    if not nombre or not precio or not imagen:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, imagen) VALUES (%s, %s, %s)",
        (nombre, precio, imagen)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Producto agregado'}), 201

if __name__ == '__main__':
    app.run(debug=True)
