import firebird.driver as fb

saved_connections = []
active_connection = None
active_cursor = None


def connect(host, port, database, user, password):
    global active_connection, active_cursor
    dsn = f"{host}/{port}:{database}"
    con = fb.connect(database=dsn, user=user, password=password)
    active_connection = con
    active_cursor = con.cursor()
    return con


def save_connection(name, host, port, database, user, password):
    for c in saved_connections:
        if c["name"] == name:
            return False
    saved_connections.append({
        "name": name,
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password
    })
    return True


def get_saved_connections():
    return saved_connections


def execute_query(sql, params=None):
    if active_cursor is None:
        return None
    if params:
        active_cursor.execute(sql, params)
    else:
        active_cursor.execute(sql)
    try:
        rows = active_cursor.fetchall()
        columns = [desc[0] for desc in active_cursor.description]
        return columns, rows
    except Exception:
        active_connection.commit()
        return None


def close_connection():
    global active_connection, active_cursor
    if active_cursor:
        active_cursor.close()
    if active_connection:
        active_connection.close()
    active_connection = None
    active_cursor = None
