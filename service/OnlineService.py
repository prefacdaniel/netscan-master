import json
from collections import namedtuple

from sklearn.externals import joblib

from repository.database_connection import select_all_data_from_feature
from service.rest_service import get_request_by_id, get_training_for_device, get_training_model_for_device
from train_model import evaluate_and_save_feature_status, load_and_prepare_test_data


def load_training_and_model_by_device(device_id):
    active_training = get_training_for_device(device_id)
    active_training = json.loads(active_training, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    active__model = get_training_model_for_device(device_id)
    with open(active_training.training.model_body, 'wb') as content_file:
        content_file.write(active__model)

    model = joblib.load(active_training.training.model_body)
    return active_training, model


#
# test_feature_vectors = select_all_data_from_feature("hydra_1000_vpn_rusia1.pcapng")
# training_feature_vectors = select_all_data_from_feature("pythonScript_1000_vpn_telekom_valid.pcapng")
#
# active_training, model = load_training_and_model_by_device(1)
#
# test_data = load_and_prepare_test_data(feature_vectors=[test_feature_vectors[0]],
#                                        modified_columns=active_training.modified_columns)
#
# training_data = load_and_prepare_test_data(feature_vectors=training_feature_vectors,
#                                            modified_columns=active_training.modified_columns)
#
# y_pred_test = model.predict(test_data)
# if y_pred_test[0].astype(int) == 1:
#     print("normal")
# elif y_pred_test[0].astype(int) == -1:
#     print("attack")
#
# print("Accuracy on training:", list(y_pred_test).count(-1) / test_data.shape[0])
#
# y_pred_training = model.predict(training_data)
# print("Accuracy on test:", list(y_pred_training).count(1) / training_data.shape[0])
