import queue
import threading

import pyshark

# cap = pyshark.FileCapture('C:\\Users\\dprefac\\PycharmProjects\\KMeans\\wiresharkScans\\tryaspcap.cap')


# capture = pyshark.LiveCapture()
# capture.sniff(timeout=50)
#
# for packet in capture.sniff_continuously(packet_count=5):
#     print(packet)
#


packet_queue = queue.Queue()


def extract_data(stream):
    pass #todo
    # capture_time = packet.frame_info.time_epoch  # epoch time when this frame (packet) was captured
    # source_ip = packet.ip.src  # the source IP of this packet
    # stream_index = packet.tcp.stream  # a sintetic unique identifier (autoincremntal integer) gave by tshark to each TCP stream
    # time_delta = packet.tcp.time_delta  # Time since previous frame in this TCP stream
    # time_relative = packet.tcp.time_relative  # Time since first frame in this TCP stream
    # tcp_payload_size = packet.tcp.len  # tpc payload size in bytes
    # print(capture_time)


def extract_stream():
    pass  # todo extract a stream by some rules (timeout or socket close) and after that, call extract_data method


stream_exaction_thread = threading.Thread(target=extract_stream)
stream_exaction_thread.setDaemon(True)
stream_exaction_thread.start()


def sort_and_filter_by_stream_index(packet):
    pass  # todo skip already existent connexion packets


def filter_packets(packet):
    if packet["ip"].proto == "6":
        sort_and_filter_by_stream_index(packet)


def capture_traffic(packet):
    t = threading.Thread(target=filter_packets(packet))
    t.setDaemon(True)
    t.start()


capture = pyshark.LiveCapture()
# capture.sniff_continuously()
capture.apply_on_packets(capture_traffic)

# print(cap[1])
# print(cap)
# cap.close()
