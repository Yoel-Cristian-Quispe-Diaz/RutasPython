#!/usr/bin/env python3
"""
Script de diagnóstico para conexión PostgreSQL
Ejecuta este script por separado para diagnosticar problemas de conexión
"""

import sys

# Verificar si psycopg2 está instalado
try:
    import psycopg2
    from psycopg2 import Error
    print("✅ psycopg2 está instalado")
except ImportError as e:
    print("❌ ERROR: psycopg2 no está instalado")
    print("   Ejecuta: pip install psycopg2-binary")
    sys.exit(1)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'transport_routes',
    'user': 'postgres',     # Cambia esto por tu usuario
    'password': '12345',         # Cambia esto por tu contraseña
    'port': '5432'
}

def test_connection():
    print("🔍 Probando configuración de conexión:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Database: {DB_CONFIG['database']}")
    print(f"   User: {DB_CONFIG['user']}")
    print(f"   Port: {DB_CONFIG['port']}")
    print(f"   Password: {'[VACÍA]' if not DB_CONFIG['password'] else '[CONFIGURADA]'}")
    print()

    # Primero intentar conectar sin especificar base de datos
    print("🔗 Paso 1: Probando conexión básica a PostgreSQL...")
    try:
        basic_config = {
            'host': DB_CONFIG['host'],
            'user': DB_CONFIG['user'],
            'password': DB_CONFIG['password'],
            'port': DB_CONFIG['port'],
        }

        connection = psycopg2.connect(**basic_config)
        print("✅ Conexión básica exitosa!")

        cursor = connection.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        print(f"📊 PostgreSQL version: {version}")

        # Listar bases de datos disponibles
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
        databases = [row[0] for row in cursor.fetchall()]
        print(f"📋 Bases de datos disponibles: {databases}")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"❌ Error en conexión básica: {e}")
        print("Intentando soluciones alternativas...")

        # Intentar con diferentes configuraciones de codificación
        alt_configs = [
            {'host': DB_CONFIG['host'], 'user': DB_CONFIG['user'], 'password': DB_CONFIG['password'], 'port': DB_CONFIG['port']},
            {'host': DB_CONFIG['host'], 'user': DB_CONFIG['user'], 'password': DB_CONFIG['password'], 'port': DB_CONFIG['port'], 'options': '-c client_encoding=latin1'},
            {'host': DB_CONFIG['host'], 'user': DB_CONFIG['user'], 'password': DB_CONFIG['password'], 'port': DB_CONFIG['port'], 'options': '-c client_encoding=win1252'}
        ]

        for i, config in enumerate(alt_configs, 1):
            try:
                print(f"   Probando configuración alternativa {i}...")
                connection = psycopg2.connect(**config)
                print(f"   ✅ ¡Configuración alternativa {i} funcionó!")
                connection.close()
                break
            except Exception as alt_error:
                print(f"   ❌ Configuración alternativa {i} falló: {alt_error}")

        return

    # Paso 2: Probar conexión a la base de datos específica
    print("\n🔗 Paso 2: Probando conexión a transport_routes...")
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print("✅ ¡Conexión a transport_routes exitosa!")

        # Verificar si la base de datos tiene las tablas
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")

        if 'routes' in [table[0] for table in tables]:
            # Verificar si existen datos
            cursor.execute('SELECT COUNT(*) FROM routes')
            route_count = cursor.fetchone()[0]
            print(f"🛣️  Número de rutas: {route_count}")

        cursor.close()
        connection.close()
        print("✅ Todas las pruebas pasaron correctamente!")

    except psycopg2.OperationalError as e:
        error_msg = str(e)
        if "database" in error_msg and "does not exist" in error_msg:
            print("❌ La base de datos 'transport_routes' no existe")
            print("💡 Solución: Crear la base de datos")
            print("   1. Conéctate: psql -U postgres")
            print("   2. Ejecuta: CREATE DATABASE transport_routes WITH ENCODING 'UTF8';")
        else:
            print(f"❌ ERROR: {e}")

    except UnicodeDecodeError as e:
        print("❌ ERROR DE CODIFICACIÓN:")
        print(f"   {e}")
        print("💡 Soluciones:")
        print("   1. Reinstalar PostgreSQL con codificación UTF-8")
        print("   2. Configurar variables de entorno:")
        print("      SET PGCLIENTENCODING=UTF8")
        print("   3. Usar una conexión alternativa (ver más abajo)")

    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()

def check_environment():
    print("🔍 Verificando entorno...")

    # Verificar sistema operativo
    import platform
    print(f"   SO: {platform.system()} {platform.release()}")

    # Verificar Python
    print(f"   Python: {sys.version}")

    # Verificar psycopg2
    print(f"   psycopg2: {psycopg2.__version__}")

    print()

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO DE CONEXIÓN POSTGRESQL")
    print("=" * 50)

    check_environment()
    test_connection()

    print("\n💡 SOLUCIONES COMUNES:")
    print("1. Instalar psycopg2: pip install psycopg2-binary")
    print("2. Verificar PostgreSQL: sudo systemctl status postgresql")
    print("3. Crear base de datos: CREATE DATABASE transport_routes;")
    print("4. Configurar usuario/contraseña en DB_CONFIG")
    print("5. Verificar pg_hba.conf para autenticación")
