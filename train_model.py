import numpy as np

from model.Training import Training
import repository.database_connection as db
from DataNormalisation import eliminate_outlier_with_z_score, normalise_data_set, normalise_training_data_set
from algorithms.isolation_forest import train_isolation_forest
from utils.utils import get_current_time_millis

utilised_columns = [1, 2, 3, 4, 5, 6, 8]
columns_to_standardise = [0, 1, 4, 6]
training_feature_vectors = db.select_all_data_from_feature("pythonScript_1000_vpn_telekom_valid.pcapng")
test_feature_vectors = db.select_all_data_from_feature("hydra_1000_vpn_rusia1.pcapng")


def load_and_prepare_training_data(feature_vectors, utilised_columns, columns_to_standardise):
    modified_column = []
    training_data = np.array(feature_vectors)  # converting to numpy
    training_data = training_data[:, utilised_columns]  # extracting only necessary columns
    training_data = np.array(training_data).astype(np.float64)  # convert to numpy float
    training_data = np.array(eliminate_outlier_with_z_score(training_data, m=2))  # eliminate outlire
    for column in columns_to_standardise:  # standardise data set
        training_data[:, column], data_set_mean, data_set_std = normalise_data_set(training_data[:, column])
        modified_column.append([column, data_set_mean, data_set_std])
    return training_data, modified_column


#


def load_and_prepare_test_data(feature_vectors, modified_columns):
    test_data = np.array(feature_vectors)  # converting to numpy
    test_data = test_data[:, utilised_columns]  # extracting only necessary columns
    test_data = np.array(test_data).astype(np.float64)  # convert to numpy float
    for item in modified_columns:  # standardise data set
        test_data[:, item[0]] = normalise_training_data_set(test_data[:, item[0]], item[1], item[2])
    return test_data


training_data, modified_columns = load_and_prepare_training_data(feature_vectors=training_feature_vectors,
                                                                 utilised_columns=utilised_columns,
                                                                 columns_to_standardise=columns_to_standardise)

test_data = load_and_prepare_test_data(feature_vectors=test_feature_vectors,
                                       modified_columns=modified_columns)


def new_training(model_id,
                 training_feature_vectors,
                 test_feature_vectors,
                 utilised_columns,
                 columns_to_standardise):
    model_data = db.get_model_by_id(model_id)
    algorithm_name = db.get_algorithm_name_by_id(str(model_data[2]))  # model[2] is algorithm id

    training_data, modified_columns = load_and_prepare_training_data(feature_vectors=training_feature_vectors,
                                                                     utilised_columns=utilised_columns,
                                                                     columns_to_standardise=columns_to_standardise)
    test_data = load_and_prepare_test_data(feature_vectors=test_feature_vectors,
                                           modified_columns=modified_columns)

    utilised_columns_str = ""
    for column in utilised_columns:
        utilised_columns_str = utilised_columns_str + str(column) + ','
    utilised_columns_str = utilised_columns_str[:-1]

    modified_columns_str = ""

    for modified_column in modified_columns:
        for element in modified_column:
            modified_columns_str = modified_columns_str + str(element) + ","
        modified_columns_str = modified_columns_str[:-1]
        modified_columns_str = modified_columns_str + "|"
    modified_columns_str = modified_columns_str[:-1]

    if algorithm_name == "ann":
        pass  # todo
    elif algorithm_name == "kmeans":
        pass  # todo
    elif algorithm_name == "random_forest":
        model = train_isolation_forest(training_data)

        y_pred_train = model.predict(training_data)
        y_pred_test = model.predict(test_data)
        y_pred_outliers = model.predict(test_data)
        #

        # print(y_pred_train)
        print(y_pred_test)

        print("Accuracy:", list(y_pred_train).count(1) / y_pred_test.shape[0])
        # # Accuracy: 0.93

        # outliers ----
        print("Accuracy:", list(y_pred_outliers).count(-1) / y_pred_outliers.shape[0])
    # elif #todo throw exception
    training = Training(
        id="",
        date=get_current_time_millis(),
        model_id=model_id,
        utilised_columns=utilised_columns_str,
        modified_columns=modified_columns_str,
        parameters_vector="",
        model_body="",
        weights="")
    db.save_training(training)


new_training(model_id="3",
             training_feature_vectors=training_feature_vectors,
             test_feature_vectors=test_feature_vectors,
             utilised_columns=utilised_columns,
             columns_to_standardise=columns_to_standardise)

# Y = np.zeros(len(training_data))
# np.random.seed(7)
#
# model = create_ann(x=training_data, y=Y, a1="relu", a2= "relu", a3="sigmoid", input_dim=7, l1_nnumber=13,
#                    l2_nnumber=8)  # try also with l2 deleted

# prediction = model.predict(training_data)
# print(prediction)
#
# scores = model.evaluate(training_data, Y)
# print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0] * 100))
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
# print("My ev:")
# print("evaluate training data")
# # prediction = model.predict_classes(training_data)
# # print(prediction)
# prediction = model.predict(training_data)
# print(prediction)
# test_Y = np.ones(len(test_data))
# scores = model.evaluate(test_data, test_Y)
# print("\n%s: %.2f%%" % (model.metrics_names[0], scores[0] * 100))
# print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
