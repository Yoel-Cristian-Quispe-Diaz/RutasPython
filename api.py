from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'transport_routes',
    'user': 'root',  # Cambiar por tu usuario
    'password': '',  # Cambiar por tu contraseña
    'charset': 'utf8mb4'
}

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            return self.connection
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

def get_db_connection():
    db = DatabaseConnection()
    return db.connect()

@app.route('/api/routes', methods=['GET'])
def get_all_routes():
    """Obtener todas las rutas con sus coordenadas"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(dictionary=True)

        # Consulta optimizada usando la vista
        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        ORDER BY name
        """

        cursor.execute(query)
        routes = cursor.fetchall()

        # Procesar las coordenadas JSON
        for route in routes:
            if route['coordinates']:
                route['coordinates'] = json.loads(route['coordinates'])
            else:
                route['coordinates'] = []

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': routes,
            'total': len(routes)
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/<route_name>', methods=['GET'])
def get_route_by_name(route_name):
    """Obtener una ruta específica por nombre"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE name = %s AND is_active = TRUE
        """

        cursor.execute(query, (route_name,))
        route = cursor.fetchone()

        if not route:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Ruta no encontrada'}), 404

        # Procesar las coordenadas JSON
        if route['coordinates']:
            route['coordinates'] = json.loads(route['coordinates'])
        else:
            route['coordinates'] = []

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': route
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/<int:route_id>', methods=['GET'])
def get_route_by_id(route_id):
    """Obtener una ruta específica por ID"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE id = %s AND is_active = TRUE
        """

        cursor.execute(query, (route_id,))
        route = cursor.fetchone()

        if not route:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Ruta no encontrada'}), 404

        # Procesar las coordenadas JSON
        if route['coordinates']:
            route['coordinates'] = json.loads(route['coordinates'])
        else:
            route['coordinates'] = []

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': route
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes', methods=['POST'])
def create_route():
    """Crear nueva ruta con coordenadas"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400

        required_fields = ['name', 'coordinates']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor()

        # Insertar la ruta
        route_query = """
        INSERT INTO routes (name, description, route_type, is_active)
        VALUES (%s, %s, %s, %s)
        """

        route_values = (
            data['name'],
            data.get('description', ''),
            data.get('route_type', 'bus'),
            data.get('is_active', True)
        )

        cursor.execute(route_query, route_values)
        route_id = cursor.lastrowid

        # Insertar las coordenadas
        coordinates_query = """
        INSERT INTO route_coordinates (route_id, latitude, longitude, sequence_order)
        VALUES (%s, %s, %s, %s)
        """

        for i, coord in enumerate(data['coordinates'], 1):
            coord_values = (route_id, coord['lat'], coord['lng'], i)
            cursor.execute(coordinates_query, coord_values)

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'message': 'Ruta creada exitosamente',
            'route_id': route_id
        }), 201

    except mysql.connector.IntegrityError as e:
        return jsonify({'error': 'La ruta ya existe'}), 409
    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/type/<route_type>', methods=['GET'])
def get_routes_by_type(route_type):
    """Obtener rutas por tipo (bus, trufi, micro)"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE route_type = %s AND is_active = TRUE
        ORDER BY name
        """

        cursor.execute(query, (route_type,))
        routes = cursor.fetchall()

        # Procesar las coordenadas JSON
        for route in routes:
            if route['coordinates']:
                route['coordinates'] = json.loads(route['coordinates'])
            else:
                route['coordinates'] = []

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': routes,
            'total': len(routes)
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/search', methods=['GET'])
def search_routes():
    """Buscar rutas por nombre o descripción"""
    try:
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'error': 'Parámetro de búsqueda requerido'}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE (name LIKE %s OR description LIKE %s) AND is_active = TRUE
        ORDER BY name
        """

        search_pattern = f'%{search_term}%'
        cursor.execute(query, (search_pattern, search_pattern))
        routes = cursor.fetchall()

        # Procesar las coordenadas JSON
        for route in routes:
            if route['coordinates']:
                route['coordinates'] = json.loads(route['coordinates'])
            else:
                route['coordinates'] = []

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': routes,
            'total': len(routes),
            'search_term': search_term
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar el estado de la API"""
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
            return jsonify({
                'status': 'OK',
                'database': 'Connected',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'Error',
                'database': 'Disconnected',
                'timestamp': datetime.now().isoformat()
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'Error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
