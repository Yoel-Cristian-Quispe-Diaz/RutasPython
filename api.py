from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2 import sql, Error
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'transport_routes',
    'user': 'postgres',  # Cambiar por tu usuario
    'password': '12345',  # Cambiar por tu contraseña
    'port': '5432'
}

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            return self.connection
        except Error as e:
            print(f"Error conectando a PostgreSQL: {e}")
            return None

    def disconnect(self):
        if self.connection:
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

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Usando la vista route_details que ya tienes creada
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

        # Convertir RealDictRow a diccionario normal
        routes_list = []
        for route in routes:
            route_dict = dict(route)
            # Las coordenadas ya vienen como JSON desde la vista
            routes_list.append(route_dict)

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': routes_list,
            'total': len(routes_list)
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

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE name = %s
        """

        cursor.execute(query, (route_name,))
        route = cursor.fetchone()

        if not route:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Ruta no encontrada'}), 404

        route_dict = dict(route)

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': route_dict
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

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE id = %s
        """

        cursor.execute(query, (route_id,))
        route = cursor.fetchone()

        if not route:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Ruta no encontrada'}), 404

        route_dict = dict(route)

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': route_dict
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

        # Validar que route_type sea válido
        valid_route_types = ['bus', 'trufi', 'micro']
        route_type = data.get('route_type', 'bus')
        if route_type not in valid_route_types:
            return jsonify({'error': f'Tipo de ruta inválido. Debe ser uno de: {valid_route_types}'}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        try:
            cursor = connection.cursor()

            # Insertar la ruta
            route_query = """
            INSERT INTO routes (name, description, route_type, is_active)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """

            route_values = (
                data['name'],
                data.get('description', ''),
                route_type,
                data.get('is_active', True)
            )

            cursor.execute(route_query, route_values)
            route_id = cursor.fetchone()[0]

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

        except psycopg2.IntegrityError as e:
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({'error': 'La ruta ya existe'}), 409

    except Error as e:
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    """Actualizar una ruta existente"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        try:
            cursor = connection.cursor()

            # Verificar que la ruta existe
            check_query = "SELECT id FROM routes WHERE id = %s"
            cursor.execute(check_query, (route_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return jsonify({'error': 'Ruta no encontrada'}), 404

            # Construir query de actualización dinámicamente
            update_fields = []
            update_values = []

            if 'name' in data:
                update_fields.append('name = %s')
                update_values.append(data['name'])

            if 'description' in data:
                update_fields.append('description = %s')
                update_values.append(data['description'])

            if 'route_type' in data:
                valid_route_types = ['bus', 'trufi', 'micro']
                if data['route_type'] not in valid_route_types:
                    cursor.close()
                    connection.close()
                    return jsonify({'error': f'Tipo de ruta inválido. Debe ser uno de: {valid_route_types}'}), 400
                update_fields.append('route_type = %s')
                update_values.append(data['route_type'])

            if 'is_active' in data:
                update_fields.append('is_active = %s')
                update_values.append(data['is_active'])

            if update_fields:
                update_values.append(route_id)
                update_query = f"UPDATE routes SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(update_query, update_values)

            # Si se enviaron coordenadas, actualizar también
            if 'coordinates' in data:
                # Eliminar coordenadas existentes
                cursor.execute("DELETE FROM route_coordinates WHERE route_id = %s", (route_id,))

                # Insertar nuevas coordenadas
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
                'message': 'Ruta actualizada exitosamente'
            })

        except psycopg2.IntegrityError as e:
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({'error': 'Conflicto de datos (posible nombre duplicado)'}), 409

    except Error as e:
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    """Eliminar una ruta (soft delete)"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor()

        # Verificar que la ruta existe
        check_query = "SELECT id FROM routes WHERE id = %s"
        cursor.execute(check_query, (route_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'error': 'Ruta no encontrada'}), 404

        # Soft delete (marcar como inactiva)
        update_query = "UPDATE routes SET is_active = FALSE WHERE id = %s"
        cursor.execute(update_query, (route_id,))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'message': 'Ruta eliminada exitosamente'
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/type/<route_type>', methods=['GET'])
def get_routes_by_type(route_type):
    """Obtener rutas por tipo (bus, trufi, micro)"""
    try:
        # Validar tipo de ruta
        valid_route_types = ['bus', 'trufi', 'micro']
        if route_type not in valid_route_types:
            return jsonify({'error': f'Tipo de ruta inválido. Debe ser uno de: {valid_route_types}'}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE route_type = %s
        ORDER BY name
        """

        cursor.execute(query, (route_type,))
        routes = cursor.fetchall()

        routes_list = []
        for route in routes:
            route_dict = dict(route)
            routes_list.append(route_dict)

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': routes_list,
            'total': len(routes_list),
            'route_type': route_type
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

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        query = """
        SELECT
            id,
            name,
            description,
            route_type,
            is_active,
            coordinates
        FROM route_details
        WHERE (name ILIKE %s OR description ILIKE %s)
        ORDER BY name
        """

        search_pattern = f'%{search_term}%'
        cursor.execute(query, (search_pattern, search_pattern))
        routes = cursor.fetchall()

        routes_list = []
        for route in routes:
            route_dict = dict(route)
            routes_list.append(route_dict)

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': routes_list,
            'total': len(routes_list),
            'search_term': search_term
        })

    except Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/api/routes/stats', methods=['GET'])
def get_routes_stats():
    """Obtener estadísticas de las rutas"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Estadísticas generales
        stats_query = """
        SELECT
            COUNT(*) as total_routes,
            COUNT(*) FILTER (WHERE is_active = TRUE) as active_routes,
            COUNT(*) FILTER (WHERE is_active = FALSE) as inactive_routes,
            COUNT(*) FILTER (WHERE route_type = 'bus') as bus_routes,
            COUNT(*) FILTER (WHERE route_type = 'trufi') as trufi_routes,
            COUNT(*) FILTER (WHERE route_type = 'micro') as micro_routes
        FROM routes
        """

        cursor.execute(stats_query)
        stats = dict(cursor.fetchone())

        # Promedio de coordenadas por ruta
        avg_query = """
        SELECT AVG(coord_count) as avg_coordinates_per_route
        FROM (
            SELECT COUNT(*) as coord_count
            FROM route_coordinates
            GROUP BY route_id
        ) as route_coord_counts
        """

        cursor.execute(avg_query)
        avg_result = cursor.fetchone()
        stats['avg_coordinates_per_route'] = float(avg_result['avg_coordinates_per_route']) if avg_result['avg_coordinates_per_route'] else 0

        cursor.close()
        connection.close()

        return jsonify({
            'success': True,
            'data': stats
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
            cursor = connection.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchone()
            cursor.close()
            connection.close()
            return jsonify({
                'status': 'OK',
                'database': 'Connected',
                'database_type': 'PostgreSQL',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'Error',
                'database': 'Disconnected',
                'database_type': 'PostgreSQL',
                'timestamp': datetime.now().isoformat()
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'Error',
            'error': str(e),
            'database_type': 'PostgreSQL',
            'timestamp': datetime.now().isoformat()
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método no permitido'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
