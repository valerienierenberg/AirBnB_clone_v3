#!/usr/bin/python3
""" API routes for users including every HTTP method """

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=["GET"])
def users():
    """retrieves list of all user objects"""
    users_dict = storage.all(User)
    users_list = []
    for value in users_dict.values():
        users_list.append(value.to_dict())
    return(jsonify(users_list))


@app_views.route('/users/<user_id>', methods=["GET"])
def users_id(user_id):
    """retrieves a user object"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"])
def user_delete(user_id):
    """deletes a user object"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"])
def user_post():
    """creates a user object"""
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    userobj = User(**request_data)
    storage.new(userobj)
    storage.save()
    userdict = userobj.to_dict()
    return jsonify(userdict), 201


@app_views.route('/users/<user_id>', methods=["PUT"])
def user_put(user_id):
    """updates a user object"""
    res = storage.get(User, user_id)
    if res is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        blacklist = ["id", "created_at", "updated_at"]
        if key not in blacklist:
            setattr(res, key, value)
    res.save()
    resdict = res.to_dict()
    return jsonify(resdict), 200
