import pyshark


# cap = pyshark.FileCapture('C:\\Users\\dprefac\\PycharmProjects\\KMeans\\wiresharkScans\\tryaspcap.cap')


# capture = pyshark.LiveCapture()
# capture.sniff(timeout=50)
#
# for packet in capture.sniff_continuously(packet_count=5):
#     print(packet)
#
def packet_captured(packet):
    if packet["ip"].proto == "6":
        print("\n\n####################")
        print('Just arrived:', packet)
        print("\n\n####################")
    else:
        print("no")


capture = pyshark.LiveCapture(bpf_filter="tcp")
# capture.sniff_continuously()
capture.apply_on_packets(packet_captured)

# print(cap[1])
# print(cap)
# cap.close()
