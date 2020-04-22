from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
from time import mktime
from common.logger import Logger

from flask import jsonify, request
from flask_restful import fields, marshal_with, reqparse, Resource, abort

# student table field
schboy_fields = {
    "studenid": fields.String,
    "firstname": fields.String,
    "lastname": fields.String,
    "age": fields.String,
    "phone": fields.String,
    "city": fields.String,
    # "id": fields.String(attribute="_id"),
}

created_hs_response = {
    'id': fields.String(attribute="_id")
}

def _getTimestamp(dt):
    return round(mktime(dt.timetuple()) + dt.microsecond / 1e6)

@marshal_with(schboy_fields)
def schboy_success(result):
    return json_util._json_convert(result)

class SchoolBoy(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
        self.table = 'student'

    def get(self, phone=None):
        data = []
        LIMIT_REC = 50
        
        if request.args:
            data = request.args

        if phone is not None:
            hs_info = self.db[self.table].find_one({"phone": phone})
            if hs_info:
                return schboy_success(hs_info)
            else:
                abort(404, message="Phone {} doesn't exist".format(phone))
            
        if data:
            city_name = str(data['city'])
            query = {
                    "city": city_name
                }
            cursor = self.db[self.table].find(query).limit(LIMIT_REC)

            respond = []
            for hs_info in cursor:
                respond.append(hs_info)
            
            return schboy_success(respond)
            
        cursor = self.db[self.table].find({}).limit(LIMIT_REC)
        respond = []
        for hs_info in cursor:
            respond.append(hs_info)

        return schboy_success(respond)

    @marshal_with(created_hs_response)
    def post(self):
        data = request.get_json()
        if not data:
            abort(400, response="ERROR")
        
        data['created_at'] = _getTimestamp(datetime.utcnow())
        room = self.db[self.table].insert_one(data)
        return {
                    "_id": str(room.inserted_id)
                }, 201

    def put(self):
        data = request.get_json()
    
        if data and "id" in data:                
            data['updated_at'] = _getTimestamp(datetime.now())

            q = {"_id": ObjectId(data['id'])}

            self.db[self.table].update(q, {'$set': data})

            hs_info = self.db[self.table].find_one(q)
            if hs_info:
                return schboy_success(hs_info)
            
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