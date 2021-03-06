import queue
import threading
import time
from datetime import datetime
import pyshark
import math
import geoip2.database
from model.Feature import FeatureVector
from model.packet import Packet
from model.stream import StreamPacket
from service.OnlineService import load_training_and_model_by_device
from service.rest_service import post_request
from train_model import load_and_prepare_test_data
from utils.utils import get_current_time_millis, get_hour_minute, get_date

reader = geoip2.database.Reader('GeoLite2-Country.mmdb')

server_ip = "192.168.0.100"
server_port = "9999"

offline_processing = True
# cap = pyshark.FileCapture('C:\\Users\\dprefac\\PycharmProjects\\KMeans\\wiresharkScans\\tryaspcap.cap')


# capture = pyshark.LiveCapture()
# capture.sniff(timeout=50)
#
# for packet in capture.sniff_continuously(packet_count=5):
#     print(packet)
#

device_id = 1  # todo extract to property file
active_training = None
model = None
active_training, model = load_training_and_model_by_device(device_id)

packet_queue = queue.Queue()
stream_queue = queue.Queue()
stream_dic = {}
feature_vectors = []

high_danger_country_list = ["RU", "CN", "IL"]
ip_whitelist = ["127.0.0.1"]


def extract_ip_trust_feature(source_ip):
    try:
        split_ip = source_ip.split(".")
        if split_ip[0] == "10":
            ip_trust_feature = 0
            country_code = "lc"
        elif split_ip[0] == "172" and 15 <= int(split_ip[1]) <= 31:
            ip_trust_feature = 0
            country_code = "lc"
        elif split_ip[0] == "192" and split_ip[1] == "168":
            ip_trust_feature = 0
            country_code = "lc"
        else:
            country_code = reader.country(
                source_ip).country.iso_code  # todo exception handling (this shit may throw exceptions)
            if country_code in high_danger_country_list:
                ip_trust_feature = 1
            elif country_code == "RO":
                ip_trust_feature = 0.3
            else:
                ip_trust_feature = 0.6

        if source_ip in ip_whitelist:
            ip_trust_feature = 0

        return ip_trust_feature, country_code
    except:
        print("Exception - sniffer - extract_ip_trust_feature")


def extract_time_feature(packet):
    try:
        date_string = packet.capture_time.split(".")[0]
        date_time = datetime.utcfromtimestamp(int(date_string))
        hour = date_time.hour
        minute = date_time.minute
        total_minute_in_a_day = 1440
        radians = ((hour * 60 + minute) / total_minute_in_a_day) * (2 * math.pi)
        time_value_sin = math.sin(radians)
        time_value_cos = math.cos(radians)
        return time_value_sin, time_value_cos
    except:
        print("Exception - sniffer - extract_time_feature")


def calculate_size(packet_list):
    try:
        data_len = 0
        for packet in packet_list:
            if packet.destination_ip == server_ip:
                data_len = data_len + int(packet.tcp_payload_size)
        return data_len
    except:
        print("Exception - sniffer - calculate_size")


def extract_feature(stream):
    try:
        if len(stream.packet_list) > 2:
            if stream.packet_list[2].source_ip == stream.packet_list[
                0].source_ip:  # todo extract irtt also when second packet came later
                irtt = stream.packet_list[2].time_relative
                total_time = stream.packet_list[len(stream.packet_list) - 1].time_relative
                time_value_sin, time_value_cos = extract_time_feature(stream.packet_list[0])
                data_len = calculate_size(
                    stream.packet_list)  # todo send also serve ip from packet in order not to use global variable anymore
                ip_trust_level, country = extract_ip_trust_feature(stream.packet_list[0].source_ip)

                feature_vector = FeatureVector(
                    id=None,
                    irtt=irtt,
                    total_time=total_time,
                    time_value_sin=time_value_sin,
                    time_value_cos=time_value_cos,
                    data_len=data_len,
                    ip_trust_level=ip_trust_level,
                    client_ip=stream.packet_list[0].source_ip,
                    packet_number=len(stream.packet_list),
                    source="",  # todo make this dinamic
                    server_ip=stream.packet_list[0].destination_ip,
                    server_port=stream.server_port,
                    server_id=device_id,
                    date=get_date(),
                    time=get_hour_minute(),
                    country=country.lower(),
                    status="INCERT"
                )
                if active_training is not None:
                    test_data = load_and_prepare_test_data(feature_vectors=
                                                           [[feature_vector.__dict__[o] for o in feature_vector.__dict__]],
                                                           modified_columns=active_training.modified_columns)
                    y_pred_test = model.predict(test_data)
                    if y_pred_test[0].astype(int) == 1:
                        feature_vector.status = "NORMAL"
                        print("normal")
                    elif y_pred_test[0].astype(int) == -1:
                        feature_vector.status = "ATTACK"
                        print("attack")

                feature_vectors.append(feature_vector)
                print(feature_vector.irtt,
                      feature_vector.total_time,
                      feature_vector.time_value_sin,
                      feature_vector.time_value_cos,
                      feature_vector.data_len,
                      feature_vector.ip_trust_level,
                      feature_vector.packet_number,
                      feature_vector.client_ip,
                      feature_vector.server_ip,
                      feature_vector.server_port)
                post_request("/addfeature", feature_vector)
            else:
                print("IP-urile nu sunt egale !!")
                for packet in stream.packet_list:
                    print(packet.source_ip, "->", packet.destination_ip, " ", packet.tcp_syn, " ", packet.tcp_ack)
    except:
        print("Exception - sniffer - extract_feature")


