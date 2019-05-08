class FeatureVector:
    def __init__(self, irtt, total_time, time_value_sin, time_value_cos, data_len, ip_trust_level, client_ip,
                 server_ip, server_port):
        self.iRTT = irtt
        self.total_time = total_time
        self.time_value_sin = time_value_sin
        self.time_value_cos = time_value_cos
        self.data_len = data_len
        self.ip_trust_level = ip_trust_level
        self.client_ip = client_ip
        self.server_ip = server_ip
        self.server_port = server_port
