# API de Rutas de Transporte

Una API REST completa para gestionar rutas de transporte público con coordenadas GPS.

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.7+
- MySQL 5.7+ o MariaDB 10.2+
- pip

### Instalación

1. **Clonar e instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar la base de datos:**
```bash
python data_loader.py
```

3. **Ejecutar la API:**
```bash
python transport_api.py
```

La API estará disponible en `http://localhost:5000`

## 🗃️ Estructura de la Base de Datos

### Tabla `routes`
- `id`: ID único de la ruta
- `name`: Nombre de la ruta (único)
- `description`: Descripción de la ruta
- `route_type`: Tipo de ruta (bus, trufi, micro)
- `is_active`: Estado activo/inactivo
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

### Tabla `route_coordinates`
- `id`: ID único de la coordenada
- `route_id`: ID de la ruta (FK)
- `latitude`: Latitud
- `longitude`: Longitud
- `sequence_order`: Orden en la secuencia
- `created_at`: Fecha de creación

## 📊 Endpoints de la API

### 1. Obtener todas las rutas
```http
GET /api/routes
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "ruta_1_ida",
      "description": "Ruta 1 dirección ida",
      "route_type": "bus",
      "is_active": true,
      "coordinates": [
        {
          "lat": -21.993376,
          "lng": -63.683664,
          "order": 1
        },
        {
          "lat": -21.992982,
          "lng": -63.686455,
          "order": 2
        }
      ]
    }
  ],
  "total": 8
}
```

### 2. Obtener ruta por nombre
```http
GET /api/routes/{route_name}
```

**Ejemplo:**
```http
GET /api/routes/ruta_1_ida
```

### 3. Obtener ruta por ID
```http
GET /api/routes/{route_id}
```

**Ejemplo:**
```http
GET /api/routes/1
```

### 4. Crear nueva ruta
```http
POST /api/routes
Content-Type: application/json
```

**Body:**
```json
{
  "name": "ruta_3_ida",
  "description": "Nueva ruta 3 ida",
  "route_type": "bus",
  "coordinates": [
    {
      "lat": -21.990000,
      "lng": -63.680000
    },
    {
      "lat": -21.995000,
      "lng": -63.685000
    }
  ]
}
```

### 5. Obtener rutas por tipo
```http
GET /api/routes/type/{route_type}
```

**Tipos disponibles:** `bus`, `trufi`, `micro`

**Ejemplo:**
```http
GET /api/routes/type/trufi
```

### 6. Buscar rutas
```http
GET /api/routes/search?q={search_term}
```

**Ejemplo:**
```http
GET /api/routes/search?q=trufi
```

### 7. Health Check
```http
GET /api/health
```

## 🔧 Configuración de la Base de Datos

Edita la configuración en `transport_api.py` y `data_loader.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'transport_routes',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'charset': 'utf8mb4'
}
```

## 📝 Ejemplos de Uso

### Python
```python
import requests

# Obtener todas las rutas
response = requests.get('http://localhost:5000/api/routes')
routes = response.json()

# Obtener ruta específica
response = requests.get('http://localhost:5000/api/routes/ruta_1_ida')
route = response.json()

# Crear nueva ruta
new_route = {
    "name": "ruta_nueva",
    "description": "Nueva ruta de ejemplo",
    "route_type": "bus",
    "coordinates": [
        {"lat": -21.990000, "lng": -63.680000},
        {"lat": -21.995000, "lng": -63.685000}
    ]
}

response = requests.post(
    'http://localhost:5000/api/routes',
    json=new_route
)
```

### JavaScript/Fetch
```javascript
// Obtener todas las rutas
fetch('http://localhost:5000/api/routes')
  .then(response => response.json())
  .then(data => console.log(data));

// Crear nueva ruta
const newRoute = {
  name: "ruta_nueva",
  description: "Nueva ruta de ejemplo",
  route_type: "bus",
  coordinates: [
    {lat: -21.990000, lng: -63.680000},
    {lat: -21.995000, lng: -63.685000}
  ]
};

fetch('http://localhost:5000/api/routes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(newRoute)
});
```

### cURL
```bash
# Obtener todas las rutas
curl http://localhost:5000/api/routes

# Obtener ruta específica
curl http://localhost:5000/api/routes/ruta_1_ida

# Crear nueva ruta
curl -X POST http://localhost:5000/api/routes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ruta_nueva",
    "description": "Nueva ruta de ejemplo",
    "route_type": "bus",
    "coordinates": [
      {"lat": -21.990000, "lng": -63.680000},
      {"lat": -21.995000, "lng": -63.685000}
    ]
  }'
```

## 🛠️ Funciones Utilitarias

El archivo `data_loader.py` incluye funciones útiles:

### Agregar coordenadas a una ruta existente
```python
from data_loader import add_coordinates_to_route

coordinates = [
    {'lat': -21.990000, 'lng': -63.680000},
    {'lat': -21.995000, 'lng': -63.685000}
]

add_coordinates_to_route('trufi_A', coordinates)
```

### Exportar todas las rutas a JSON
```python
from data_loader import export_routes_to_json

export_routes_to_json()  # Crea archivo 'routes_export.json'
```

## 📋 Rutas Predefinidas

La API viene con estas rutas configuradas:

1. **ruta_1_ida** - Ruta 1 dirección ida (47 coordenadas)
2. **ruta_1_vuelta** - Ruta 1 dirección vuelta
3. **ruta_2_ida** - Ruta 2 dirección ida
4. **ruta_2_vuelta** - Ruta 2 dirección vuelta
5. **trufi_A** - Línea de trufi A
6. **trufi_B** - Línea de trufi B
7. **trufi_C** - Línea de trufi C
8. **trufi_D** - Línea de trufi D

## 🚦 Códigos de Estado HTTP

- `200` - Éxito
- `201` - Creado exitosamente
- `400` - Solicitud incorrecta
- `404` - No encontrado
- `409` - Conflicto (ruta ya existe)
- `500` - Error interno del servidor

## 🔐 CORS

La API tiene CORS habilitado para permitir solicitudes desde cualquier origen. En producción, considera configurar orígenes específicos.

## 📊 Formato de Respuesta

Todas las respuestas siguen este formato:

```json
{
  "success": true/false,
  "data": {...},
  "total": number,
  "error": "mensaje de error (si aplica)"
}
```

## 🚀 Despliegue en Producción

Para producción, considera:

1. Usar un servidor WSGI como Gunicorn
2. Configurar HTTPS
3. Usar variables de entorno para configuración
4. Implementar autenticación/autorización
5. Configurar logging adecuado
6. Usar un proxy reverso como Nginx