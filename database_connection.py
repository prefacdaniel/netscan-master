import sqlite3

from Feature import FeatureVector

conn = sqlite3.connect('C:\\Users\\dprefac\\Documents\\disertatie\\sqlite\\databases\\feature_vectors.db')

feature = FeatureVector(0.1, 0.1, 0.2, 0.43, 233, 3, "127.4.0.1", "176.123.54.23", 5000)

conn.executemany('INSERT INTO feature VALUES (NULL,?,?,?,?,?,?,?,?,?)',
                 [(feature.iRTT, feature.total_time, feature.time_value_sin, feature.time_value_cos, feature.data_len, feature.ip_trust_level, feature.client_ip, feature.server_ip, feature.server_port)])

conn.commit()
conn.close()
