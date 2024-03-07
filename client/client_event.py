import db_conn
import jsonify


def create_event():
    return jsonify({"message":"Created"}),201