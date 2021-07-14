import sys
from flask import Flask, render_template, request, Response, redirect
import json
import os
from os import environ
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Setup database
client = MongoClient('mongodb://root:superSecretPassword@mongo:27017/napkin?authSource=admin')
db = client.get_default_database()
napkins = db.napkins

@app.route("/index")
def index():
    notes = napkins.find()
    return render_template('index.html', napkins=notes)

@app.route("/napkin/<_id>")
def paint(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return render_template('paint.html', napkin=napkin)

@app.route("/create", methods=['GET'])
def create():
    new_napkin = napkins.insert_one({
        'title': 'Untitled Napkin',
        'canvas': {
            'attrs': {'height': 562, 'width': 1920},
            'className': 'Stage',
            'children': []
        }
    })
    return redirect(f'/napkin/{new_napkin.inserted_id}')

@app.route("/update/<_id>", methods=['POST'])
def update(_id):
    if request.form['canvas']:
        canvas = json.loads(request.form['canvas'])
        napkin = napkins.update_one({'_id': ObjectId(_id)}, {'$set': {'canvas': canvas}})
        return 'success'

@app.route("/get-napkin-canvas/<_id>", methods=['GET'])
def get_napkin_canvas(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return napkin['canvas']

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response