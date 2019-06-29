import json
from collections import namedtuple

from flask import Flask, Response, request, make_response

from model.Server import Server
from model.TrainingResponse import TrainingResponse
from repository.database_connection import query_db_get_json, save_server, get_device_data_by_id, \
    get_connection_for_device_from_date_from_db, update_connection_status_in_db, insert_feature_vector, \
    select_all_normal_or_unknown_traffic_data_from_feature, select_all_normal_traffic_data_from_feature, \
    update_current_active_training, get_active_training_for_device
from service.Encode import MyEncoder
from train_model import new_training, get_and_load_training_model_by_id

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/feature')
def get_feature():
    json_feature = query_db_get_json("SELECT * FROM feature")
    return Response(json_feature, status=200, mimetype='application/json')


@app.route('/servers')
def get_servers():
    json_feature = query_db_get_json("SELECT * FROM server")
    return Response(json_feature, status=200, mimetype='application/json')


@app.route('/server', methods=['POST'])
def add_server():
    data = request.data
    data = json.loads(data)
    server = Server(id=data['id'],
                    ip=data['ip'],
                    port=data['port'],
                    name=data['name'],
                    status=data['status'],
                    image=data['image']
                    )
    server_id = save_server(server)
    return Response(server_id, status=200, mimetype='application/json')


@app.route("/date/<deviceid>", methods=['GET'])
def get_dates_for_device(deviceid):
    json_feature = get_device_data_by_id(deviceid)
    return Response(json_feature, status=200, mimetype='application/json')


@app.route("/connections/<deviceid>/<date>", methods=['GET'])
def get_connection_for_device_from_date(deviceid, date):
    date = date.replace("_", "/")
    json_feature = get_connection_for_device_from_date_from_db(deviceid, date)
    return Response(json_feature, status=200, mimetype='application/json')


@app.route('/statusupdate', methods=['POST'])
def update_connection_status():
    data = request.data
    data = json.loads(data)
    updated_connections_number = update_connection_status_in_db(data)
    return Response(updated_connections_number, status=200, mimetype='application/json')


@app.route('/startnewtraining', methods=['POST'])
def start_new_training():
    data = request.data
    data = json.loads(data)
    if data['use_unknown_status_data']:
        training_data = select_all_normal_or_unknown_traffic_data_from_feature()
    else:
        training_data = select_all_normal_traffic_data_from_feature()

    model, training_id, modified_columns, training_data = new_training(model_id="3",
                                                                       training_feature_vectors=training_data,
                                                                       utilised_columns=[1, 2, 3, 4, 5, 6, 8],
                                                                       columns_to_standardise=[0, 1, 4, 6])
    update_current_active_training(training_id=training_id, algorithm_id=3)
    return Response(status=200)


######################python client#########

@app.route('/addfeature', methods=['POST'])
def add_feature():
    data = request.data
    data = json.loads(data)
    feature_vector = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    insert_feature_vector(feature_vector)
    return Response(data, status=200)


@app.route('/getactivetraining/<deviceid>', methods=['GET'])
def get_active_training(deviceid):
    active_training_id = get_active_training_for_device(device_id=deviceid, algorithm_id=3)
    model, utilised_columns, modified_columns, training = get_and_load_training_model_by_id(active_training_id)
    training_response = TrainingResponse(model="",
                                         utilised_columns=utilised_columns,
                                         modified_columns=modified_columns,
                                         training=training)
    return Response(MyEncoder().encode(training_response), status=200)


@app.route('/getactivetrainingmodel/<deviceid>', methods=['GET'])
def get_active_training_model(deviceid):
    active_training_id = get_active_training_for_device(device_id=deviceid, algorithm_id=3)
    model, utilised_columns, modified_columns, training = get_and_load_training_model_by_id(active_training_id)
    response = make_response(model)
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='mdl')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
