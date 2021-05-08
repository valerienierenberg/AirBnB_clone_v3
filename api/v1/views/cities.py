#!/usr/bin/python3
""" API routes for cities including every HTTP method """

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=["GET"])
def cities(state_id):
    """retrieves list of all city objects of a state"""
    home_state = storage.get(State, state_id)
    if home_state is None:
        abort(404)
    cities_obj_list = home_state.cities
    cities_list = []
    for obj in cities_obj_list:
        cities_list.append(obj.to_dict())
    return(jsonify(cities_list))


@app_views.route('/cities/<city_id>', methods=["GET"])
def cities_id(city_id):
    """retrieves a city object"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def city_delete(city_id):
    """deletes a city object"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"])
def city_post(state_id):
    """creates a city object"""
    home_state = storage.get(State, state_id)
    if home_state is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    request_data["state_id"] = state_id
    city_obj = City(**request_data)
    storage.new(city_obj)
    storage.save()
    city_dict = city_obj.to_dict()
    return jsonify(city_dict), 201


@app_views.route('/cities/<city_id>', methods=["PUT"])
def city_put(city_id):
    """updates a city object"""
    res = storage.get(City, city_id)
    if res is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        blacklist = ["id", "state_id", "created_at", "updated_at"]
        if key not in blacklist:
            setattr(res, key, value)
    res.save()
    res_dict = res.to_dict()
    return jsonify(res_dict), 200
