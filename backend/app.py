from pymongo import MongoClient
from flask import Flask, redirect, url_for, request, session
from flask_cors import CORS, cross_origin
import json
from bson import ObjectId
from typing import Any
import bcrypt
from dotenv import load_dotenv
import os
import jwt
import datetime

from db.mongodb import get_record_collection, get_user_collection
from modules.records import get_all_records, get_single_record, create_record, update_record, delete_record
from modules.users import get_all_users, get_single_user, update_user, register_user, login_user, delete_user

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('JWT_SECRET')
JWT_SECRET = os.getenv("JWT_SECRET")

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

user_col = get_user_collection()
record_col = get_record_collection()


@app.route('/api/health')
def health():
    return {"success": True, "message": "The server is up and running. It is healthy."}


@app.route('/api/records', methods=['GET', 'POST'])
def records_route():
    if request.method == 'GET':
        records = get_all_records()
        return {"success": True, "data": records}
    if request.method == 'POST':
        data = request.get_json()
        new_record = create_record(data)
        return {"success": True, "data": new_record}


@app.route('/api/records/<record_id>', methods=['GET', 'PATCH', 'DELETE'])
def album_route(record_id):
    if request.method == 'GET':
        album = get_single_record(record_id)
        return {"success": True, "data": album}
    if request.method == 'PATCH':
        data = request.get_json()
        try:
            updated = update_record(record_id, data)
            if updated.modified_count > 0:
                return {"success": True, "message": "Record successfully updated"}
            else:
                return {"success": False, "message": "Unable to update record"}, 404
        except:
            return {"success": False, "message": "Invalid record id"}, 500
    if request.method == 'DELETE':
        try:
            print("DELETE RECORD CALLED")
            deleted = delete_record(record_id)
            print(f"Deleted: {deleted.deleted_count}")
            if deleted.deleted_count > 0:
                return {"success": True, "message": "Record successfully deleted"}
            else:
                return {"success": False, "message": "Unable to delete record"}, 404
        except:
            return {"success": False, "message": "Invalid record id"}, 500


@app.route("/api/users", methods=["GET", "POST"])
def users_route():
    if request.method == 'GET':
        users = get_all_users()
        return {"success": True, "data": users}


@app.route('/api/users/<user_id>', methods=['GET', 'PATCH', 'DELETE'])
def single_user_route(user_id):
    if request.method == 'GET':
        user = get_single_user(user_id)
        return {"success": True, "data": user}
    if request.method == 'PATCH':
        data = request.get_json()
        try:
            updated = update_user(user_id, data)
            if updated.modified_count > 0:
                return {"success": True, "message": "User successfully updated"}
            else:
                return {"success": False, "message": "Unable to update user"}, 404
        except:
            return {"success": False, "message": "Invalid user id"}, 500
    if request.method == 'DELETE':
        try:
            print("DELETE USER CALLED")
            deleted = delete_user(user_id)
            print(f"Deleted: {deleted.deleted_count}")
            if deleted.deleted_count > 0:
                return {"success": True, "message": "User successfully deleted"}
            else:
                return {"success": False, "message": "Unable to delete user"}, 404
        except:
            return {"success": False, "message": "Invalid user id"}, 500


@app.route("/api/users/register", methods=['POST'])
def register():
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    user_found = user_col.find_one({"username": username})
    email_found = user_col.find_one({"email": email})
    try:
        if email_found or user_found:
            message = 'This user already exists in database'
            return {"success": False, "message": message}
        else:
            new_user = register_user(username, email, password)
            new_email = new_user["email"]
            token = jwt.encode(
                {"email": email, "username": username}, JWT_SECRET, algorithm="HS256")
            return {"success": True, "message": f"New User created with email: {new_email}", "token": token}
    except:
        return {"success": False, "message": "Invalid input. Unable to register user"}, 500


@app.errorhandler(404)
def handle_404(e):
    return {'success': False, 'message': 'Error. Not found'}, 404


@app.route("/")
def api_working():
    return "welcome to the recordX api"


if __name__ == "__main__":
    app.run(host='localhost', port=3500, debug=True)
