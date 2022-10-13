

from flask import session, redirect
import sys
import json
import os
from os import environ
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt 
from functools import wraps
from napkin.api.models import Users as Users
from database import database
users = Users(database)

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

