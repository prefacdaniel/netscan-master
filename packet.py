class Packet:
    def __init__(self, tpc_packet):
        self.stream_index = tpc_packet.tcp.stream  # a sintetic unique identifier (autoincremntal integer) gave by tshark to each TCP stream
        self.capture_time = tpc_packet.frame_info.time_epoch  # epoch time when this frame (packet) was captured
        self.source_ip = tpc_packet.ip.src  # the source IP of this packet
        self.time_delta = tpc_packet.tcp.time_delta  # Time since previous frame in this TCP stream
        self.time_relative = tpc_packet.tcp.time_relative  # Time since first frame in this TCP stream
        self.tcp_payload_size = tpc_packet.tcp.len  # tpc payload size in bytes
        self.tcp_syn = tpc_packet.tcp.flags_syn
