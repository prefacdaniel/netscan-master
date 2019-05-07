import queue
import threading
import time

import pyshark

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


def extract_data(stream):
    pass  # todo


def extract_stream():
    while True:
        stream = stream_queue.get()
        if stream is None:
            print("nothing in stream up: ", stream_queue.empty())
            break
        if current_milli_time() - stream.added_time_milliseconds > 10000:
            stream_size = len(stream.packet_list);
            if stream_size > 100:
                print("nigga, this is big")
            print(stream.stream_index, ": ", stream.packet_list[0].source_ip, " -> ",
                  stream.packet_list[0].destination_ip)
            if all(
                    int(stream.packet_list[i].capture_time.split('.')[1]) <= int(stream.packet_list[i + 1].capture_time.split('.')[1]) for i in
                    range(len(
                            stream.packet_list) - 1)):  # todo: remove daca s a stabilit ca listele sunt mereu ordonate
                print()
            else:
                print("List: ")
                for i in range(len(stream.packet_list) - 1):
                    print(int(stream.packet_list[i].capture_time.split('.')[1]))
                print("LISTA NU ESTE ORDONATA !! ^")
            if all(
                    float(stream.packet_list[i].time_relative) <= float(stream.packet_list[i + 1].time_relative) for i in
                    range(len(
                            stream.packet_list) - 1)):  # todo: remove daca s a stabilit ca listele sunt mereu ordonate
                print()
            else:
                print("List: ")
                for i in range(len(stream.packet_list) - 1):
                    print(float(stream.packet_list[i].time_relative))
                print("LISTA NU ESTE ORDONATA !! ^")
            del stream_dic[stream.stream_index]
        else:
            stream_queue.put(stream)
            time.sleep(3)
            print('readded')
        stream_queue.task_done()
        # todo extract a stream by some rules (timeout or socket close) and after that, call extract_feature method


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
    else:
        print("not TCP")


def capture_traffic(packet):
    t = threading.Thread(target=filter_packets(packet))
    t.setDaemon(True)
    t.start()


capture = pyshark.LiveCapture(bpf_filter="tcp")
# capture.sniff_continuously()
capture.apply_on_packets(capture_traffic)
