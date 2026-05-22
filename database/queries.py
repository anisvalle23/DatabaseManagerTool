import database.connection as db


def get_tables():
    sql = """
        SELECT TRIM(RDB$RELATION_NAME)
        FROM RDB$RELATIONS
        WHERE RDB$VIEW_BLR IS NULL
        AND (RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL)
        ORDER BY RDB$RELATION_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_views():
    sql = """
        SELECT TRIM(RDB$RELATION_NAME)
        FROM RDB$RELATIONS
        WHERE RDB$VIEW_BLR IS NOT NULL
        AND (RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL)
        ORDER BY RDB$RELATION_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_procedures():
    sql = """
        SELECT TRIM(RDB$PROCEDURE_NAME)
        FROM RDB$PROCEDURES
        WHERE RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL
        ORDER BY RDB$PROCEDURE_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_functions():
    sql = """
        SELECT TRIM(RDB$FUNCTION_NAME)
        FROM RDB$FUNCTIONS
        WHERE RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL
        ORDER BY RDB$FUNCTION_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_triggers():
    sql = """
        SELECT TRIM(RDB$TRIGGER_NAME)
        FROM RDB$TRIGGERS
        WHERE RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL
        ORDER BY RDB$TRIGGER_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_indexes():
    sql = """
        SELECT TRIM(RDB$INDEX_NAME), TRIM(RDB$RELATION_NAME)
        FROM RDB$INDICES
        WHERE RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL
        ORDER BY RDB$INDEX_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] + " (" + row[1] + ")" for row in result[1]]
    return []


def get_sequences():
    sql = """
        SELECT TRIM(RDB$GENERATOR_NAME)
        FROM RDB$GENERATORS
        WHERE RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL
        ORDER BY RDB$GENERATOR_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_users():
    sql = """
        SELECT TRIM(SEC$USER_NAME)
        FROM SEC$USERS
        ORDER BY SEC$USER_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_packages():
    sql = """
        SELECT TRIM(RDB$PACKAGE_NAME)
        FROM RDB$PACKAGES
        WHERE RDB$SYSTEM_FLAG = 0 OR RDB$SYSTEM_FLAG IS NULL
        ORDER BY RDB$PACKAGE_NAME
    """
    result = db.execute_query(sql)
    if result:
        return [row[0] for row in result[1]]
    return []


def get_table_ddl(table_name):
    sql = """
        SELECT TRIM(r.RDB$FIELD_NAME), f.RDB$FIELD_TYPE,
               f.RDB$FIELD_LENGTH, f.RDB$FIELD_PRECISION,
               f.RDB$FIELD_SCALE, r.RDB$NULL_FLAG
        FROM RDB$RELATION_FIELDS r
        JOIN RDB$FIELDS f ON r.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME
        WHERE r.RDB$RELATION_NAME = ?
        ORDER BY r.RDB$FIELD_POSITION
    """
    result = db.execute_query(sql, (table_name,))
    if not result:
        return ""

    type_map = {
        7: "SMALLINT",
        8: "INTEGER",
        9: "QUAD",
        10: "FLOAT",
        11: "D_FLOAT",
        12: "DATE",
        13: "TIME",
        14: "CHAR",
        16: "BIGINT",
        23: "BOOLEAN",
        24: "DECFLOAT",
        25: "DECFLOAT",
        26: "INT128",
        27: "DOUBLE PRECISION",
        28: "TIME WITH TIME ZONE",
        29: "TIMESTAMP WITH TIME ZONE",
        35: "TIMESTAMP",
        37: "VARCHAR",
        40: "CSTRING",
        45: "BLOB_ID",
        261: "BLOB"
    }

    columns = []
    for row in result[1]:
        col_name = row[0]
        type_code = row[1]
        length = row[2]
        precision = row[3]
        scale = row[4]
        not_null = row[5]

        type_name = type_map.get(type_code, f"TYPE_{type_code}")

        if type_code in (14, 37):
            type_str = f"{type_name}({length})"
        elif type_code == 8 and scale and scale < 0:
            type_str = f"NUMERIC({precision},{abs(scale)})"
        else:
            type_str = type_name

        null_str = " NOT NULL" if not_null else ""
        columns.append(f"    {col_name} {type_str}{null_str}")

    ddl = f"CREATE TABLE {table_name} (\n"
    ddl += ",\n".join(columns)
    ddl += "\n);"
    return ddl


def get_view_ddl(view_name):
    sql = """
        SELECT RDB$VIEW_SOURCE
        FROM RDB$RELATIONS
        WHERE TRIM(RDB$RELATION_NAME) = ?
    """
    result = db.execute_query(sql, (view_name,))
    if result and result[1]:
        source = result[1][0][0]
        return f"CREATE VIEW {view_name} AS\n{source}"
    return ""


def get_procedure_ddl(proc_name):
    sql = """
        SELECT RDB$PROCEDURE_SOURCE
        FROM RDB$PROCEDURES
        WHERE TRIM(RDB$PROCEDURE_NAME) = ?
    """
    result = db.execute_query(sql, (proc_name,))
    if result and result[1]:
        source = result[1][0][0]
        return f"CREATE PROCEDURE {proc_name}\nAS\n{source}"
    return ""


def get_function_ddl(func_name):
    sql = """
        SELECT RDB$FUNCTION_SOURCE
        FROM RDB$FUNCTIONS
        WHERE TRIM(RDB$FUNCTION_NAME) = ?
    """
    result = db.execute_query(sql, (func_name,))
    if result and result[1]:
        source = result[1][0][0]
        return f"CREATE FUNCTION {func_name}\n{source}"
    return ""


def get_trigger_ddl(trigger_name):
    sql = """
        SELECT RDB$TRIGGER_SOURCE, TRIM(RDB$RELATION_NAME), RDB$TRIGGER_TYPE
        FROM RDB$TRIGGERS
        WHERE TRIM(RDB$TRIGGER_NAME) = ?
    """
    result = db.execute_query(sql, (trigger_name,))
    if result and result[1]:
        source = result[1][0][0]
        table = result[1][0][1]
        return f"CREATE TRIGGER {trigger_name} FOR {table}\nAS\n{source}"
    return ""
