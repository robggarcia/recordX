from pymongo import MongoClient
from flask import Flask, redirect, url_for, request, session
from flask_cors import CORS, cross_origin
import json
from bson import ObjectId
from typing import Any
import bcrypt
import os
import jwt
import datetime

from db.mongodb import get_record_collection, get_user_collection
from modules.records import get_all_records, get_single_record, update_record

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

users_col = get_user_collection()
records_col = get_record_collection()


@app.route('/api/health')
def health():
    return {"success": True, "message": "The server is up and running. It is healthy."}


@app.route('/api/records', methods=['GET', 'PUT', 'PATCH'])
def records_route():
    if request.method == 'GET':
        records = get_all_records()
        return {"success": True, "data": records}


@app.route('/api/records/<record_id>')
def album_route(record_id):
    album = get_single_record(record_id)
    return {"success": True, "data": album}


@app.errorhandler(404)
def handle_404(e):
    return {'success': False, 'message': 'Error. Not found'}, 404


@app.route("/")
def api_working():
    return "welcome to the recordX api"


if __name__ == "__main__":
    app.run(host='localhost', port=3500, debug=True)
