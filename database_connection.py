import sqlite3

database_path = 'C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\database\\feature_vectors.db'

def insert_data(feature_vectors, instance_name):
    conn = sqlite3.connect(database_path)
    for feature in feature_vectors:
        conn.executemany('INSERT INTO feature VALUES (NULL,?,?,?,?,?,?,?,?,?)',
                         [(feature.irtt,
                           feature.total_time,
                           feature.time_value_sin,
                           feature.time_value_cos,
                           feature.data_len,
                           feature.ip_trust_level,
                           feature.client_ip,
                           feature.packet_number,
                           instance_name
                           )])
    conn.commit()
    conn.close()


def select_columns_data_from_feature(source_name, column_list):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    sql = 'SELECT '
    for column in column_list:
        sql = sql + column + " ,"
    sql = sql[:-1]
    sql = sql + 'FROM feature where source LIKE \"' + source_name + '\";'
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def select_all_data_from_feature(source_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feature where source LIKE \"" + source_name + "\"")
    rows = cursor.fetchall()
    return rows
