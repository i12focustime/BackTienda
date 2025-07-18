from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_db_connection, crear_tabla

app = Flask(__name__)
CORS(app)

# Asegurarse que la tabla existe
crear_tabla()

@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    productos_lista = [dict(prod) for prod in productos]
    return jsonify(productos_lista)

@app.route('/productos', methods=['POST'])
def agregar_producto():
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
        "INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)",
        (nombre, precio, imagen)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Producto agregado'}), 201

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    filas_afectadas = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if filas_afectadas == 0:
        return jsonify({'error': 'Producto no encontrado'}), 404
    return jsonify({'mensaje': 'Producto eliminado'}), 200

if __name__ == '__main__':
    app.run(debug=True)
