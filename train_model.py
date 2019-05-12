import numpy as np

from database_connection import select_all_data_from_feature
from practiceNumpy import eliminate_outlier_column, reject_outliers, eliminate_outlier, detect_outlier, \
    eliminate_outlier_with_z_score


def new_training(model_id, feature_vectors):
    pass


telekom_data = select_all_data_from_feature("pythonScript_1000_vpn_telekom_valid.pcapng")

# for t in telekom_data:
#     print(t)
training_data = np.array(telekom_data)  # converting to numpy
print("numpy data: ")
print(training_data[0])
training_data = training_data[:, [1, 2, 3, 4, 5, 6, 8]]  # extracting only necessary columns
print("remaining numpy data: ")
print(training_data[0])
training_data = np.array(training_data).astype(np.float64)
print("numpy data after convetions: ")
print(training_data[0])
print("mean: ")
print(np.mean(training_data, axis=0))
print("std: ")
print(np.std(training_data, axis=0))
print("initial size", len(training_data))
training_data = eliminate_outlier_with_z_score(training_data, m=2)
print("size after` eliminating outliers", len(training_data))

