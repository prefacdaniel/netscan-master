import queue
import threading
import time
from datetime import datetime
import pyshark
import math

server_ip = "127.0.0.1"
server_port = "8080"

current_milli_time = lambda: int(round(time.time() * 1000))
# cap = pyshark.FileCapture('C:\\Users\\dprefac\\PycharmProjects\\KMeans\\wiresharkScans\\tryaspcap.cap')


# capture = pyshark.LiveCapture()
# capture.sniff(timeout=50)
#
# for packet in capture.sniff_continuously(packet_count=5):
#     print(packet)
#
from packet import Packet
from stream import StreamPacket

packet_queue = queue.Queue()
stream_queue = queue.Queue()
stream_dic = {}


def extract_time_feature(packet):
    date_string = packet.capture_time.split(".")[0]
    date_time = datetime.utcfromtimestamp(int(date_string))
    hour = date_time.hour
    minute = date_time.minute
    time_value = (hour * 60 + minute) / 8
    return math.sin(math.radians(time_value))


def extract_feature(stream):
    if len(stream.packet_list) > 2:
        if stream.packet_list[2].source_ip == stream.packet_list[0].source_ip:
            iRTT = stream.packet_list[2].time_relative
            total_time = stream.packet_list[len(stream.packet_list) - 1].time_relative
            time_feature = extract_time_feature(stream.packet_list[0])
            # minute = extract
        else:
            print("IP-urile nu sunt egale !!")


def extract_stream():
    while True:
        stream = stream_queue.get()
        if stream is None:
            print("nothing in stream up: ", stream_queue.empty())
            break
        if current_milli_time() - stream.added_time_milliseconds > 10000:
            print(stream.stream_index, ": ", stream.packet_list[0].source_ip, " -> ",
                  stream.packet_list[0].destination_ip)
            del stream_dic[stream.stream_index]
            extract_feature(stream)
        else:
            stream_queue.put(stream)
            print("stream queue size: ", stream_queue.qsize())
            time.sleep(3)
            print('Processing thread is sleeping....')
        stream_queue.task_done()


stream_exaction_thread = threading.Thread(target=extract_stream)
stream_exaction_thread.setDaemon(True)
stream_exaction_thread.start()


def sort_and_filter_by_stream_index(packet):
    stream_index = packet.stream_index
    if stream_index in stream_dic:
        stream = stream_dic[stream_index]
        if current_milli_time() - stream.added_time_milliseconds < 10000:
            if float(packet.time_relative) > 1:
                print(packet.time_relative, " ", stream_index, " ", packet.source_ip)
            stream_dic[stream_index].packet_list.append(packet)
        else:
            print("more than 10 seconds has passed ", stream_index)
    else:
        if packet.tcp_syn == "1" and packet.tcp_ack == "0":
            stream = StreamPacket(stream_index, [packet], current_milli_time())
            stream_dic[stream_index] = stream
            stream_queue.put(stream)


def get_packet():
    while True:
        packet = packet_queue.get()
        if packet is None:
            break
        sort_and_filter_by_stream_index(packet)
        packet_queue.task_done()


packet_exaction_thread = threading.Thread(target=get_packet)
packet_exaction_thread.setDaemon(True)
packet_exaction_thread.start()


def filter_packets(raw_packet):
    if raw_packet["ip"].proto == "6":
        packet_queue.put(Packet(raw_packet))
        # print("packet queue size: ", packet_queue.qsize())
    else:
        print("not TCP")


def capture_traffic(packet):
    t = threading.Thread(target=filter_packets(packet))
    t.setDaemon(True)
    t.start()


capture = pyshark.LiveCapture(bpf_filter="tcp")
# capture.sniff_continuously()
capture.apply_on_packets(capture_traffic)
