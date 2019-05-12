import numpy as np

from KarasANN import create_ann
from database_connection import select_all_data_from_feature
from DataNormalisation import eliminate_outlier_with_z_score, normalise_data_set, normalise_training_data_set


def new_training(model_id, feature_vectors, utilised_columns, columns_to_standardise):
    modified_column = []
    training_data = np.array(feature_vectors)  # converting to numpy
    training_data = training_data[:, utilised_columns]  # extracting only necessary columns
    training_data = np.array(training_data).astype(np.float64)  # convert to numpy float
    training_data = np.array(eliminate_outlier_with_z_score(training_data, m=2))  # eliminate outlire
    for column in columns_to_standardise:  # standardise data set
        training_data[:, column], data_set_mean, data_set_std = normalise_data_set(training_data[:, column])
        modified_column.append([column, data_set_mean, data_set_std])


columns_to_standardise = [0, 1, 4, 6]
utilised_columns = [1, 2, 3, 4, 5, 6, 8]

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

Y = np.ones(len(training_data))
np.random.seed(7)

model = create_ann(x=training_data, y=Y, input_dim=7, l1_nnumber=13, l2_nnumber=4)  # try also with l2 deleted

test_data = select_all_data_from_feature("hydra_1000_vpn_rusia1.pcapng")

test_data = np.array(test_data)  # converting to numpy
test_data = test_data[:, utilised_columns]  # extracting only necessary columns
test_data = np.array(test_data).astype(np.float64)  # convert to numpy float
for item in modified_column:  # standardise data set
    test_data[:, item[0]] = normalise_training_data_set(test_data[:, item[0]], item[1], item[2])



print("evaluate training data")
prediction = model.predict_classes(training_data)
print(prediction)
prediction = model.predict(training_data)
print(prediction)

prediction = model.predict(test_data)
print(prediction)

scores = model.evaluate(training_data, Y)
print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0] * 100))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
print("My ev:")
test_Y = np.zeros(len(test_data))
scores = model.evaluate(test_data, test_Y)
print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0] * 100))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
