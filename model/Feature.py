class FeatureVector:
    def __init__(self,
                 id,
                 irtt,
                 total_time,
                 time_value_sin,
                 time_value_cos,
                 data_len,
                 ip_trust_level,
                 client_ip,
                 packet_number,
                 source,
                 server_ip,
                 server_port,
                 server_id,
                 date,
                 time,
                 country,
                 status):
        self.id =id
        self.irtt = float(irtt)
        self.total_time = float(total_time)
        self.time_value_sin = float(time_value_sin)
        self.time_value_cos = float(time_value_cos)
        self.data_len = int(data_len)
        self.ip_trust_level = float(ip_trust_level)
        self.client_ip = client_ip
        self.packet_number = packet_number
        self.source = source
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.server_id = int(server_id)
        self.date = date
        self.time = time
        self.country = country
        self.status = status

    def default(self, o):
        return o.__dict__
