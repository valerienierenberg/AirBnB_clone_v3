#!/usr/bin/python3
""" API routes for amenities including every HTTP method """

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=["GET"])
def amenities():
    """retrieves list of all amenity objects"""
    amenities_dict = storage.all(Amenity)
    amenities_list = []
    for value in amenities_dict.values():
        amenities_list.append(value.to_dict())
    return(jsonify(amenities_list))


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
def amenities_id(amenity_id):
    """retrieves a amenity object"""
    res = storage.get(Amenity, amenity_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def amenity_delete(amenity_id):
    """deletes a amenity object"""
    res = storage.get(Amenity, amenity_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"])
def amenity_post():
    """creates a amenity object"""
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenityobj = Amenity(**request_data)
    storage.new(amenityobj)
    storage.save()
    amenitydict = amenityobj.to_dict()
    return jsonify(amenitydict), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def amenity_put(amenity_id):
    """updates a amenity object"""
    res = storage.get(Amenity, amenity_id)
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
