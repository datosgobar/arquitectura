#!/usr/bin/python

from flask import Flask
import json

import db_commons

from flask import Flask, jsonify
#from flask_marshmallow import Marshmallow
#from marshmallow import Schema, fields, ValidationError, pre_load

#from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
#ma = Marshmallow(app)

class IrisSchema(ModelSchema):
    #fields = ("sepal_length", "sepal_width", "petal_length", "petal_width", "flower_class")
    class Meta:
        model = db_commons.Iris

iris_schema = IrisSchema(many=True)

@app.route('/getdata')
def getdata():
    session = db_commons.get_session()
    ret = []
    for d in session.query(db_commons.Iris).all() :
        ret_e = {}
        for a in ["sepal_length", "sepal_width", "petal_length", "petal_width", "flower_class"] :
            ret_e[a] = getattr(d, a)
        ret += [ret_e]
    return json.dumps(ret)
    #author_schema.dump(author).data

@app.route('/')
def index():
    data = open("index.html").read()
    return data

if __name__ == '__main__':
    app.run(debug=True)