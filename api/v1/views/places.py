#!/usr/bin/python3
""" API routes for places including every HTTP method """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=["GET"])
def places(city_id):
    """retrieves list of all place objects of a city"""
    home_city = storage.get(City, city_id)
    if home_city is None:
        abort(404)
    places_dict = storage.all(Place)
    places_list = []
    for obj in places_dict.values():
        if obj.city_id == city_id:
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


@app_views.route('/cities/<city_id>/places', methods=["POST"])
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


@app_views.route('/places_search', methods=["POST"])
def place_post_search():
    """retrieves all Place objects depending on JSON in body of the request"""
    request_data = request.get_json()
    places_dict = storage.all(Place)
    places_list = []
    for value in places_dict.values():
        places_list.append(value.to_dict())
    cities_dict = storage.all(City)
    cities_list = []
    for value in cities_dict.values():
        cities_list.append(value.to_dict())
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    # if no search criteria given, return all places:
    if request_data == {} or ((request_data["states"] is None or
                               request_data["states"] == []) and
                              (request_data["cities"] is None or
                               request_data["cities"] == []) and
                              (request_data["amenities"] is None or
                               request_data["amenities"] == [])):
        return(jsonify(places_list))
    places_res_list = []
    if type(request_data["states"]) is list:
        for id in request_data["states"]:
            for city in cities_list:
                if city["state_id"] == id:
                    for place in places_list:
                        places_res_list.append(place)
        # list now has every place in every city in the states passed in
    if type(request_data["cities"]) is list:
        for city in cities_list:
            if city["state_id"] not in request_data["states"]:
                for place in places_list:
                    places_res_list.append(place)
        # added places from cities passed if they aren't in the states passed
    # if the place doesn't have *all* amenities passed in, remove from results
    if ("amenities" in request_data.keys() and
            type(request_data["amenities"]) is list and
            len(request_data["amenities"]) != 0):
        search = set(request["amenities"])
        for place in places_res_list:
            present = set(place.amenities)
            if not search.issubset(present):  # if not a subset,
                places_res_list.remove(place)  # remove place from our list
    return(jsonify(places_res_list))
