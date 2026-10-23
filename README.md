# 🚌 RutasPython

API REST para gestionar rutas de transporte público (buses, trufis y micros) con sus coordenadas GPS. Está hecha con **Flask** y **PostgreSQL**, y se incluye una interfaz web para visualizar y editar las rutas sobre un mapa.

## ✨ Características

- CRUD completo de rutas de transporte.
- Coordenadas GPS ordenadas por secuencia para dibujar el recorrido de cada ruta.
- Tipos de ruta: `bus`, `trufi` y `micro`.
- Eliminación lógica (*soft delete*): las rutas se marcan como inactivas, no se borran.
- Búsqueda por nombre o descripción (sin distinguir mayúsculas).
- Filtro por tipo de ruta y endpoint de estadísticas.
- Endpoint de salud (`/api/health`) para verificar la conexión a la base de datos.
- CORS habilitado para consumir la API desde el frontend.
- Listo para desplegar con `gunicorn` (incluye `Procfile` y `runtime.txt`).

## 🧰 Tecnologías

| Componente | Tecnología |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| Base de datos | PostgreSQL (psycopg2) |
| Servidor de producción | Gunicorn |
| Frontend | HTML (`index.html`, `mapa_editor.html`) |

## 📁 Estructura del proyecto

```
RutasPython/
├── main.py                    # API Flask (endpoints)
├── script.py                  # Script auxiliar
├── postgresql.sql             # Creación de tablas, vista y datos
├── index.html                 # Interfaz web
├── mapa_editor.html           # Editor de rutas sobre el mapa
├── documentacion.md           # Documentación detallada de la API
├── conexionUtf8_problema.md   # Notas sobre problemas de codificación UTF-8
├── requirements.txt           # Dependencias de Python
├── runtime.txt                # Versión de Python para el despliegue
└── Procfile                   # Comando de arranque para despliegue
```

## 🚀 Instalación

### Requisitos previos

- Python 3.7 o superior
- PostgreSQL 12 o superior

### Pasos

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/Yoel-Cristian-Quispe-Diaz/RutasPython.git
   cd RutasPython
   ```

2. **Crear y activar un entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear la base de datos**

   ```bash
   psql -U postgres -c "CREATE DATABASE transport_routes WITH ENCODING 'UTF8';"
   psql -U postgres -d transport_routes -f postgresql.sql
   ```

## ⚙️ Configuración

La conexión a la base de datos se configura con **variables de entorno**:

| Variable | Descripción | Obligatoria |
|---|---|---|
| `DB_HOST` | Servidor de PostgreSQL | Sí |
| `DB_NAME` | Nombre de la base de datos | Sí |
| `DB_USER` | Usuario de PostgreSQL | Sí |
| `DB_PASSWORD` | Contraseña | Sí |
| `DB_PORT` | Puerto (por defecto `5432`) | No |

Ejemplo en Linux / macOS:

```bash
export DB_HOST=localhost
export DB_NAME=transport_routes
export DB_USER=postgres
export DB_PASSWORD=tu_password
export DB_PORT=5432
```

En Windows (PowerShell):

```powershell
$env:DB_HOST="localhost"
$env:DB_NAME="transport_routes"
$env:DB_USER="postgres"
$env:DB_PASSWORD="tu_password"
```

> ⚠️ Nunca subas tus credenciales al repositorio.

## ▶️ Ejecución

**Desarrollo:**

```bash
flask --app main run --debug
```

**Producción (Gunicorn):**

```bash
gunicorn main:app
```

La API quedará disponible en `http://localhost:5000/api` (puerto por defecto de Flask).

## 🌐 Endpoints

URL base: `http://localhost:5000/api`

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/routes` | Lista todas las rutas con sus coordenadas |
| `GET` | `/routes/{nombre}` | Obtiene una ruta por nombre exacto |
| `GET` | `/routes/{id}` | Obtiene una ruta por ID |
| `GET` | `/routes/type/{tipo}` | Lista rutas por tipo (`bus`, `trufi`, `micro`) |
| `GET` | `/routes/search?q={texto}` | Busca en nombre y descripción |
| `GET` | `/routes/stats` | Estadísticas generales de las rutas |
| `POST` | `/routes` | Crea una nueva ruta |
| `PUT` | `/routes/{id}` | Actualiza una ruta (campos opcionales) |
| `DELETE` | `/routes/{id}` | Desactiva una ruta (*soft delete*) |
| `GET` | `/health` | Estado de la API y de la base de datos |

### Crear una ruta

`POST /api/routes`

```json
{
  "name": "trufi_linea_a",
  "description": "Trufi Línea A - Centro a Pampa",
  "route_type": "trufi",
  "is_active": true,
  "coordinates": [
    { "lat": -21.993376, "lng": -63.683664 },
    { "lat": -21.994376, "lng": -63.684664 }
  ]
}
```

- **Obligatorios:** `name` (único) y `coordinates`.
- **Opcionales:** `description`, `route_type` (por defecto `bus`) e `is_active` (por defecto `true`).
- El campo `order` de cada coordenada se asigna automáticamente.

### Ejemplos con `curl`

```bash
# Estado de la API
curl http://localhost:5000/api/health

# Todas las rutas
curl http://localhost:5000/api/routes

# Rutas de tipo bus
curl http://localhost:5000/api/routes/type/bus

# Buscar rutas
curl "http://localhost:5000/api/routes/search?q=centro"

# Actualizar solo la descripción
curl -X PUT http://localhost:5000/api/routes/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Nueva descripción"}'
```

### Respuesta de ejemplo

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
        { "lat": -21.993376, "lng": -63.683664, "order": 1 }
      ]
    }
  ],
  "total": 1
}
```

### Códigos de respuesta

| Código | Significado |
|---|---|
| `200` | Éxito |
| `201` | Recurso creado |
| `400` | Solicitud inválida (datos faltantes o tipo de ruta incorrecto) |
| `404` | Recurso no encontrado |
| `409` | Conflicto (la ruta ya existe) |
| `500` | Error interno del servidor |

## 🗄️ Base de datos

- **`routes`**: `id`, `name` (único), `description`, `route_type` (`bus` / `trufi` / `micro`), `is_active`, `created_at`, `updated_at`.
- **`route_coordinates`**: `id`, `route_id` (clave foránea), `latitude`, `longitude`, `sequence_order`, `created_at`.
- **`route_details`** (vista): combina cada ruta con sus coordenadas en formato JSON.

## ☁️ Despliegue

El proyecto incluye `Procfile` y `runtime.txt`, por lo que puede desplegarse en plataformas como Heroku o Render. Solo configura las variables de entorno `DB_*` en el panel de la plataforma y apunta a una base de datos PostgreSQL.

## 📚 Más documentación

Consulta [`documentacion.md`](documentacion.md) para el detalle completo de cada endpoint y [`conexionUtf8_problema.md`](conexionUtf8_problema.md) si tienes problemas con acentos o caracteres especiales.

## 👤 Autor

**Yoel Cristian Quispe Diaz** — [@Yoel-Cristian-Quispe-Diaz](https://github.com/Yoel-Cristian-Quispe-Diaz)
