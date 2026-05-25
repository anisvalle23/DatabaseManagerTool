# Limitaciones y Consideraciones Técnicas - Firebird

## SGBD Utilizado
Firebird 4.0 — acceso directo vía system tables (RDB$*)

---

## 1. Tablespaces
Firebird no implementa el concepto de Tablespaces como Oracle o PostgreSQL.
En Firebird, cada base de datos es un único archivo `.fdb` en el sistema operativo.
No existe ninguna tabla de sistema equivalente a `DBA_TABLESPACES` o similar.
Por esta razón, la sección de Tablespaces en la herramienta muestra vacío y no aplica para este SGBD.

---

## 2. Paquetes (Packages)
Los paquetes existen en Firebird únicamente a partir de la versión 3.0.
Se consultan desde la tabla de sistema `RDB$PACKAGES`.
Si la base de datos es anterior a Firebird 3.0, esta sección estará vacía.

---

## 3. Usuarios
En Firebird 3.0 y superior, los usuarios se gestionan desde la tabla `SEC$USERS`.
En versiones anteriores, los usuarios se almacenaban en una base de datos de seguridad separada (`security3.fdb`) y no eran accesibles directamente por SQL de usuario.
Esta herramienta consulta `SEC$USERS`, por lo que requiere Firebird 3.0 o superior para listar usuarios.

---

## 4. Information Schema
Firebird no implementa el esquema estándar `information_schema`.
Toda la metadata se obtiene directamente desde las tablas de sistema propias de Firebird:

| Objeto            | System Table         |
|-------------------|----------------------|
| Tablas            | RDB$RELATIONS        |
| Vistas            | RDB$RELATIONS        |
| Columnas          | RDB$RELATION_FIELDS  |
| Procedimientos    | RDB$PROCEDURES       |
| Funciones         | RDB$FUNCTIONS        |
| Triggers          | RDB$TRIGGERS         |
| Índices           | RDB$INDICES          |
| Secuencias        | RDB$GENERATORS       |
| Paquetes          | RDB$PACKAGES         |
| Tipos de datos    | RDB$FIELDS           |

---

## 5. Generadores vs Secuencias
En Firebird, las secuencias se llaman "Generators" internamente y se almacenan en `RDB$GENERATORS`.
A partir de Firebird 3.0 se puede usar la sintaxis `CREATE SEQUENCE` como alias, pero internamente siguen siendo generadores.

---

## 6. Librerías prohibidas
Esta herramienta no utiliza ninguna librería de administración como SQLAlchemy, Dapper, Entity Framework o Hibernate.
La conexión se realiza directamente mediante el driver `firebirdsql` (wire protocol nativo de Firebird sobre TCP).
Todas las consultas de metadata son SQL directo sobre las tablas de sistema `RDB$*`.
