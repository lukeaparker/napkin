import sys
from flask import Blueprint, request, jsonify, redirect, session, g, render_template
import json
import os
from bson.objectid import ObjectId
import bcrypt 
from datetime import date
from napkin.api.models import Users as Users
from database import database
from napkin.utils import login_required

api = Blueprint('api', __name__)
users = Users(database)
napkins = database.napkins

@api.route('/register', methods=['POST'])
def register():
    user = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'password': bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt()),
    }
    users.create_user(user)
    return redirect('/login')

@api.route('/login', methods=['POST'])
def login():
    user = users.verify_credentials({
        'email': request.form.get('email'),
        'password': request.form.get('password').encode('utf-8'),
    })
    if user != False:
        session['user'] = str(user['_id'])
        return redirect('/napkins')
    else: 
        return redirect('/login')

@api.route('/logout')
def logout():
    session['user'] = None 
    return redirect('/')

# Create napkin 
@api.route("/create", methods=['GET'])
@login_required()
def create():
    new_napkin = napkins.insert_one({
        'title': 'Untitled Napkin',
        'owner': session['user'], 
        'date_created': str(date.today()),
        'canvas': {
            'attrs': {'height': 4000, 'width': 1000},
            'className': 'Stage',
            'children': []
        }
    })
    return redirect(f'/napkin/{new_napkin.inserted_id}')

# Update napkin 
@api.route("/update/<_id>", methods=['POST'])
@login_required()
def update(_id):
    if 'canvas' in request.form.keys():
        canvas = json.loads(request.form['canvas'])
        napkin = napkins.update_one({'_id': ObjectId(_id)}, {'$set': {'canvas': canvas}})
        return 'success'
    if 'title' in request.form.keys():
        title = request.form['title']
        napkin = napkins.update_one({'_id': ObjectId(_id)}, {'$set': {'title': title}})
        return redirect(f'/napkin/{_id}')

# Delete napkin
@api.route("/delete/<_id>", methods=['GET'])
@login_required()
def delete_napkin(_id):
        napkin = napkins.delete_one({'_id': ObjectId(_id)})
        return redirect('/napkins')

# Get napkin json 
@api.route("/get/napkin/canvas/<_id>", methods=['GET'])
@login_required()
def get_napkin_canvas(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return napkin['canvas']

