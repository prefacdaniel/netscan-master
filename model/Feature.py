class FeatureVector:
    def __init__(self,
                 irtt,
                 total_time,
                 time_value_sin,
                 time_value_cos,
                 data_len,
                 packet_number,
                 source,
                 ip_trust_level,
                 client_ip,
                 server_ip,
                 server_port,
                 server_id,
                 date,
                 time,
                 country,
                 status):
        self.irtt = float(irtt)
        self.total_time = float(total_time)
        self.time_value_sin = float(time_value_sin)
        self.time_value_cos = float(time_value_cos)
        self.data_len = int(data_len)
        self.ip_trust_level = float(ip_trust_level)
        self.packet_number = packet_number
        self.source = source
        self.client_ip = client_ip
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.server_id = int(server_id)
        self.date = date
        self.time = time
        self.country = country
        self.status = status

    def default(self, o):
        return o.__dict__
