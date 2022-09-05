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
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'please'    

# Setup database
client = MongoClient('mongodb://root:superSecretPassword@mongo:27017/napkin?authSource=admin')
db = client.get_default_database()
napkins = db.napkins
users = Users(db)

@app.context_processor
def inject_context():
    all_napkins = list(napkins.find({'owner': session['user']}))
    current_user = users.users.find_one({'_id': ObjectId(session['user'])})
    return dict(all_napkins=all_napkins, current_user=current_user)



# Auth middlewear 
def login_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user' not in session:
                return redirect('/login')
            else:
                user = users.find_user(ObjectId(session['user']))
                if user == None:
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
@app.route("/", methods=['GET'])
def landing_page():
    return render_template('landing.html')

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
        print(user)
        if user != False:
            session['user'] = str(user['_id'])
            return redirect('/index')
        else: 
            return redirect('/login')

@app.route('/logout')
def logout():
    session['user'] = None 
    return redirect('/login')

# Index view         
@app.route("/index")
@login_required()
def index():
    all_napkins = list(napkins.find({'owner': session['user']}))
    
    return render_template('index.html', napkins=all_napkins, user=session['user'])

# Napkin detail view 
@app.route("/napkin/<_id>")
@login_required()
def napkin_detail(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    print(session['user'])
    return render_template('paint.html', napkin=napkin, user=session['user'])

# Create napkin 
@app.route("/create", methods=['GET'])
@login_required()
def create():
    new_napkin = napkins.insert_one({
        'owner': session['user'], 
        'title': 'Untitled Napkin',
        'canvas': {
            'attrs': {'height': 4000, 'width': 1000},
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
        title = request.form['title']
        napkin = napkins.update_one({'_id': ObjectId(_id)}, {'$set': {'title': title}})
        return 'success'

# Update title 
@app.route("/update-title/<_id>", methods=['POST'])
@login_required()
def update_title(_id):
        title = request.form['title']
        napkin = napkins.update_one({'_id': ObjectId(_id)}, {'$set': {'title': title}})
        return redirect(f'/napkin/{_id}')

# Get napkin json 
@app.route("/get-napkin-canvas/<_id>", methods=['GET'])
def get_napkin_canvas(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return napkin['canvas']

# Delete napkin
@app.route("/delete/<_id>", methods=['GET'])
@login_required()
def delete_napkin(_id):
        napkin = napkins.delete_one({'_id': ObjectId(_id)})
        return redirect('/index')

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'))

    




