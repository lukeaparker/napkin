import sys
from flask import Flask, render_template, request, Response, redirect, session
import json
import os
from os import environ
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt 
from functools import wraps
from models import Users


app = Flask(__name__)
print('you bitch')
app.config['SECRET_KEY'] = 'please'    
print('you bitch')

# Setup database
client = MongoClient('mongodb://root:superSecretPassword@mongo:27017/napkin?authSource=admin')
db = client.get_default_database()
napkins = db.napkins
users = Users(db)

# Auth middlewear 
def login_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user' not in session:
                return redirect('/login')
            else:
                user = users.find_user(ObjectId(session['user'])
                if user == False:
                    return redirect('/login')
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Request middlewear 
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# User registration 
@app.route("/register", methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('auth/register.html')
    elif request.method == 'POST':
        user = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'password': bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt()),
        }
        users.create_user(user)
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/auth/login.html')
    elif request.method == 'POST':
        user_credentials = {
            'email': request.form.get('email'),
            'password': request.form.get('password').encode('utf-8'),
        }
        user = users.verify_credentials(user_credentials)
        if user != False:
            session['user'] = str(user['_id'])
            return redirect('/index')
        else: 
            return redirect('/login')


@app.route('/logout')
def logout():
    session['user'] = None 
    return redirect('/logout')

# Index view         
@app.route("/index")
@login_required()
def index():
    notes = napkins.find({'owner': session['user']})
    return render_template('index.html', napkins=notes)

# Napkin detail view 
@app.route("/napkin/<_id>")
def napkin_detail(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return render_template('paint.html', napkin=napkin)

# Create napkin 
@app.route("/create", methods=['GET'])
def create():
    new_napkin = napkins.insert_one({
        'owner': session['user'], 
        'title': 'Untitled Napkin',
        'canvas': {
            'attrs': {'height': 562, 'width': 1920},
            'className': 'Stage',
            'children': []
        }
    })
    return redirect(f'/napkin/{new_napkin.inserted_id}')

# Update napkin 
@app.route("/update/<_id>", methods=['POST'])
def update(_id):
    if request.form['canvas']:
        canvas = json.loads(request.form['canvas'])
        napkin = napkins.update_one({'_id': ObjectId(_id)}, {'$set': {'canvas': canvas}})
        return 'success'
# Get napkin json 
@app.route("/get-napkin-canvas/<_id>", methods=['GET'])
def get_napkin_canvas(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return napkin['canvas']


    




