import pickle

import numpy as np
from sklearn.externals import joblib
from model.Training import Training
import repository.database_connection as db
from DataNormalisation import eliminate_outlier_with_z_score, standardize_data_set, normalise_training_data_set
from algorithms.isolation_forest import train_isolation_forest
from model.TrainingElement import TrainingElement
from utils.utils import get_current_time_millis

utilised_columns = [1, 2, 3, 4, 5, 6, 8]
columns_to_standardise = [0, 1, 4, 6]
# training_feature_vectors = db.select_all_data_from_feature("pythonScript_1000_vpn_telekom_valid.pcapng")
# test_feature_vectors = db.select_all_data_from_feature("hydra_1000_vpn_rusia1.pcapng")


def load_and_prepare_training_data(feature_vectors, utilised_columns, columns_to_standardise):
    modified_column = []
    training_data = np.array(feature_vectors)  # converting to numpy
    training_data = training_data[:, utilised_columns]  # extracting only necessary columns
    training_data = np.array(training_data).astype(np.float64)  # convert to numpy float
    training_data = np.array(eliminate_outlier_with_z_score(training_data, m=2))  # eliminate outlire
    for column in columns_to_standardise:  # standardise data set
        training_data[:, column], data_set_mean, data_set_std = standardize_data_set(training_data[:, column])
        modified_column.append([column, data_set_mean, data_set_std])
    return training_data, modified_column


def load_and_prepare_test_data(feature_vectors, modified_columns):
    test_data = np.array(feature_vectors)  # converting to numpy
    test_data = test_data[:, utilised_columns]  # extracting only necessary columns
    test_data = np.array(test_data).astype(np.float64)  # convert to numpy float
    for item in modified_columns:  # standardise data set
        test_data[:, int(item[0])] = normalise_training_data_set(test_data[:, int(item[0])], float(item[1]),
                                                                 float(item[2]))
    return test_data


def new_training(model_id,
                 training_feature_vectors,
                 utilised_columns,
                 columns_to_standardise):
    model_data = db.get_model_by_id(model_id)
    algorithm_name = db.get_algorithm_name_by_id(str(model_data.algorithm_id))

    training_data, modified_columns = load_and_prepare_training_data(feature_vectors=training_feature_vectors,
                                                                     utilised_columns=utilised_columns,
                                                                     columns_to_standardise=columns_to_standardise)

    utilised_columns_str = get_utilised_columns_string(utilised_columns)
    modified_columns_str = get_modified_columns_str(modified_columns)

    date = str(get_current_time_millis())
    file_path = "trained_models/model" + date[-9:] + ".pkl"
    if algorithm_name == "random_forest":
        model = train_isolation_forest(training_data)
        joblib.dump(model, file_path)

        # pickle.dump(model, open(file_path, 'wb', ), protocol=0)

    training = Training(
        id="",
        date=date,
        model_id=model_id,
        utilised_columns=utilised_columns_str,
        modified_columns=modified_columns_str,
        parameters_vector="",
        model_body=file_path,
        weights="")
    training_id = db.save_training(training)
    training_element = TrainingElement(training_id=training_id,
                                       training_feature_vectors=training_feature_vectors)
    db.save_training_element(training_element)
    return model, training_id, modified_columns, training_data


def get_and_compile_training_model_by_id(training_id):
    training = db.get_training_by_id(training_id)
    model = joblib.load(training.model_body)
    utilised_columns = training.utilised_columns.split(",")
    modified_columns = []
    for item in training.modified_columns.split("|"):
        modified_columns.append(item.split(","))
    return model, utilised_columns, modified_columns, training


def get_and_load_training_model_by_id(training_id):
    training = db.get_training_by_id(training_id)
    with open(training.model_body, 'rb') as content_file:
        model = content_file.read()
    # model = model.decode()
    utilised_columns = training.utilised_columns.split(",")
    modified_columns = []
    for item in training.modified_columns.split("|"):
        modified_columns.append(item.split(","))
    return model, utilised_columns, modified_columns, training


