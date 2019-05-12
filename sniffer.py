import queue
import threading
import time
from datetime import datetime
import pyshark
import math
import geoip2.database
from Feature import FeatureVector
from packet import Packet
from stream import StreamPacket

reader = geoip2.database.Reader('C:\\Users\\dprefac\\Downloads\\GeoLite2-Country.mmdb')

server_ip = "192.168.0.100"
server_port = "9999"

current_milli_time = lambda: int(round(time.time() * 1000))
# cap = pyshark.FileCapture('C:\\Users\\dprefac\\PycharmProjects\\KMeans\\wiresharkScans\\tryaspcap.cap')


# capture = pyshark.LiveCapture()
# capture.sniff(timeout=50)
#
# for packet in capture.sniff_continuously(packet_count=5):
#     print(packet)
#

packet_queue = queue.Queue()
stream_queue = queue.Queue()
stream_dic = {}

high_danger_country_list = ["RU", "CN", "IL"]
ip_whitelist = ["127.0.0.1"]


def extract_ip_trust_feature(source_ip):
    if source_ip in ip_whitelist:
        ip_trust_feature = 0
    else:
        split_ip = source_ip.split(".")
        if split_ip[0] == "10":
            ip_trust_feature = 0
        elif split_ip[0] == "172" and 15 <= int(split_ip[1]) <= 31:
            ip_trust_feature = 0
        elif split_ip[0] == "192" and split_ip[1] == "168":
            ip_trust_feature = 0
        else:
            country_code = reader.country(
                source_ip).country.iso_code  # todo exception handling (this shit may throw exceptions)
            if country_code in high_danger_country_list:
                ip_trust_feature = 1
            elif country_code == "RO":
                ip_trust_feature = 0.3
            else:
                ip_trust_feature = 0.6
    return ip_trust_feature


def extract_time_feature(packet):
    date_string = packet.capture_time.split(".")[0]
    date_time = datetime.utcfromtimestamp(int(date_string))
    hour = date_time.hour
    minute = date_time.minute
    total_minute_in_a_day = 1440
    radians = ((hour * 60 + minute) / total_minute_in_a_day) * (2 * math.pi)
    time_value_sin = math.sin(radians)
    time_value_cos = math.cos(radians)
    return time_value_sin, time_value_cos


def calculate_size(packet_list):
    data_len = 0
    for packet in packet_list:
        if packet.destination_ip == server_ip:
            data_len = data_len + int(packet.tcp_payload_size)
    return data_len


def extract_feature(stream):
    if len(stream.packet_list) > 2:
        if stream.packet_list[2].source_ip == stream.packet_list[0].source_ip:
            iRTT = stream.packet_list[2].time_relative
            total_time = stream.packet_list[len(stream.packet_list) - 1].time_relative
            time_value_sin, time_value_cos = extract_time_feature(stream.packet_list[0])
            data_len = calculate_size(stream.packet_list)
            ip_trust_level = extract_ip_trust_feature(stream.packet_list[0].source_ip)
            feature_vector = FeatureVector(irtt=iRTT,
                                           total_time=total_time,
                                           time_value_sin=time_value_sin,
                                           time_value_cos=time_value_cos,
                                           data_len=data_len,
                                           ip_trust_level=ip_trust_level,
                                           client_ip=stream.packet_list[0].source_ip,
                                           server_ip=stream.packet_list[0].destination_ip,
                                           server_port=stream.server_port
                                           )
        else:
            print("IP-urile nu sunt egale !!")
            for packet in stream.packet_list:
                print(packet.source_ip, "->", packet.destination_ip, " ", packet.tcp_syn, " ", packet.tcp_ack)


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
            initial_connection_time = round(float(packet.capture_time)) * 1000
            stream = StreamPacket(stream_index, [packet], initial_connection_time, server_port=packet.destination_port)
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


def filter_and_save_packets(raw_packet):
    if raw_packet["eth"].type == "0x00000800":
        if raw_packet["ip"].proto == "6":
            if raw_packet["ip"].dst == server_ip and raw_packet["tcp"].dstport == server_port \
                    or \
                    raw_packet["ip"].src == server_ip and raw_packet["tcp"].srcport == server_port:
                packet_queue.put(Packet(raw_packet))
        else:
            print("not TCP")
    else:
        print("not IPV4")


def save_packet(raw_packet):
    packet_queue.put(Packet(raw_packet))


def capture_traffic(packet):
    t = threading.Thread(target=save_packet(packet))
    t.setDaemon(True)
    t.start()


def capture_live_traffic(bpf_filter="tcp"):
    capture = pyshark.LiveCapture(bpf_filter=bpf_filter)
    # capture.sniff_continuously()
    capture.apply_on_packets(capture_traffic)


def capture_traffic_from_file(file_path):
    capture = pyshark.FileCapture(input_file=file_path)
    capture.apply_on_packets(filter_and_save_packets)


# capture_live_traffic(bpf_filter="tcp")
capture_traffic_from_file(
    file_path="C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\wiresharkScans\\home_test\\hydra_1000_vpn_rusia1.pcapng")
