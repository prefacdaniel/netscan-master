from database_connection import insert_data
import sniffer

full_path = "C:\\Users\\dprefac\\PycharmProjects\\netscan-master\\wiresharkScans\\home_test\\"
file_name = "hydra_1000_vpn_rusia1.pcapng"

feature_vectors = sniffer.capture_traffic_from_file(file_path=full_path + file_name)

print("Start inserting data")
insert_data(feature_vectors, file_name)
print("Done inserting data")
