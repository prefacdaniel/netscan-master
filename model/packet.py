class Packet:
    def __init__(self, raw_packet):
        self.stream_index = raw_packet.tcp.stream  # a sintetic unique identifier (autoincremntal integer) gave by tshark to each TCP stream
        self.capture_time = raw_packet.frame_info.time_epoch  # epoch time when this frame (packet) was captured
        self.source_ip = raw_packet.ip.src  # the source IP of this packet
        self.destination_ip = raw_packet.ip.dst  # the destination IP of this packet
        self.time_delta = raw_packet.tcp.time_delta  # Time since previous frame in this TCP stream
        self.time_relative = raw_packet.tcp.time_relative  # Time since first frame in this TCP stream
        self.tcp_payload_size = raw_packet.tcp.len  # tpc payload size in bytes
        self.tcp_syn = raw_packet.tcp.flags_syn
        self.tcp_ack = raw_packet.tcp.flags_ack
        self.destination_port = raw_packet.tcp.dstport