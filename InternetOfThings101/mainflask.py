#!/usr/bin/python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Network(Resource):
    def get(self):
        data = 'Network Data'
        return data

api.add_resource(Network, '/network')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
