from flask import Flask, request, jsonify, abort, make_response, url_for
from flask_restful import Resource, Api, reqparse, fields, marshal
import pyodbc
import config
import json
import logging
from applicationinsights.logging import enable


app = Flask(__name__)
api = Api(app)

sampleTable_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'value': fields.String
}

dataTable_fields = {
    'id': fields.Integer,
    'datavalue': fields.Integer
}

class AzureSQLDatabase(object):
    connection = None
    cursor = None

    def __init__(self):
        self.connection = pyodbc.connect(config.CONN_STRING)
        self.cursor = self.connection.cursor()

    def query(self, query):
        return self.cursor.execute(query)
    
    def commit(self):
        return self.connection.commit()
    
    def __del__(self):
        self.connection.close()

class HelloWorld(Resource):
    def get(self):
        # set up logging
        # enable('29c9677a-bf5d-4d42-a88c-c6cbb4cb952f')
        enable('43fd2869-a1d1-454d-a151-926f64f4a230')

        # log something (this will be sent to the Application Insights service as a trace)
        logging.info('This is a message to app insight')

        # logging shutdown will cause a flush of all un-sent telemetry items
        logging.shutdown()
        
        logging.basicConfig(filename='/home/LogFiles/myapp.log', filemode='w', format='%(name)s - %(levelname)s, %(message)s')
        logging.warning('This will get logged in file')
        return {'message': 'Hello world!!'}

class HelloWorldv2(Resource):
    def get(self):
        try:
            sql = u"select * from sampleTable"
            conn = AzureSQLDatabase()
            cursor = conn.query(sql)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))

            return {
                'data': marshal(data, sampleTable_fields)
            }
        except Exception as e:
            return {'error': str(e)}


class Testv2(Resource):
    def get(self):
        try:
            sql = u"select * from dataTable"
            conn = AzureSQLDatabase()
            cursor = conn.query(sql)
            columns = [column[0] for column in cursor.description]
            data = []
            for row in cursor.fetchall():
                data.append(dict(zip(columns, row)))

            return {
                'data': marshal(data, dataTable_fields)
            }
        except Exception as e:
            return {'error': str(e)}

api.add_resource(HelloWorld, '/')
api.add_resource(HelloWorldv2, '/api/v1/test')
api.add_resource(Testv2, '/api/v1/test2')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
