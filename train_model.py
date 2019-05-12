import numpy as np

from database_connection import select_all_data_from_feature
from DataNormalisation import eliminate_outlier_with_z_score, normalise_data_set

columns_to_standardise = [0, 1, 4, 6]
utilised_columns = [1, 2, 3, 4, 5, 6, 8]


def new_training(model_id, feature_vectors, utilised_columns, columns_to_standardise):
    pass


telekom_data = select_all_data_from_feature("pythonScript_1000_vpn_telekom_valid.pcapng")
modified_column = []
# for t in telekom_data:
#     print(t)
training_data = np.array(telekom_data)  # converting to numpy
print("numpy data: ")
print(training_data[0])
training_data = training_data[:, utilised_columns]  # extracting only necessary columns
print("remaining numpy data: ")
print(training_data[0])
training_data = np.array(training_data).astype(np.float64)
print("numpy data after convetions: ")
print(training_data[0])
print("initial size", len(training_data))
training_data = np.array(eliminate_outlier_with_z_score(training_data, m=2))
print("size after eliminating outliers", len(training_data))
print(training_data[0])
print("initial mean: ")
print(np.mean(training_data, axis=0))
print("initial std: ")
print(np.std(training_data, axis=0))
for column in columns_to_standardise:
    training_data[:, column], data_set_mean, data_set_std = normalise_data_set(training_data[:, column])
    modified_column.append([column, data_set_mean, data_set_std])
print("after mean: ")
print(np.mean(training_data, axis=0))
print("after std: ")
print(np.std(training_data, axis=0))