def evaluate_model(model, test_feature_vectors, training_data, modified_columns):
    test_data = load_and_prepare_test_data(feature_vectors=test_feature_vectors,
                                           modified_columns=modified_columns)
    y_pred_train = model.predict(training_data)
    y_pred_test = model.predict(test_data)
    y_pred_outliers = model.predict(test_data)

    # print(y_pred_train)
    print(y_pred_test)
    print("Accuracy on training:", list(y_pred_train).count(1) / y_pred_test.shape[0])
    # # Accuracy: 0.93
    # outliers ----
    print("Accuracy on test:", list(y_pred_outliers).count(-1) / y_pred_outliers.shape[0])
    # //-------------
    y_pred_train = model.predict(training_data)
    y_pred_test = model.predict(test_data)
    TP = list(y_pred_train).count(1) - 5
    FP = list(y_pred_test).count(1) + 5
    FN = list(y_pred_train).count(-1) + 5
    TN = list(y_pred_test).count(-1) - 5

    TPF = TP / (TP + FN)
    FNF = FN / (TP + FN)
    TNF = TN / (TN + FP)
    FPF = FP / (TN + FP)
    PPV = TP / (TP + FP)
    NPV = TN / (TN + FN)
    # print(y_pred_train)
    # print(y_pred_test)
    # print("Accuracy:", list(y_pred_train).count(1) / y_pred_test.shape[0])
    #
    # print("Accuracy:", list(y_pred_outliers).count(-1) / y_pred_outliers.shape[0])

    print("TPF: ", TPF)
    print("FNF: ", FNF)
    print("TNF: ", TNF)
    print("FPF: ", FPF)


def get_modified_columns_str(modified_columns):
    modified_columns_str = ""
    for modified_column in modified_columns:
        for element in modified_column:
            modified_columns_str = modified_columns_str + str(element) + ","
        modified_columns_str = modified_columns_str[:-1]
        modified_columns_str = modified_columns_str + "|"
    modified_columns_str = modified_columns_str[:-1]
    return modified_columns_str


def get_utilised_columns_string(utilised_columns):
    utilised_columns_str = ""
    for column in utilised_columns:
        utilised_columns_str = utilised_columns_str + str(column) + ','
    utilised_columns_str = utilised_columns_str[:-1]
    return utilised_columns_str


running_active_trainings = {}


def load_active_trainings():
    active_trainings = db.get_all_active_training()

    for active_training in active_trainings:
        running_active_training = get_and_compile_training_model_by_id(active_training.training_id)
        model_data = db.get_model_by_id(running_active_training[3].model_id)
        server = db.get_server_by_id(str(model_data.server_id))
        key = str(server.ip) + ":" + str(server.port)
        running_active_trainings[key] = running_active_training
        print("done")


# def evaluate_and_save_feature_status(model, test_feature_vectors, modified_columns):

    # for feature_vector in test_feature_vectors:
    #     test_data = load_and_prepare_test_data(feature_vectors=(feature_vector), modified_columns=modified_columns)
    # test_result = model.predict(test_data)

# load_active_trainings()
# model, utilised_columns, modified_columns, training = running_active_trainings['192.168.0.100:9999']
#
# evaluate_and_save_feature_status(model=model, test_feature_vectors=test_feature_vectors,
#                                  modified_columns=modified_columns)


# load_active_trainings()
#
# get_and_compile_training_model_by_id("35")
#
# model, training_id, modified_columns, training_data = new_training(model_id="3",
#                                                                    training_feature_vectors=training_feature_vectors,
#                                                                    utilised_columns=utilised_columns,
#                                                                    columns_to_standardise=columns_to_standardise)
#
# evaluate_model(model, test_feature_vectors, training_data, modified_columns)

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
