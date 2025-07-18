import os
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de conexión desde variables de entorno
db_config = {
    'host': os.getenv('DB_HOST', 'sql302.infinityfree.com'),
    'user': os.getenv('DB_USER', 'if0_39499590'),
    'password': os.getenv('DB_PASSWORD', 'I12focustime'),  # Default pero mejor no dejar la real aquí
    'database': os.getenv('DB_NAME', 'if0_39499590_XXX')
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

if __name__ == '__main__':
    app.run(debug=True)

