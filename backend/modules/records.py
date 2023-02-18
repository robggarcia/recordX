from db.mongodb import get_record_collection, MongoJSONEncoder
from bson import ObjectId, json_util
import json


def create_object(data):
    data_json = MongoJSONEncoder().encode(list(data))
    data_obj = json.loads(data_json)
    return data_obj


def get_all_records():
    record_col = get_record_collection()
    data = record_col.find().sort("artist")
    records = create_object(data)
    return records


def get_single_record(record_id):
    record_col = get_record_collection()
    data = record_col.find_one({"_id": ObjectId(record_id)})
    album = json.loads(json_util.dumps(data))
    return album


def update_record(id, data):
    record_col = get_record_collection()
