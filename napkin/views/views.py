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

views = Blueprint('views', __name__, template_folder="templates", static_folder="static")
users = Users(database)
napkins = database.napkins

@views.context_processor
def inject_context():
    if 'user' in session.keys() and users.users.find_one({'_id': ObjectId(session['user'])}):
            all_napkins = list(napkins.find({'owner': session['user']}))
            current_user = users.users.find_one({'_id': ObjectId(session['user'])})
            return dict(all_napkins=all_napkins, current_user=current_user)
    else:
        return dict(no_session=True)

# User registration 
@views.route("/", methods=['GET'])
def landing_page():
    if 'user' in session.keys() and users.users.find_one({'_id': ObjectId(session['user'])}):
        return redirect('/index')
    return render_template('landing.html')

# User registration 
@views.route("/register", methods=['GET'])
def register():
    if 'user' in session.keys() and users.users.find_one({'_id': ObjectId(session['user'])}):
        return redirect('/index')
    else:
        return render_template('auth/register.html')

@views.route('/login', methods=['GET'])
def login():
    if 'user' in session.keys() and users.users.find_one({'_id': ObjectId(session['user'])}):
        return redirect('/index')
    return render_template('/auth/login.html')

# Index view         
@views.route("/napkins")
@login_required()
def list_view():
    all_napkins = list(napkins.find({'owner': session['user']}))
    return render_template('napkins.html', napkins=all_napkins, user=session['user'])

# Napkin detail view 
@views.route("/napkin/<_id>")
@login_required()
def detail_view(_id):
    napkin = napkins.find_one({'_id': ObjectId(_id)})
    return render_template('napkin.html', napkin=napkin, user=session['user'])
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'))

    




