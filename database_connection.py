import sqlite3

from Feature import FeatureVector


#
# conn = sqlite3.connect('C:\\Users\\dprefac\\Documents\\disertatie\\sqlite\\databases\\feature_vectors.db')
#
# feature = FeatureVector(0.1, 0.1, 0.2, 0.43, 233, 3, "127.4.0.1", "176.123.54.23", 5000)
#
# conn.executemany('INSERT INTO feature VALUES (NULL,?,?,?,?,?,?,?,?,?)',
#                  [(feature.iRTT, feature.total_time, feature.time_value_sin, feature.time_value_cos, feature.data_len, feature.ip_trust_level, feature.client_ip, feature.server_ip, feature.server_port)])
#
# conn.commit()
# conn.close()


def insert_data(feature_vectors, instance_name):
    conn = sqlite3.connect('C:\\Users\\dprefac\\Documents\\disertatie\\sqlite\\databases\\feature_vectors.db')
    for feature in feature_vectors:
        conn.executemany('INSERT INTO feature VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)',
                         [(feature.irtt,
                           feature.total_time,
                           feature.time_value_sin,
                           feature.time_value_cos,
                           feature.data_len,
                           feature.ip_trust_level,
                           feature.client_ip,
                           feature.server_ip,
                           feature.server_port,
                           feature.packet_number,
                           instance_name
                           )])
    conn.commit()
    conn.close()


def select_columns_data_from_feature(instance_name, column_list):
    conn = sqlite3.connect('C:\\Users\\dprefac\\Documents\\disertatie\\sqlite\\databases\\feature_vectors.db')
    cursor = conn.cursor()
    sql = 'SELECT '
    for column in column_list:
        sql = sql + column + " ,"
    sql = sql[:-1]
    sql = sql + 'FROM feature where instance_name LIKE \"' + instance_name + '\";'
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def select_all_data_from_feature(instance_name):
    conn = sqlite3.connect('C:\\Users\\dprefac\\Documents\\disertatie\\sqlite\\databases\\feature_vectors.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feature where instance_name LIKE \"" + instance_name + "\"")
    rows = cursor.fetchall()
    return rows


feature_vectors = select_columns_data_from_feature("hydra_1000_vpn_rusia1.pcapng", ['irtt', 'total_time', 'time_value_sin', 'time_value_cos', 'data_len'])

for feature in feature_vectors:
    print(feature)
