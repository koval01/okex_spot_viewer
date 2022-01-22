from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api

from utils.GridJson import GridJson

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


class DataJson(Resource):
    @staticmethod
    def get() -> jsonify:
        return GridJson().getData()


api.add_resource(DataJson, '/')

if __name__ == "__main__":
    app.run()
