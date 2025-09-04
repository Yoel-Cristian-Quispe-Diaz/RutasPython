
# API de Rutas de Transporte - Documentación

API RESTful para gestionar rutas de transporte público (autobuses, trufis, micros) con coordenadas GPS en PostgreSQL.

## 📋 Tabla de Contenidos

- [Instalación](#instalación)
- [Configuración](#configuración)
- [Endpoints](#endpoints)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Códigos de Error](#códigos-de-error)
- [Estructura de Datos](#estructura-de-datos)

## 🚀 Instalación

### Prerrequisitos

- Python 3.7+
- PostgreSQL 12+

### Pasos de instalación

1. **Clonar o descargar los archivos del proyecto**

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar PostgreSQL**
   ```sql
   -- Crear la base de datos
   CREATE DATABASE transport_routes WITH ENCODING 'UTF8';

   -- Ejecutar el script SQL de creación de tablas
   psql -U postgres -d transport_routes -f transport_routes_postgresql.sql
   ```

## ⚙️ Configuración

Editar las credenciales de la base de datos en el archivo principal:

```python
DB_CONFIG = {
    'host': 'localhost',        # Servidor de PostgreSQL
    'database': 'transport_routes',  # Nombre de la base de datos
    'user': 'postgres',         # Usuario de PostgreSQL
    'password': 'tu_password',  # Contraseña
    'port': '5432'             # Puerto (por defecto 5432)
}
```

## 🌐 Endpoints

### Base URL
```
http://localhost:5000/api
```

### 1. Obtener todas las rutas
```http
GET /routes
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "ruta_2_ida",
      "description": "Ruta 1 dirección ida",
      "route_type": "bus",
      "is_active": true,
      "coordinates": [
        {
          "lat": -21.993376,
          "lng": -63.683664,
          "order": 1
        }
      ]
    }
  ],
  "total": 1
}
```

### 2. Obtener ruta por nombre
```http
GET /routes/{route_name}
```

**Parámetros:**
- `route_name` (string): Nombre exacto de la ruta

**Ejemplo:**
```http
GET /routes/ruta_2_ida
```

### 3. Obtener ruta por ID
```http
GET /routes/{route_id}
```

**Parámetros:**
- `route_id` (integer): ID único de la ruta

**Ejemplo:**
```http
GET /routes/1
```

### 4. Crear nueva ruta
```http
POST /routes
```

**Body (JSON):**
```json
{
  "name": "nueva_ruta",
  "description": "Descripción de la ruta",
  "route_type": "bus",
  "is_active": true,
  "coordinates": [
    {
      "lat": -21.993376,
      "lng": -63.683664
    },
    {
      "lat": -21.994376,
      "lng": -63.684664
    }
  ]
}
```

**Campos obligatorios:**
- `name` (string): Nombre único de la ruta
- `coordinates` (array): Array de objetos con lat/lng

**Campos opcionales:**
- `description` (string): Descripción de la ruta
- `route_type` (enum): "bus", "trufi", "micro" (default: "bus")
- `is_active` (boolean): Estado activo/inactivo (default: true)

### 5. Actualizar ruta
```http
PUT /routes/{route_id}
```

**Body (JSON):**
```json
{
  "name": "nombre_actualizado",
  "description": "Nueva descripción",
  "route_type": "trufi",
  "is_active": false,
  "coordinates": [
    {
      "lat": -21.993376,
      "lng": -63.683664
    }
  ]
}
```

**Nota:** Todos los campos son opcionales. Solo se actualizarán los campos enviados.

### 6. Eliminar ruta (Soft Delete)
```http
DELETE /routes/{route_id}
```

**Nota:** La ruta no se elimina físicamente, solo se marca como `is_active = false`.

### 7. Obtener rutas por tipo
```http
GET /routes/type/{route_type}
```

**Parámetros:**
- `route_type` (enum): "bus", "trufi" o "micro"

**Ejemplo:**
```http
GET /routes/type/bus
```

### 8. Buscar rutas
```http
GET /routes/search?q={search_term}
```

**Parámetros de consulta:**
- `q` (string): Término de búsqueda (busca en nombre y descripción)

**Ejemplo:**
```http
GET /routes/search?q=trufi
```

**Nota:** La búsqueda es case-insensitive.

### 9. Estado de la API
```http
GET /health
```

**Respuesta:**
```json
{
  "status": "OK",
  "database": "Connected",
  "db_version": "PostgreSQL 14.9...",
  "timestamp": "2025-09-04T10:30:00"
}
```

## 📝 Ejemplos de Uso

### Crear una nueva ruta de trufi

```bash
curl -X POST http://localhost:5000/api/routes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "trufi_linea_a",
    "description": "Trufi Línea A - Centro a Pampa",
    "route_type": "trufi",
    "coordinates": [
      {"lat": -21.993376, "lng": -63.683664},
      {"lat": -21.994376, "lng": -63.684664},
      {"lat": -21.995376, "lng": -63.685664}
    ]
  }'
```

### Buscar rutas que contengan "centro"

```bash
curl "http://localhost:5000/api/routes/search?q=centro"
```

### Obtener todas las rutas de tipo "bus"

```bash
curl "http://localhost:5000/api/routes/type/bus"
```

### Actualizar solo la descripción de una ruta

```bash
curl -X PUT http://localhost:5000/api/routes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Nueva descripción actualizada"
  }'
```

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | Éxito |
| 201 | Creado exitosamente |
| 400 | Solicitud incorrecta (datos faltantes o inválidos) |
| 404 | Recurso no encontrado |
| 409 | Conflicto (ruta ya existe o error de integridad) |
| 500 | Error interno del servidor |

### Formato de respuesta de error

```json
{
  "error": "Descripción del error"
}
```

## 📊 Estructura de Datos

### Objeto Ruta

```json
{
  "id": 1,
  "name": "nombre_ruta",
  "description": "Descripción opcional",
  "route_type": "bus|trufi|micro",
  "is_active": true,
  "coordinates": [
    {
      "lat": -21.993376,
      "lng": -63.683664,
      "order": 1
    }
  ]
}
```

### Tipos de Ruta

- `bus`: Autobús urbano
- `trufi`: Trufi (minibús compartido)
- `micro`: Micro (autobús pequeño)

### Coordenadas

Las coordenadas se almacenan como puntos GPS en formato decimal:
- `lat` (latitude): Coordenada de latitud (-90 a 90)
- `lng` (longitude): Coordenada de longitud (-180 a 180)
- `order`: Orden secuencial en la ruta (automático)

## 🔧 Estructura de la Base de Datos

### Tabla: routes
- `id` (SERIAL PRIMARY KEY)
- `name` (VARCHAR(100) UNIQUE NOT NULL)
- `description` (TEXT)
- `route_type` (ENUM: bus, trufi, micro)
- `is_active` (BOOLEAN DEFAULT TRUE)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Tabla: route_coordinates
- `id` (SERIAL PRIMARY KEY)
- `route_id` (INTEGER FOREIGN KEY)
- `latitude` (DECIMAL(10,6))
- `longitude` (DECIMAL(10,6))
- `sequence_order` (INTEGER)
- `created_at` (TIMESTAMP)

### Vista: route_details
Vista optimizada que combina rutas con sus coordenadas en formato JSON.

## 🚀 Ejecución

Para iniciar la API:

```bash
python app.py
```

La API estará disponible en: `http://localhost:5000`

Para modo de producción, considera usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🛠️ Desarrollo

### Variables de entorno recomendadas

```bash
export FLASK_ENV=development  # Para desarrollo
export FLASK_ENV=production   # Para producción
export DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Testing

Para probar todos los endpoints:

```bash
# Verificar estado
curl http://localhost:5000/api/health

# Obtener todas las rutas
curl http://localhost:5000/api/routes

# Crear ruta de prueba
curl -X POST http://localhost:5000/api/routes \
  -H "Content-Type: application/json" \
  -d '{"name":"test_route","coordinates":[{"lat":-21.5,"lng":-63.2}]}'
```

## 📞 Soporte

Para reportar problemas o sugerencias, revisa:
- Los logs de la aplicación
- La conectividad a PostgreSQL
- Los permisos de la base de datos
- La sintaxis de las consultas JSON
