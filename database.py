from os import environ
from pymongo import MongoClient
from flask import Flask, current_app
import bcrypt
from bson.objectid import ObjectId
import datetime
import string
import random

class MongoDB():

    def __init__(self):
        client = MongoClient(environ.get('MONGODB_URI'))
        self.db = client[environ.get('MONGODB_DATABASE', 'napkin')]

    def load_app(self):
        """Loads the current application and makes changes to db in needed"""
        self.users = self.db.users
        self.napkins = self.db.napkins
        
database = MongoDB()