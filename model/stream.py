class StreamPacket:
    def __init__(self, stream_index, packet_list, added_time_milliseconds, server_port):
        self.stream_index = stream_index
        self.packet_list = packet_list
        self.added_time_milliseconds = added_time_milliseconds
        self.server_port = server_port