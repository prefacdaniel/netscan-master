from flask import Flask, Response

from repository.database_connection import query_db_get_json

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/feature')
def get_feature():
    json_feature = query_db_get_json("SELECT * FROM feature")
    return Response(json_feature, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