def extract_stream_live():
    while True:
        try:
            if stream_queue.empty():
                stream = None
            else:
                stream = stream_queue.get()

            if stream is not None:
                if offline_processing or get_current_time_millis() - stream.added_time_milliseconds > 10000:
                    # print(stream.stream_index, ": ", stream.packet_list[0].source_ip, " -> ",
                    #       stream.packet_list[0].destination_ip)
                    del stream_dic[stream.stream_index]
                    extract_feature(stream)
                else:
                    stream_queue.put(stream)
                    print("stream queue size: ", stream_queue.qsize())
                    time.sleep(3)
                    print('Processing thread is sleeping....')
                # stream_queue.task_done()
            else:
                time.sleep(3)
        except:
            print("Exception - sniffer - extract_stream_live")


stream_exaction_thread = threading.Thread(target=extract_stream_live)
stream_exaction_thread.setDaemon(True)


def sort_and_filter_by_stream_index(packet):
    try:
        stream_index = packet.stream_index
        if stream_index in stream_dic:
            stream = stream_dic[stream_index]
            if offline_processing or get_current_time_millis() - stream.added_time_milliseconds < 10000:
                if float(packet.time_relative) > 1:
                    print(packet.time_relative, " ", stream_index, " ", packet.source_ip)
                stream.packet_list.append(packet)
            else:
                print("more than 10 seconds has passed ", stream_index)
        else:
            if packet.tcp_syn == "1" and packet.tcp_ack == "0":
                initial_connection_time = round(float(packet.capture_time)) * 1000
                stream = StreamPacket(stream_index, [packet], initial_connection_time, server_port=packet.destination_port)
                stream_dic[stream_index] = stream
                stream_queue.put(stream)
    except:
        print("Exception - sniffer - sort_and_filter_by_stream_index")


def get_packet_live():
    while True:
        try:
            packet = packet_queue.get()
            if packet is not None:
                sort_and_filter_by_stream_index(packet)
                # print("size: ", packet_queue.qsize())
                # packet_queue.task_done()
            else:
                print("no packet")
        except:
            print("Exception - sniffer - get_packet_live")


def get_packet_offline():
    packet = packet_queue.get()
    while packet is not None:
        try:
            sort_and_filter_by_stream_index(packet)
            print("Extracted")
            if packet_queue.empty():
                packet = None
            else:
                packet = packet_queue.get()
        except:
            print("Exception - sniffer - get_packet_offline")
    print("Done getting packets offline")


packet_exaction_thread = threading.Thread(target=get_packet_live)
packet_exaction_thread.setDaemon(True)


def filter_and_save_packets(raw_packet):
    try:
        # if raw_packet["eth"].type == "0x00000800":
        if raw_packet["ip"].proto == "6":
            if raw_packet["ip"].dst == server_ip and raw_packet["tcp"].dstport == server_port \
                    or \
                    raw_packet["ip"].src == server_ip and raw_packet["tcp"].srcport == server_port:
                packet_queue.put(Packet(raw_packet))
                print("put")
        else:
            print("not TCP")
    except:
        print("Exception - sniffer - filter_and_save_packets")


# else:
#     print("not IPV4")


def extract_stream_offline():
    stream = stream_queue.get()
    while stream is not None:
        try:
            if offline_processing or get_current_time_millis() - stream.added_time_milliseconds > 10000:
                # print(stream.stream_index, ": ", stream.packet_list[0].source_ip, " -> ",
                #       stream.packet_list[0].destination_ip)
                del stream_dic[stream.stream_index]
                extract_feature(stream)
            else:
                stream_queue.put(stream)
                print("stream queue size: ", stream_queue.qsize())
                time.sleep(3)
                print('Processing thread is sleeping....')
            if stream_queue.empty():
                stream = None
            else:
                stream = stream_queue.get()
            stream_queue.task_done()
        except:
            print("Exception - sniffer - extract_stream_offline")


def save_packet(raw_packet):
    try:
        packet_queue.put(Packet(raw_packet))
    except:
        print("Exception - sniffer - save_packet")


def capture_traffic_live(packet):
    try:
        t = threading.Thread(target=filter_and_save_packets(packet))
        t.setDaemon(True)
        t.start()
    except:
        print("Exception - sniffer - capture_traffic_live")


def capture_traffic_offline(packet):
    try:
        t = threading.Thread(target=filter_and_save_packets(packet))
        t.setDaemon(True)
        t.start()
    except:
        print("Exception - sniffer - capture_traffic_offline")


def capture_live_traffic(bpf_filter="ip.dst == 192.168.43.28 and tcp.dstport == 5000"):
    try:
        packet_exaction_thread.start()
        stream_exaction_thread.start()
        capture = pyshark.LiveCapture(bpf_filter=bpf_filter)
        capture.set_debug()
        # capture.sniff_continuously()
        capture.apply_on_packets(capture_traffic_live)
    except:
        print("Exception - sniffer - capture_live_traffic")


def capture_traffic_from_file(file_path):
    try:
        capture = pyshark.FileCapture(input_file=file_path, display_filter="tcp")
        start_time = get_current_time_millis()
        print(0, "Start extracting data from file...")
        for packet in capture:
            capture_traffic_offline(packet)
        # capture.apply_on_packets(capture_traffic_offline)
        print((get_current_time_millis() - start_time) / 60000, "Start extracting packets from queue...")
        get_packet_offline()
        print(get_current_time_millis() - start_time, "Start extracting stream from dic...")
        extract_stream_offline()
        return feature_vectors
    except:
        print("Exception - sniffer - capture_traffic_from_file")


capture_live_traffic(bpf_filter="dst host 192.168.0.100 and dst port 9999")
# capture_traffic_from_file(
#     file_path="C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\wiresharkScans\\home_test\\hydra_1000_vpn_rusia1.pcapng")
