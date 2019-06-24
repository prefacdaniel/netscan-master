import sqlite3
import json
from model.ActiveTraining import ActiveTraining
from model.Model import Model
from model.Server import Server
from model.Training import Training

database_path = 'C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\database\\feature_vectors.db'


def insert_feature_vectors(feature_vectors, instance_name):
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
                           )])  # //todo probably this muse be modified
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


def get_model_by_id(model_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM model WHERE id = " + model_id)
    rows = cursor.fetchall()
    model = Model(id=rows[0][0], server_id=rows[0][1], algorithm_id=rows[0][2])
    return model


def get_algorithm_name_by_id(algorithm_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM algorithms WHERE id = " + algorithm_id)
    rows = cursor.fetchall()
    return rows[0][1]


def save_training(training):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO training VALUES (NULL,?,?,?,?,?,?,?)',
                   (
                       training.model_id,
                       training.date,
                       training.utilised_columns,
                       training.modified_columns,
                       training.parameters_vector,
                       training.model_body,
                       training.weights
                   ))
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def get_training_by_id(training_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM training WHERE id = " + training_id)
    rows = cursor.fetchall()
    return Training(
        id=rows[0][0],
        model_id=rows[0][1],
        date=rows[0][2],
        utilised_columns=rows[0][3],
        modified_columns=rows[0][4],
        parameters_vector=rows[0][5],
        model_body=rows[0][6],
        weights=rows[0][7])


def get_all_active_training():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM active_training")
    rows = cursor.fetchall()
    active_trainings = []
    for training in rows:
        active_training = ActiveTraining(id=training[0], algorithm_id=training[1], training_id=training[2])
        active_trainings.append(active_training)
    return active_trainings


def save_training_element(training_element):
    conn = sqlite3.connect(database_path)
    for feature in training_element.training_feature_vectors:
        conn.executemany('INSERT INTO training_element VALUES (NULL,?,?)',
                         [(feature[0],
                           training_element.training_id,
                           )])
    conn.commit()
    conn.close()


def get_server_by_id(server_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server WHERE id = " + server_id)
    rows = cursor.fetchall()
    server = Server(id=rows[0][0], ip=rows[0][1], port=rows[0][2], name=rows[0][3], status=rows[0][4], image=rows[0][5])
    return server


def get_all_servers():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server")
    rows = cursor.fetchall()
    servers = []
    for row in rows:
        server = Server(id=row[0], ip=row[1], port=row[2], name=row[3], status=row[4], image=row[5])
        servers.append(server)
    return servers


def save_server(server):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO server VALUES (NULL,?,?,?,?,?)',
                   (
                       server.ip,
                       server.port,
                       server.name,
                       server.status,
                       server.image
                   ))
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id


def query_db(query, args=(), one=False):
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


def query_db_get_json(query, args=()):
    my_query = query_db(query, args)
    return json.dumps(my_query)


def get_device_data_by_id(device_id):
    query = "select date dateString, count(b.evaluation) attacksNumber " \
            "from server, feature " \
            "left join (Select st.evaluation, st.feature_id " \
            "from training t, active_training at,  status st " \
            "where t.id = at.training_id " \
            "and t.id = st.training_id " \
            "and st.evaluation = \"attack\") b " \
            "on feature_id = b.feature_id " \
            "where server.id = feature.server_id " \
            "and server.id = ? " \
            "group by feature.date, b.evaluation "
    return query_db_get_json(query, device_id)


def get_connection_for_device_from_date_from_db(device_id, date):
    query = "select feature.id, time, country, feature.status connectionStatusFromUser, b.evaluation " \
            "connectionStatusFromAlgorithm " \
            "from server, feature " \
            "left join (Select st.evaluation, st.feature_id " \
            "            from training t, active_training at,  status st " \
            "            where t.id = at.training_id " \
            "            and t.id = st.training_id) b " \
            "    on feature_id = b.feature_id " \
            "where server.id = feature.server_id " \
            "and server.id = ?" \
            "and date = ?"
    return query_db_get_json(query, (device_id, date))


print(query_db_get_json("SELECT * FROM feature"))
