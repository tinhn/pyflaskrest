import flask_pymongo
import conf.databaseconfig as cfg
import urllib.parse

class VNEDU_DB:
    def __init__(self, app):
        db_host = cfg.mongodb['host']
        db_port = cfg.mongodb['port']
        db_name = cfg.mongodb['db']
        
        uri = "mongodb://{host}:{port}/{db}?ssl=false".format(host=db_host, port=db_port, db=db_name)

        if "user" in cfg.mongodb:
            uri = "mongodb://{user}:{pwd}@{host}:{port}/{db}".format(user=cfg.mongodb['user'], pwd=urllib.parse.quote(cfg.mongodb['password']), host=db_host, port=db_port, db=db_name)

        client = flask_pymongo.MongoClient(uri)

        self.client = client
        self.db = client[cfg.mongodb['db']]
    
    def getClient(self):
        return self.client
    
    def getDb(self):
        return self.db
    
class CRM_DB:
    def __init__(self, app):
        db_host = cfg.crmdb['host']
        db_port = cfg.crmdb['port']
        db_name = cfg.crmdb['db']
        
        uri = "mongodb://{host}:{port}/{db}?ssl=false".format(host=db_host, port=db_port, db=db_name)

        if "user" in cfg.crmdb:
            uri = "mongodb://{user}:{pwd}@{host}:{port}/{db}".format(user=cfg.crmdb['user'], pwd=urllib.parse.quote(cfg.crmdb['password']), host=db_host, port=db_port, db=db_name)

        client = flask_pymongo.MongoClient(uri)

        self.db = client[cfg.crmdb['db']]
        self.client = client
        
    def getDb(self):
        return self.db    

    def getClient(self):
        return self.client