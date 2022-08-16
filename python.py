#Libraries
from traceback import print_tb
from flask import Flask,jsonify, render_template, url_for, flash, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from bson import ObjectId
from bson.json_util import dumps

app = Flask(__name__, template_folder='templates')