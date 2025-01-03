from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return jsonify(data)
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404
    pass

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture with that id is not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    # Check if the JSON data is empty or None
    if not new_picture:
        return {"Message": "Invalid input parameter"}, 422

    # Check if 'id' exists in the incoming picture data
    if 'id' not in new_picture:
        return {"Message": "Missing 'id' in input data"}, 422

    # Check if a picture with the same 'id' already exists
    for picture in data:  # Assuming 'data' is a predefined list of pictures
        if picture['id'] == new_picture['id']:
            return {"Message": f"picture with id {new_picture['id']} already present"}, 302

    # Add the new picture to the data list
    try:
        data.append(new_picture)
    except NameError:
        return {"Message": "data not defined"}, 500

    # Return a success message with the 'id' and a 201 Created status code
    return {"id": new_picture['id']}, 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.json

    # Check if the JSON data is empty or None
    if not updated_picture:
        return {"Message": "Invalid input parameter"}, 422

    # Find the picture by id in the data list
    for picture in data:
        if picture['id'] == id:
            # Update the picture's fields with the incoming data
            picture.update(updated_picture)
            return {"Message": f"picture with id {id} is updated"}, 200

    # If no picture is found, return 404 Not Found
    return {"Message": "picture not found"}, 404



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Iterate through the data list to find the picture
    for picture in data:
        if picture['id'] == id:
            # Remove the picture from the data list
            data.remove(picture)
            # Return a 204 No Content response
            return {}, 204

    # If no picture is found, return 404 Not Found
    return {"message": "picture not found"}, 404
