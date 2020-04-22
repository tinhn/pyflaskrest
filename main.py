#!/usr/bin/env python
from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource


from api.student import SchoolBoy
from api.customers import Customer
from common.logger import Logger
from common.mongoDB import VNEDU_DB, CRM_DB

AP_HOST='0.0.0.0'
AP_PORT=5000

app = Flask(__name__, template_folder="templates")
api = Api(app, default_mediatype='application/json')

##
## Mongodb Edu database connect
##
mongo_edu = VNEDU_DB(app)
edu_db = mongo_edu.getDb()

##
## Mongodb Crm database connect
##
mongo_crm = CRM_DB(app)
crm_db = mongo_crm.getDb()

@app.route("/", methods = ['GET'])
def get_home():
    return render_template('home.html')

##
## Actually setup the Api resource routing here
##
def edu_routes(api, db):
    api.add_resource(SchoolBoy, "/v1/hs", "/v1/hs/<int:phone>", resource_class_kwargs={'db': edu_db})
    
def crm_routes(api, db):
    api.add_resource(Customer, "/v1/crm", "/v1/crm/<int:id>", resource_class_kwargs={'db': crm_db})
    

def main(host, port, debug):
    Logger(app)
    app.run(host, port, debug)

##
## Call Api resource routing
##
edu_routes(api, edu_db)
crm_routes(api, crm_db)

if __name__ == '__main__':
    main(host=AP_HOST, port=AP_PORT, debug=True)
    # main(debug=True)

