# Database Manager Tool - Firebird

Herramienta administrativa de base de datos desarrollada como proyecto universitario para la clase de Teoría de Base de Datos II. Permite administrar los principales objetos de una base de datos Firebird interactuando directamente con las tablas de sistema (system tables) del SGBD, sin el uso de ORMs ni information_schema.

---

## Tecnologías Utilizadas

- **Python 3.14**
- **PyQt6** — Interfaz gráfica de escritorio
- **firebirdsql** — Driver de conexión nativo a Firebird vía protocolo TCP (wire protocol), sin necesidad de librerías nativas instaladas en el sistema operativo

---

## Requisitos

- Python 3.10 o superior
- Firebird 3.0 o superior corriendo (local o en Docker)
- Entorno virtual de Python

---

## Instalación y Ejecución

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd DatabaseManagerTool

# Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install PyQt6 firebirdsql

# Correr la aplicación
python3 main.py
```

---

## Estructura del Proyecto

```
DatabaseManagerTool/
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias del proyecto
├── LIMITACIONES.md              # Limitaciones técnicas del SGBD
├── README.md                    # Este archivo
├── database/
│   ├── __init__.py
│   ├── connection.py            # Gestión de conexiones a Firebird
│   └── queries.py               # Queries directas a system tables RDB$*
└── ui/
    ├── __init__.py
    ├── login_window.py          # Ventana de login y gestión de conexiones
    ├── main_window.py           # Ventana principal con árbol de objetos
    ├── create_table_dialog.py   # Diálogo visual para crear tablas
    └── create_view_dialog.py    # Diálogo visual para crear vistas
```

---

## Cumplimiento de la Rúbrica

### 1. Gestión de Conexiones y Autenticación — 10 pts
- El usuario puede iniciar sesión con cualquier usuario válido de Firebird (SYSDBA u otro)
- Se pueden guardar múltiples conexiones con nombre, host, puerto, base de datos, usuario y contraseña
- Al hacer click en una conexión guardada se cargan los datos automáticamente en el formulario
- La conexión se realiza mediante `firebirdsql.connect()` con el wire protocol nativo de Firebird sobre TCP

### 2. Administración de Objetos de Base de Datos — 30 pts
Todos los objetos se listan consultando directamente las system tables de Firebird sin usar information_schema:

| Objeto | System Table utilizada | Filtro aplicado |
|---|---|---|
| Tablas | RDB$RELATIONS | RDB$VIEW_BLR IS NULL y RDB$SYSTEM_FLAG = 0 |
| Vistas | RDB$RELATIONS | RDB$VIEW_BLR IS NOT NULL y RDB$SYSTEM_FLAG = 0 |
| Procedimientos | RDB$PROCEDURES | RDB$SYSTEM_FLAG = 0 |
| Funciones | RDB$FUNCTIONS | RDB$SYSTEM_FLAG = 0 |
| Triggers | RDB$TRIGGERS | RDB$SYSTEM_FLAG = 0 |
| Índices | RDB$INDICES | RDB$SYSTEM_FLAG = 0 |
| Secuencias | RDB$GENERATORS | RDB$SYSTEM_FLAG = 0 |
| Usuarios | SEC$USERS | — |
| Paquetes | RDB$PACKAGES | RDB$SYSTEM_FLAG = 0 |

El filtro `RDB$SYSTEM_FLAG = 0` se aplica para mostrar únicamente los objetos creados por el usuario, excluyendo los objetos internos del sistema.

### 3. Operaciones sobre Objetos — 40 pts

**Creación visual de tablas:**
Al hacer click en "+ Nueva Tabla" se abre un formulario donde se puede definir el nombre de la tabla y agregar columnas con los siguientes atributos:
- Nombre de la columna
- Tipo de dato (INTEGER, VARCHAR, CHAR, DATE, TIMESTAMP, BOOLEAN, BLOB, NUMERIC, DECIMAL, entre otros)
- Longitud o precisión
- Escala (para tipos numéricos)
- Restricción NOT NULL

El formulario genera y muestra el DDL antes de ejecutarlo, y lo ejecuta directamente en la base de datos.

**Creación visual de vistas:**
Al hacer click en "+ Nueva Vista" se abre un formulario donde se define el nombre de la vista y la sentencia SELECT. El formulario genera el `CREATE VIEW` automáticamente.

**Generación de DDL desde metadata:**
Al hacer click en cualquier objeto del árbol se genera el DDL consultando las system tables:
- Para tablas: se leen RDB$RELATION_FIELDS y RDB$FIELDS para obtener columnas y tipos
- Para vistas: se lee RDB$VIEW_SOURCE de RDB$RELATIONS
- Para procedimientos: se lee RDB$PROCEDURE_SOURCE de RDB$PROCEDURES
- Para funciones: se lee RDB$FUNCTION_SOURCE de RDB$FUNCTIONS
- Para triggers: se lee RDB$TRIGGER_SOURCE de RDB$TRIGGERS

**Modificación mediante SQL:**
El botón "Modificar (Exportar DDL al editor SQL)" toma el DDL del objeto seleccionado y lo carga en el editor SQL para que el usuario lo edite y re-ejecute.

### 4. Ejecución de Sentencias SQL — 15 pts
- El editor SQL permite ejecutar cualquier sentencia SELECT mostrando los resultados en una tabla con columnas y filas
- También soporta sentencias DDL (CREATE, ALTER, DROP) y DML (INSERT, UPDATE, DELETE)
- Después de ejecutar una sentencia que modifica objetos, el árbol se recarga automáticamente

### 5. Consideraciones Técnicas y Restricciones — 5 pts
- No se utiliza `information_schema`
- No se utiliza ningún ORM (SQLAlchemy, Dapper, Entity Framework, Hibernate, etc.)
- Toda la metadata se obtiene mediante SQL directo sobre las system tables `RDB$*` de Firebird
- La aplicación es de tipo Desktop (PyQt6), no modo consola
- Las limitaciones del SGBD están documentadas en LIMITACIONES.md

---

## Funcionalidades Adicionales

- Diseño con colores burgundy, beige y dorado
- Árbol de objetos expandible por categoría
- Botón "Actualizar" para recargar el árbol sin reiniciar la app
- Mensajes de error descriptivos 
- Interfaz dividida con splitter ajustable entre el árbol y el panel principal
- Pestañas DDL y SQL en el panel derecho

---

## Limitaciones del SGBD

Ver archivo [LIMITACIONES.md](./LIMITACIONES.md) para el detalle completo de las limitaciones y diferencias de Firebird respecto a otros motores de base de datos.
