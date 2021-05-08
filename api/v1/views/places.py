#!/usr/bin/python3
""" API routes for places including every HTTP method """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/citys/<city_id>/places', methods=["GET"])
def places(city_id):
    """retrieves list of all place objects of a city"""
    home_city = storage.get(City, city_id)
    if home_city is None:
        abort(404)
    places_dict = storage.all(Place)
    places_list = []
    for obj in places_dict.values:
        if obj.city_id == city.id:
            places_list.append(obj.to_dict())
    return(jsonify(places_list))


@app_views.route('/places/<place_id>', methods=["GET"])
def places_id(place_id):
    """retrieves a place object"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"])
def place_delete(place_id):
    """deletes a place object"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route('/citys/<city_id>/places', methods=["POST"])
def place_post(city_id):
    """creates a place object"""
    home_city = storage.get(City, city_id)
    if home_city is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)
    if "name" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    request_data["city_id"] = city_id
    place_obj = Place(**request_data)
    storage.new(place_obj)
    storage.save()
    place_dict = place_obj.to_dict()
    return jsonify(place_dict), 201


@app_views.route('/places/<place_id>', methods=["PUT"])
def place_put(place_id):
    """updates a place object"""
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        blacklist = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in blacklist:
            setattr(res, key, value)
    res.save()
    res_dict = res.to_dict()
    return jsonify(res_dict), 200
