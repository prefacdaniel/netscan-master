import time
from enum import Enum

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP


class PktDirection(Enum):
    not_defined = 0
    client_to_server = 1
    server_to_client = 2


# , pkt_metadata, pkt_data, data_link_filters, network_filters, transport_filters, application_filters):

def apply_link_filters(ether_pkt):
    if 'type' not in ether_pkt.fields:
        # LLC frames will have 'len' instead of 'type'.
        # We disregard those
        return False
    if ether_pkt.type != 0x0800:
        # disregard non-IPv4 packets
        return False
    return True


def apply_network_filters(ip_pkt):
    if ip_pkt.proto != 6:
        # Ignore non-TCP packet
        return False
    client_ip = '37.120.249.45'
    if ip_pkt.src != client_ip:
        return False
    # Determine the TCP payload length. IP fragmentation will mess up this
    # logic, so first check that this is an unfragmented packet
    if (ip_pkt.flags == 'MF') or (ip_pkt.frag != 0):
            print('No support for fragmented IP packets')
            return False
    return True


def apply_transport_filters(tcp_pkt):
    return True


def process_packet(pkt_metadata, ether_pkt, ip_pkt, tcp_pkt):
    tcp_payload_len = ip_pkt.len - (ip_pkt.ihl * 4) - (tcp_pkt.dataofs * 4)
    if tcp_payload_len > 0:
        ip_source = ip_pkt.src
        ip_destination = ip_pkt.dst
        str = '{}  {} {} irt'


def process_file(file_name):
    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        ether_pkt = Ether(pkt_data)
        if apply_link_filters(ether_pkt):
            ip_pkt = ether_pkt[IP]
            if apply_network_filters(ip_pkt):
                tcp_pkt = ip_pkt[TCP]
                if apply_transport_filters(tcp_pkt):
                    process_packet(pkt_metadata, ether_pkt, ip_pkt,tcp_pkt)


def process_pcap(file_name):
    print('Opening {}...'.format(file_name))

    client_ip = '37.120.249.45'
    server_ip = '192.168.0.100'

    count = 0
    interesting_packet_count = 0

    server_sequence_offset = None
    client_sequence_offset = None

    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        count += 1

        ether_pkt = Ether(pkt_data)
        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'.
            # We disregard those
            continue

        if ether_pkt.type != 0x0800:
            # disregard non-IPv4 packets
            continue

        ip_pkt = ether_pkt[IP]

        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue

        tcp_pkt = ip_pkt[TCP]

        direction = PktDirection.not_defined

        if ip_pkt.src == client_ip:
            if ip_pkt.dst != server_ip:
                continue
            direction = PktDirection.client_to_server
        elif ip_pkt.src == server_ip:
            if ip_pkt.dst != client_ip:
                continue
            direction = PktDirection.server_to_client
        else:
            continue

        interesting_packet_count += 1
        if interesting_packet_count == 1:
            first_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
            first_pkt_timestamp_resolution = pkt_metadata.tsresol
            first_pkt_ordinal = count

        last_pkt_timestamp = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
        last_pkt_timestamp_resolution = pkt_metadata.tsresol
        last_pkt_ordinal = count

        this_pkt_relative_timestamp = last_pkt_timestamp - first_pkt_timestamp

        if direction == PktDirection.client_to_server:
            if client_sequence_offset is None:
                client_sequence_offset = tcp_pkt.seq
            relative_offset_seq = tcp_pkt.seq - client_sequence_offset
        else:
            assert direction == PktDirection.server_to_client
            if server_sequence_offset is None:
                server_sequence_offset = tcp_pkt.seq
            relative_offset_seq = tcp_pkt.seq - server_sequence_offset

        # If this TCP packet has the Ack bit set, then it must carry an ack
        # number.
        if 'A' not in str(tcp_pkt.flags):
            relative_offset_ack = 0
        else:
            if direction == PktDirection.client_to_server:
                relative_offset_ack = tcp_pkt.ack - server_sequence_offset
            else:
                relative_offset_ack = tcp_pkt.ack - client_sequence_offset

        # Determine the TCP payload length. IP fragmentation will mess up this
        # logic, so first check that this is an unfragmented packet
        if (ip_pkt.flags == 'MF') or (ip_pkt.frag != 0):
            print('No support for fragmented IP packets')
            break

        tcp_payload_len = ip_pkt.len - (ip_pkt.ihl * 4) - (tcp_pkt.dataofs * 4)
        # payload = bytes(tcp_pkt.payload)

        # Print
        fmt = '[{ordnl:>5}]{ts:>10.6f}s flag={flag:<3s} seq={seq:<9d} ack={ack:<9d} len={len:<6d} TCP_payload={' \
              'tcp_payload} '
        if direction == PktDirection.client_to_server:
            fmt = '{arrow}' + fmt
            arr = '-->'
        else:
            fmt = '{arrow:>69}' + fmt
            arr = '<--'

        print(fmt.format(arrow=arr,
                         ordnl=last_pkt_ordinal,
                         ts=this_pkt_relative_timestamp / pkt_metadata.tsresol,
                         flag=str(tcp_pkt.flags),
                         seq=relative_offset_seq,
                         ack=relative_offset_ack,
                         len=tcp_payload_len,
                         tcp_payload=tcp_pkt.payload))
    # ---

    print('{} contains {} packets ({} interesting)'.
          format(file_name, count, interesting_packet_count))


star_time = time.time()
print("start time: ", star_time)

process_file(
    "C:\\Users\\dprefac\\PycharmProjects\\KMeans\\wiresharkScans\\invalid_pythonScript_1000_telekom_VPNRusia.pcapng")
print("loading time: ", time.time() - star_time)
