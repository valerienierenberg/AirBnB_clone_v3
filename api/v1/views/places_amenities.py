#!/usr/bin/python3
""" view for link between Place and Amenity objects that
handles all default Restful API actions """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
import os


@app_views.route('/places/<place_id>/amenities', methods=["GET"])
def places_amenities(place_id):
    """retrieves the list of all Amenity objects of a Place"""
    home_place = storage.get(Place, place_id)
    if home_place is None:
        abort(404)
    amenities_obj_list = home_place.amenities
    amenities_list = []
    for obj in amenities_obj_list:
        amenities_list.append(obj.to_dict())
    return(jsonify(amenities_list))


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE"])
def places_amenity_del(place_id, amenity_id):
    """deletes an Amenity object to a Place"""
    home_place = storage.get(Place, place_id)
    res_amenity = storage.get(Amenity, amenity_id)
    if (res_amenity is None or home_place is None or res_amenity not in
            amenities_obj_list):
        abort(404)
    amenities_obj_list = home_place.amenities
    for amenity_obj in home_place.amenities:
        if amenity_obj.id == amenity_id:
            home_place.amenities.remove(amenity_obj)
            storage.save()
            return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=["POST"])
def places_amenity_post(place_id, amenity_id):
    """links an Amenity object to a Place"""
    home_place = storage.get(Place, place_id)
    res_amenity = storage.get(Amenity, amenity_id)
    if (res_amenity is None or home_place is None):
        abort(404)
    amenities_obj_list = home_place.amenities
    for amenity_obj in home_place.amenities:
        if amenity_obj.id == amenity_id:
            return jsonify(res_amenity.to_dict()), 200
    home_place.amenities.append(res_amenity)
    storage.save()
    return jsonify(res_amenity.to_dict()), 201
