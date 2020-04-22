from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
from time import mktime
from common.logger import Logger

from flask import jsonify, request
from flask_restful import fields, marshal_with, reqparse, Resource, abort

# customers table field
cust_fields = {
    "customerid": fields.String,
    "name": fields.String,
    "age": fields.String,
    "address": fields.String,
    "salary": fields.String,
    # "id": fields.String(attribute="_id"),
}

created_cust_response = {
    'id': fields.String(attribute="_id")
}

def _getTimestamp(dt):
    return round(mktime(dt.timetuple()) + dt.microsecond / 1e6)

@marshal_with(cust_fields)
def cust_success(result):
    return json_util._json_convert(result)

class Customer(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.table = 'customers'

    def get(self, id=None):
        data = []
        LIMIT_REC = 50
        
        if request.args:
            data = request.args

        if id is not None:
            cust_info = self.db[self.table].find_one({"customerid": id})
            if cust_info:
                return cust_success(cust_info)
            else:
                abort(404, message="Id {} doesn't exist".format(id))
            
        if data:
            age = int(data['age'])
            query = {
                    "age": age
                }
            cursor = self.db[self.table].find(query).limit(LIMIT_REC)

            respond = []
            for cust_info in cursor:
                respond.append(cust_info)
            
            return cust_success(respond)
            
        cursor = self.db[self.table].find({}).limit(LIMIT_REC)
        respond = []
        for cust_info in cursor:
            respond.append(cust_info)

        return cust_success(respond)

    @marshal_with(created_cust_response)
    def post(self):
        data = request.get_json()
        if not data:
            abort(400, response="ERROR")
        
        data['created_at'] = _getTimestamp(datetime.utcnow())
        customer_info = self.db[self.table].insert_one(data)
        return {
                    "_id": str(customer_info.inserted_id)
                }, 201

    def put(self):
        data = request.get_json()
    
        if data and "id" in data:                
            data['updated_at'] = _getTimestamp(datetime.now())

            q = {"_id": ObjectId(data['id'])}

            self.db[self.table].update(q, {'$set': data})

            cust_info = self.db[self.table].find_one(q)
            if cust_info:
                return cust_success(cust_info)
            
        data = {"response": "ERROR"}
        return data, 400

    def delete(self):
        data = []
        if request.args:
            data = request.args
            
        if data and "id" in data:
            self.db[self.table].remove({"_id": ObjectId(data['id'])})
            return {"response": "SUCESS"}, 200

        data = {"response": "ERROR"}
        return (data), 400