import json

from flask import Flask, Response, request

from model.Server import Server
from repository.database_connection import query_db_get_json, save_server, get_device_data_by_id, \
    get_connection_for_device_from_date_from_db, update_connection_status_in_db

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
