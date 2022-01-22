from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Resource, Api

from network.recaptcha import Recaptcha
from utils.GridJson import GridJson

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
api = Api(app)
CORS(app)


class DataJson(Resource):
    @staticmethod
    def post() -> jsonify:
        if Recaptcha(request.get_json()["re_token"]).check_token():
            return GridJson().get()


api.add_resource(DataJson, '/')

if __name__ == "__main__":
    app.run()
