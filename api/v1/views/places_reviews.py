#!/usr/bin/python3
""" API routes for reviews including every HTTP method """

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=["GET"])
def reviews(place_id):
    """retrieves list of all review objects of a place"""
    home_place = storage.get(Place, place_id)
    if home_place is None:
        abort(404)
    reviews_dict = storage.all(Review)
    reviews_list = []
    for obj in reviews_dict.values:
        if obj.place_id == place.id:
            reviews_list.append(obj.to_dict())
    return(jsonify(reviews_list))


@app_views.route('/reviews/<review_id>', methods=["GET"])
def reviews_id(review_id):
    """retrieves a review object"""
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"])
def review_delete(review_id):
    """deletes a review object"""
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"])
def review_post(place_id):
    """creates a review object"""
    home_place = storage.get(Place, place_id)
    if home_place is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)
    if "text" not in request_data.keys():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    request_data["place_id"] = place_id
    review_obj = Review(**request_data)
    storage.new(review_obj)
    storage.save()
    review_dict = review_obj.to_dict()
    return jsonify(review_dict), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def review_put(review_id):
    """updates a review object"""
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        blacklist = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in blacklist:
            setattr(res, key, value)
    res.save()
    res_dict = res.to_dict()
    return jsonify(res_dict), 200
