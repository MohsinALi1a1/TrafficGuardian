import io
import os
import threading
from pydoc import locate
import socket

from PIL import Image
from datetime import datetime
from waitress import serve
import Model.Configure


import Controller
from Model.Configure import app
from flask import  request ,jsonify, send_from_directory
from Controller import LocationController, ChallanController, ImageControllerAndNotification, NakaGraphController, \
    StolenBikeController
from Controller import CameraChowkiController
from Controller import WardenChowkiController
from Controller import YoloController



########################################  City  ############################################


@app.route('/city', methods=['GET'])
def get_all_cities():
    try:
        city_list = LocationController.get_all_City()
        print(city_list)
        return jsonify(city_list),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/citybyid', methods=['GET'])
def get_city_by_id():
    try:
        data = request.get_json()
        city_id = data.get('id')
        print(city_id)
        if not city_id:
            return jsonify({"error": "City id is required"}), 400
        city = LocationController.get_city_by_id(city_id)
        return jsonify(city),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/citybyname', methods=['GET'])
def get_city_by_name():
    try:
        data = request.get_json()
        city_name = data.get('name')

        if not city_name:
            return jsonify({"error": "City name is required"}), 400
        city_name = city_name.title()
        city = LocationController.get_city_by_name(city_name)
        return jsonify(city),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addcity', methods=['POST'])
def add_city():
    try:
        data = request.get_json()
        city_name = data.get('name')

        if not city_name:
            return jsonify({"error": "City name is required"}), 400
        city_name = city_name.title()

        # Add the new city
        city=LocationController.add_city(city_name)
        if 'error' in city:
            return jsonify(city), 401
        else :
            return jsonify(city) , 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletecity', methods=['DELETE'])
def delete_city_by_name():
    try:
        data = request.get_json()
        city_name = data.get('name')
        if not city_name:
            return jsonify({"error": "City name is required"}), 400
        city_name = city_name.title()

        # Delete the city and get the success message
        message ,code = LocationController.delete_city(city_name)
        return jsonify(message) , code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletecitybyname', methods=['DELETE'])
def delete_city_by_n():
    try:
        city_name = request.args.get('name')
        if not city_name:
            return jsonify({"error": "City Name is required as query parameter"}), 400

        # Delete the city and get the success message
        message, code = LocationController.delete_city(city_name)
        return jsonify(message), code

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Route to update a city
@app.route('/updatecity', methods=['PUT'])
def update_city():
    try:
        data = request.get_json()
        city_name = data.get('name')
        new_name = data.get('new_name')

        if not city_name or not new_name:
            return jsonify({"error": "Both current city name and new name are required"}), 400
        city_name = city_name.title()
        new_name = new_name.title()

        message ,code=LocationController.update_city(city_name, new_name)
        return jsonify(message) ,code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


########################################  PLACE  ############################################


@app.route('/place', methods=['GET'])
def get_all_places():
    try:
        city_name = request.args.get('name')  # Use query parameter
        if not city_name:
            return jsonify({"error": "City name is required"}), 400
        city_name = city_name.title()
        place_list = LocationController.get_all_Places(city_name)


        if not place_list:
            return jsonify({"error": "No places found for the specified city"}), 404

        return jsonify(place_list), 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/placebyid', methods=['GET'])
def get_place_by_id():
    try:
        data = request.get_json()
        place_id = data.get('id')
        print(place_id)
        if not place_id:
            return jsonify({"error": "Place id is required"}), 400
        place = LocationController.get_place_by_id(place_id)
        return jsonify(place),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/placebyname', methods=['GET'])
def get_place_by_name():
    try:
        place_name = request.args.get('name')
        if not place_name:
            return jsonify({"error": "Place name is required"}), 400
        place_name = place_name.title()
        place = LocationController.get_place_by_name(place_name)
        return jsonify(place),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addplace', methods=['POST'])
def add_place():
    try:
        data = request.get_json()
        city_name = data.get('cityname')
        place_name=data.get('placename')

        if not city_name or not place_name:
            return jsonify({"error": "Both City & Place name is required"}), 400
        city_name = city_name.title()
        place_name = place_name.title()
        # Add the new Place
        place=LocationController.add_place(city_name,place_name)
        if 'error' in place:
            return jsonify(place), 401
        return jsonify(place), 200
    except Exception as exp:
        print(exp)
        return jsonify({'error': str(exp)}), 500



@app.route('/deleteplace', methods=['DELETE'])
def delete_place_by_name():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        city_name = data.get('cityname')
        if not place_name or not city_name:
            return jsonify({"error": "Place name & City Name  is required"}), 400
        city_name = city_name.title()
        place_name = place_name.title()
        # Delete the Place and get the success message
        message ,code= LocationController.delete_place(city_name,place_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/deleteplacebyget', methods=['DELETE'])
def delete_place_by_name_by_get():
    try:
        place_name = request.args.get('placename')
        city_name = request.args.get('cityname')

        if not place_name or not city_name:
            return jsonify({"error": "Place name & City name are required"}), 400

        city_name = city_name.title()
        place_name = place_name.title()

        # Call the delete function
        message, code = LocationController.delete_place(city_name, place_name)
        return jsonify(message), code

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# Route to update a Place name
@app.route('/updateplace', methods=['PUT'])
def update_place():
    try:
        data = request.get_json()
        city_name = data.get('city_name')
        place_name = data.get('place_name')
        new_name = data.get('new_name')

        if not place_name or not new_name or not city_name:
            return jsonify({"error": "Cityname and Both current Place name and new name are required"}), 400
        city_name = city_name.title()
        place_name = place_name.title()
        new_name=new_name.title()
        message,code=LocationController.update_place(city_name,place_name, new_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


########################################  Directions  ############################################

@app.route('/directions', methods=['GET'])
def get_all_directions():
    try:

        place_name =  request.args.get('name')
        print(place_name)
        if not place_name:
            return jsonify({"error": "Place name is required"}), 400
        place_name = place_name.title()
        directions = LocationController.get_all_Directions(place_name)
        if not directions:
            return jsonify({"error": "No Direction found for the specified Place"}), 404
        return jsonify(directions),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/directionbyid', methods=['GET'])
def get_direction_by_id():
    try:
        data = request.get_json()
        direction_id = data.get('id')
        print(direction_id)
        if not direction_id:
            return jsonify({"error": "Direction id is required"}), 400
        directions = LocationController.get_direction_by_id(direction_id)
        return jsonify(directions),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/directionbyname', methods=['GET'])
def get_direction_by_name():
    try:
        direction_name = request.args.get('name')
        if not direction_name:
            return jsonify({"error": "Direction name is required"}), 400
        direction_name = direction_name.title()
        direction = LocationController.get_direction_by_name(direction_name)
        return jsonify(direction),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/adddirection', methods=['POST'])
def add_direction():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        direction_name = data.get('directionname')


        if not place_name or not direction_name:
            return jsonify({"error": "Both  Place & Direction name is required"}), 400
        direction_name=direction_name.title()
        place_name=place_name.title()
        # Add the new Direction
        direction=LocationController.add_direction(place_name,direction_name)
        if 'error' in direction:
            return jsonify(direction), 401

        return jsonify(direction), 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletedirection', methods=['DELETE'])
def delete_direction_by_name():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        direction_name = data.get('directionname')
        if not place_name or not direction_name:
            return jsonify({"error": "Place name & Direction name is required"}), 400
        direction_name = direction_name.title()
        place_name = place_name.title()
        # Delete the Place and get the success message
        message,code = LocationController.delete_direction(place_name,direction_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletedirectionget', methods=['DELETE'])
def delete_direction_by_namebyget():
    try:
        place_name = request.args.get('placename')
        direction_name = request.args.get('directionname')
        if not place_name or not direction_name:
            return jsonify({"error": "Place name & Direction name is required"}), 400
        direction_name = direction_name.title()
        place_name = place_name.title()
        # Delete the Place and get the success message
        message,code = LocationController.delete_direction(place_name,direction_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



# Route to update a Direction
@app.route('/updatedirection', methods=['PUT'])
def update_direction():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        direction_name=data.get('directionname')
        new_name = data.get('newname')

        if not place_name or not new_name or not direction_name:
            return jsonify({"error": "Place ,Direction name  and new Direction name are required"}), 400
        direction_name = direction_name.title()
        place_name = place_name.title()
        new_name=new_name.title()
        message,code=LocationController.update_direction(place_name,direction_name,new_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Camera  ############################################
@app.route('/camera', methods=['POST'])
def get_all_camera():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        direction_name = data.get('directionname')

        print(place_name , direction_name)
        if not place_name or not  direction_name:
            return jsonify({"error": "Place name & direction name is required"}), 400
        place_name = place_name.title()
        direction_name = direction_name.title()
        cameras= CameraChowkiController.get_all_camera(place_name, direction_name)
        if not cameras:
            return jsonify({"error": f"No camera found for the specified Place {place_name} on Direction {direction_name}"}), 404
        return jsonify(cameras),200
    except Exception as exp:

        return jsonify({'error': str(exp)}), 500


@app.route('/camerabyid', methods=['GET'])
def get_camera_by_id():
    try:
        data = request.get_json()
        camera_id = data.get('id')
        print(camera_id)
        if not camera_id:
            return jsonify({"error": "Camera id is required"}), 400
        camera = CameraChowkiController.get_camera_by_id(camera_id)
        return jsonify(camera)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/camerabyname', methods=['GET'])
def get_camera_by_name():
    try:
        camera_name = request.args.get('name')
        if not camera_name:
            return jsonify({"error": "Camera name is required"}), 400
        camera_name=camera_name.title()
        camera =CameraChowkiController.get_camera_by_name(camera_name)
        return jsonify(camera)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addcamera', methods=['POST'])
def add_camera():
    try:
        data = request.get_json()
        name = data.get('name')
        direction_name = data.get('directionname')
        cam_type=data.get('type')


        if not name or not direction_name or not cam_type:
            return jsonify({"error": " Camera,Direction name & Camera Type  is required"}), 400
        name=name.title()
        direction_name=direction_name.title()
        # Add the new Direction
        camera = CameraChowkiController.add_camera(name,direction_name,cam_type)
        return jsonify(camera), 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletecamera', methods=['DELETE'])
def delete_camera_by_name():
    try:
        data = request.get_json()
        camera_name = data.get('name')
        direction_name = data.get('directionname')
        camera_type=data.get('cameratype')
        if not camera_name or not direction_name or not camera_type:
            return jsonify({"error": "Direction name ,Camera name and Type  is required"}), 400
        camera_name = camera_name.title()
        direction_name = direction_name.title()
        # Delete the Camera and get the success message
        message = CameraChowkiController.delete_camera(camera_name,direction_name,camera_type)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/deletecamerabyget', methods=['DELETE'])
def delete_camera_by_name_byget():
    try:
        camera_name = request.args.get('name')
        direction_name = request.args.get('directionname')
        camera_type = request.args.get('cameratype')
        print(camera_name ,direction_name ,camera_type)

        if not camera_name or not direction_name or not camera_type:
            return jsonify({"error": "Direction name, Camera name, and Type are required"}), 400

        camera_name = camera_name.title()
        direction_name = direction_name.title()

        # Delete the Camera and get the success message
        message ,code= CameraChowkiController.delete_camera(camera_name, direction_name, camera_type)
        return jsonify(message),code

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Chowki  ############################################

@app.route('/chowki', methods=['POST'])
def get_all_chowki():
    try:
        data = request.get_json()
        place_name = data.get('placename')

        print(place_name )
        if not place_name :
            return jsonify({"error": "Place name  is required"}), 400
        place_name.title()
        chowki= CameraChowkiController.get_all_Chowki(place_name)
        if not chowki:
            return jsonify({"error": f"No Chowki found for the specified Place {place_name}"}), 404
        return jsonify(chowki)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/chowkiincity', methods=['POST'])
def get_all_chowki_incity():
    try:
        data = request.get_json()
        city_name = data.get('cityname')

        print(city_name )
        if not city_name :
            return jsonify({"error": "city name  is required"}), 400
        city_name.title()
        chowki= CameraChowkiController.get_all_Chowki_bycity(city_name)
        if not chowki:
            return jsonify({"error": f"No Chowki found for the specified Place {city_name}"}), 404
        return jsonify(chowki)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500
@app.route('/chowkibyid', methods=['GET'])
def get_chowki_by_id():
    try:
        data = request.get_json()
        chowki_id = data.get('id')
        print(chowki_id)
        if not chowki_id:
            return jsonify({"error": "Chowki id is required"}), 400
        chowki = CameraChowkiController.get_chowki_by_id(chowki_id)
        return jsonify(chowki)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/chowkibyname', methods=['GET'])
def get_chowki_by_name():
    try:
        data = request.get_json()
        chowki_name = data.get('name')
        if not chowki_name:
            return jsonify({"error": "Chowki name is required"}), 400
        chowki_name=chowki_name.title()
        chowki =CameraChowkiController.get_chowki_by_name(chowki_name)
        return jsonify(chowki)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/addchowki', methods=['POST'])
def add_chowki():
    try:
        data = request.get_json()
        name = data.get('name')
        place_name = data.get('placename')

        if not name or not place_name:
            return jsonify({"error": " Chowki Name,Place name is required"}), 400
        name=name.title()
        place_name=place_name.title()
        # Add the new Chowki
        chowki = CameraChowkiController.add_chowki(name,place_name)
        return jsonify(chowki), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletechowki', methods=['DELETE'])
def delete_chowki_by_name():
    try:
        data = request.get_json()
        name = data.get('name')
        place_name = data.get('placename')

        if not name or not place_name:
            return jsonify({"error": " Chowki name,Place name is required"}), 400
        name=name.title()
        place_name=place_name.title()
        # Delete the Chowki and get the success message
        message = CameraChowkiController.delete_chowki(name,place_name)
        return jsonify(message),201
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500

########################################  CameraChowki  ############################################


@app.route('/chowkicamera', methods=['GET'])
def get_all_chowkicamera_bycity():
    try:
        data = request.get_json()
        city_name = data.get('cityname')

        print(city_name )
        if not city_name :
            return jsonify({"error": "city name  is required"}), 400
        city_name.title()
        chowki_info = CameraChowkiController.get_all_ChowkiCamera_bycity(city_name)

        if not chowki_info:
            return jsonify({"error": f" Camera_Chowki not found for the specified City {city_name}"}), 404

        return jsonify(chowki_info)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500




@app.route('/chowkicameraplace', methods=['GET'])
def get_all_chowkicamera_byplace():
    try:
        data = request.get_json()
        place_name = data.get('placename')

        print(place_name )
        if not place_name :
            return jsonify({"error": "city name  is required"}), 400
        place_name=place_name.title()
        chowki_info = CameraChowkiController.get_all_ChowkiCamera_byplace(place_name)

        if not chowki_info:
            return jsonify({"error": f" Camera_Chowki not found for the specified Place {place_name}"}), 404

        return jsonify(chowki_info)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/linkcamerawithchowki', methods=['POST'])
def get_all_camera_with_chowki():
    try:
        data = request.get_json()
        chowki_name = data.get('chowkiname')

        print(chowki_name )
        if not chowki_name :
            return jsonify({"error": "Chowki name  is required"}), 400
        chowki_name=chowki_name.title()
        chowki_info = CameraChowkiController.get_all_linkCamera_with_Chowki(chowki_name)

        if not chowki_info:
            return jsonify({"error": f" No Camera is linked for the specified Chowki {chowki_name}"}), 404

        return jsonify(chowki_info),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/linkcamerawithchowkibyid', methods=['POST'])
def get_all_camera_with_chowkibyid():
    try:
        data = request.get_json()
        chowki_id = data.get('chowki_id')

        print(chowki_id )
        if not chowki_id :
            return jsonify({"error": "Chowki id  is required"}), 400

        chowki_info = CameraChowkiController.get_all_linkCamera_with_Chowkibyid(chowki_id)

        if not chowki_info:
            return jsonify({"error": f" No Camera is linked for the specified Chowki {chowki_id}"}), 404

        return jsonify(chowki_info),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/linkchowkiwithcamera', methods=['GET'])
def get_all_chowki_with_camera():
    try:
        data = request.get_json()
        camera_name = data.get('cameraname')

        print(camera_name )
        if not camera_name :
            return jsonify({"error": "Camera name  is required"}), 400
        camera_name=camera_name.title()
        chowki_info = CameraChowkiController.get_all_linkChowki_with_Camera(camera_name)

        if not chowki_info:
            return jsonify({"error": f" Camera is linked for the specified Chowki {camera_name}"}), 404

        return jsonify(chowki_info)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/linkcamerachowki', methods=['POST'])
def add_camerachowki():
    try:
        data = request.get_json()
        camera_list = data.get('cameraname')
        chowki_name = data.get('chowkiname')

        if not camera_list or not chowki_name:
            return jsonify({"error": " Chowki Name,camera name is required"}), 400

        chowki = CameraChowkiController.link_camera_to_chowki(chowki_name, camera_list)
        return jsonify(chowki), 201
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500



@app.route('/unlinkcamerachowki', methods=['DELETE'])
def delete_camerachowki():
    try:
        data = request.get_json()
        camera_list = data.get('cameraname')
        chowki_name = data.get('chowkiname')

        if not camera_list or not chowki_name:
            return jsonify({"error": " Chowki name,camera name is required"}), 400

        chowki = CameraChowkiController.unlink_camera_from_chowki(chowki_name, camera_list)
        return jsonify(chowki), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/updatecamerachowki', methods=['PUT'])
def update_camerachowki():
    try:
        data = request.get_json()

        unlink_camera_list = data.get('unlinkcameraname')
        link_camera_list = data.get('linkcameraname')
        chowki_name = data.get('chowkiname')


        if not chowki_name or (not unlink_camera_list and not link_camera_list):
            return jsonify({"error": "Chowki name, and at least one camera name (to link or unlink) are required"}), 400

        # Call the controller method to update linked cameras
        result = CameraChowkiController.update_linked_cameras_with_chowki(
            chowki_name,
            link_camera_list or [],  # Default to empty list if no cameras to link
            unlink_camera_list or []  # Default to empty list if no cameras to unlink
        )

        return jsonify({"message": result}), 200  # Return the result with a 200 status code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Shift  ############################################

@app.route('/shift', methods=['GET'])
def get_all_shift():
    try:
        shift_list = WardenChowkiController.get_all_Shift()
        print(shift_list)
        return jsonify(shift_list)
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500


@app.route('/shiftbyid', methods=['GET'])
def get_shift_by_id():
    try:
        data = request.get_json()
        shift_id = data.get('id')
        print(shift_id)
        if not shift_id:
            return jsonify({"error": "Shift id is required"}), 400
        shift=WardenChowkiController.get_shift_by_id(shift_id)
        return jsonify(shift)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/shiftbyname', methods=['GET'])
def get_shift_by_name():
    try:
        data = request.get_json()
        shift_name = data.get('shiftname')
        shift = WardenChowkiController.get_shift_by_name(shift_name)
        return jsonify(shift)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/addshift', methods=['POST'])
def add_shift():
    try:
        data = request.get_json()
        shift_name = data.get('shiftname')
        shift_starttime = data.get('starttime')
        shift_endtime = data.get('endtime')


        if not shift_name or not shift_starttime or not shift_endtime:
            return jsonify({"error": "Shift name, start time, and end time are required."}), 400

        shift_name=shift_name.title()
        # Convert string times to time objects
        shift_starttime = datetime.strptime(shift_starttime, "%H:%M:%S").time()
        shift_endtime = datetime.strptime(shift_endtime, "%H:%M:%S").time()

        # Add the new shift
        shift_response,code = WardenChowkiController.add_shift(shift_name, shift_starttime, shift_endtime)

        return jsonify(shift_response), code
    except ValueError as ve:
        return jsonify({'error': f'{ve}\nInvalid time format. Use HH:MM:SS. '}), 400
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deleteshift', methods=['DELETE'])
def delete_shift_by_name():
    try:
        data = request.get_json()
        shift_name = data.get('shiftname')
        shift_starttime = data.get('starttime')
        shift_endtime = data.get('endtime')

        if not shift_name or not shift_starttime or not shift_endtime:
            return jsonify({"error": "Shift name, start time, and end time are required."}), 400

        # Convert string times to time objects
        shift_starttime = datetime.strptime(shift_starttime, "%H:%M:%S").time()
        shift_endtime = datetime.strptime(shift_endtime, "%H:%M:%S").time()
        message = WardenChowkiController.delete_shift(shift_name)
        return jsonify(message),201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deleteshiftbyget', methods=['DELETE'])
def delete_shift_by_name_get():
    try:
        shift_name = request.args.get('shiftname')


        message,code = WardenChowkiController.delete_shift(shift_name)
        return jsonify(message), 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# Route to update a city
@app.route('/updateshift', methods=['PUT'])
def update_shifty():
    try:
        data = request.get_json()
        city_name = data.get('name')
        new_name = data.get('new_name')

        if not city_name or not new_name:
            return jsonify({"error": "Both current city name and new name are required"}), 400

        message=LocationController.update_city(city_name, new_name)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Traffic Warden  ############################################

@app.route('/trafficwarden', methods=['GET'])
def get_all_trafficwarden():
    try:
        warden_list = WardenChowkiController.get_all_warden()
        print(warden_list)
        return jsonify(warden_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/wardensincity', methods=['POST'])
def get_warden_in_city():
    try:
        data = request.get_json()
        city_name = data.get('cityname')
        if not city_name:
            return jsonify({"error": "City name is required"}), 400
        warden=WardenChowkiController.get_all_warden_city(city_name)
        if warden:
            return jsonify(warden)
        else:
            return ({"Invalid": f"No traffic Warden exist from the location {city_name}"}), 400
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500




@app.route('/wardentbycnic', methods=['GET'])
def get_warden_by_cnic():
    try:
        data = request.get_json()
        warden_cnic = data.get('cnic')
        warden = WardenChowkiController.get_warden_by_cnic(warden_cnic)
        return jsonify(warden)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/wardentbyid', methods=['POST'])
def get_warden_by_id():
    try:
        data = request.get_json()
        warden_id = data.get('id')
        warden,code = WardenChowkiController.get_warden_by_id(warden_id)
        return jsonify(warden),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/unassignwardenincity', methods=['POST'])
def get_unassignwarden():
    try:
        data = request.get_json()
        city_name = data.get('cityname')
        warden,code = WardenChowkiController.get_all_unassigned_wardens(city_name)
        return jsonify(warden),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addtrafficwarden', methods=['POST'])
def add_warden():
    try:
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        cnic = data.get('cnic')
        email = data.get('email')
        mobile_number = data.get('mobilenumber')
        city_name=data.get('cityname')

        if not name  or not address or not cnic or not email or not mobile_number or not city_name:
            return jsonify({"error": "Warden name , address, cnic , email, mobile_number, and city_name are required."}), 400
        name = name.title()
        address = address.title()
        email = email.title()
        city_name = city_name.title()
        # Add the new warden
        new_warden,code = WardenChowkiController.add_warden(name, address, cnic, email, mobile_number, city_name)
        return jsonify(new_warden), code
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500



@app.route('/deletewarden', methods=['DELETE'])
def delete_warden_route():
    try:
        data = request.get_json()
        cnic = data.get('cnic')

        if not cnic:
            return jsonify({"error": "CNIC  is required"}), 400

        return WardenChowkiController.delete_warden(cnic)
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500



@app.route('/deletewardenbyget', methods=['DELETE'])
def delete_warden_routebyget():
    try:
        cnic = request.args.get('cnic')

        if not cnic:
            return jsonify({"error": "CNIC is required"}), 400

        mesg,code= WardenChowkiController.delete_warden(cnic)
        return jsonify(mesg),code
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500


@app.route('/updatewarden', methods=['PUT'])
def update_warden_route():

    try:
        data = request.get_json()
        cnic = data.get('cnic')
        return WardenChowkiController.update_warden(
            cnic,
            name=data.get('name'),
            badge_number=data.get('badgenumber'),
            address=data.get('address'),
            email=data.get('email'),
            mobile_number=data.get('mobilenumber'),
            city_name=data.get('cityname')
        )
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/wardenlogin', methods=['POST'])
def wardenlogin():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 400

        data = request.get_json()
        badge = data.get('badge')
        password = data.get('password')
        print(badge)
        print(password)

        if not badge or not password:
            return jsonify({"error": "Badge Number and Password are required"}), 400

        response,code = WardenChowkiController.wardenlogincheck(badge, password)
        print(response)
        return jsonify(response), code

    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500

########################################  WardenChowki  ############################################

@app.route('/wardenassignments', methods=['POST'])
def warden_assignments():
    try:
        duty=WardenChowkiController.create_duty_roster()
        return jsonify({"sucessfully":duty}),201
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500



@app.route('/assignwarden', methods=['POST'])
def assign_warden():
    try:
        data = request.get_json()
        warden_id = data.get('wardenid')
        chowki_id = data.get('chowkiid')
        shift_id=data.get('shiftid')
        if not warden_id or not chowki_id or not shift_id:
            return jsonify({"error": "Warden_id, Chowki_id & Shift_id are required."}), 400

        # Add the new warden
        new_assignment = WardenChowkiController.assignwarden(warden_id, chowki_id, shift_id)
        return jsonify(new_assignment), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getassignjobs', methods=['GET'])
def get_all_dutyroster():
    try:

        dutyroster_list = WardenChowkiController.get_all_assignments_on_last_assign_date()
        print(dutyroster_list)
        return jsonify(dutyroster_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getassignjobofwarden', methods=['GET'])
def get_all_dutyroster_of_warden():
    try:
        data = request.get_json()
        badge_number = data.get('badge')
        dutyroster_list = WardenChowkiController.get_dutyroster_for_warden(badge_number)
        print(dutyroster_list)
        return jsonify(dutyroster_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getassignjobofwardenbyid', methods=['POST'])
def get_all_dutyroster_of_warden_byid():
    try:
        data = request.get_json()
        id = data.get('id')
        dutyroster_list = WardenChowkiController.get_dutyroster_for_warden_byid(id)
        print(dutyroster_list)
        return jsonify(dutyroster_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Vehicle  ############################################
@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    try:
        vehicle_list = ChallanController.get_all_vehicles()
        return jsonify(vehicle_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/vehiclebyid', methods=['POST'])
def get_vehicle_by_id():
    try:
        data = request.get_json()
        vehicle_id = data.get('id')
        if not vehicle_id:
            return jsonify({"error": "Vehicle id is required"}), 400
        vehicle = ChallanController.get_vehicle_by_id(vehicle_id)
        return jsonify(vehicle)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/vehiclebylicenseplate', methods=['GET'])
def get_vehicle_by_licenseplate():
    try:
        data = request.get_json()
        licenseplate = data.get('licenseplate')
        vehicle = ChallanController.get_vehicle_by_licenseplate(licenseplate)
        return jsonify(vehicle)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addvehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.get_json()
        licenseplate = data.get('licenseplate')
        vehicletype = data.get('vehicletype')

        if not licenseplate or not vehicletype:
            return jsonify({"error": "License plate and vehicle type are required"}), 400

        vehicle = ChallanController.add_vehicle(licenseplate, vehicletype)
        return jsonify(vehicle), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletevehicle', methods=['DELETE'])
def delete_vehicle_by_licenseplate():
    try:
        data = request.get_json()
        licenseplate = data.get('licenseplate')
        if not licenseplate:
            return jsonify({"error": "License plate is required"}), 400

        message = ChallanController.delete_vehicle(licenseplate)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/updatevehicle', methods=['PUT'])
def update_vehicle():
    try:
        data = request.get_json()
        licenseplate = data.get('licenseplate')
        new_licenseplate = data.get('new_licenseplate')


        if not licenseplate or not new_licenseplate :
            return jsonify({"error": "Current license plate and at least one new value are required"}), 400

        message = ChallanController.update_vehicle(licenseplate, new_licenseplate)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  User  ############################################


@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        user_list = ChallanController.get_all_users()
        return jsonify(user_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/userbyid', methods=['POST'])
def get_user_by_id():
    try:
        data = request.get_json()
        user_id = data.get('id')
        if not user_id:
            return jsonify({"error": "User id is required"}), 400
        user = ChallanController.get_user_by_id(user_id)
        return jsonify(user)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/userbycnic', methods=['GET'])
def get_user_by_cnic():
    try:
        data = request.get_json()
        cnic = data.get('cnic')
        user = ChallanController.get_user_by_cnic(cnic)
        return jsonify(user)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/adduser', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        cnic = data.get('cnic')
        mobilenumber = data.get('mobilenumber')
        email = data.get('email')
        password=data.get('password')

        if not name or not cnic or not mobilenumber or not password:
            return jsonify({"error": "Name, CNIC, and mobile number and password are required"}), 400

        user = ChallanController.add_user(name, cnic, mobilenumber, email,password)
        return jsonify(user), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deleteuser', methods=['DELETE'])
def delete_user_by_cnic():
    try:
        data = request.get_json()
        cnic = data.get('cnic')
        if not cnic:
            return jsonify({"error": "CNIC is required"}), 400

        message = ChallanController.delete_user(cnic)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/updateuser', methods=['PUT'])
def update_user():
    try:
        data = request.get_json()
        cnic = data.get('cnic')
        new_name = data.get('new_name')
        new_mobilenumber = data.get('new_mobilenumber')
        new_email = data.get('new_email')

        if not cnic:
            return jsonify({"error": "CNIC is required"}), 400

        message = ChallanController.update_user(cnic, new_name, new_mobilenumber, new_email)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/Userlogin', methods=['POST'])
def userlogin():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 400

        data = request.get_json()
        cnic = data.get('Cnic')
        password = data.get('password')
        print(cnic)
        print(password)

        if not cnic or not password:
            return jsonify({"error": "Badge Number and Password are required"}), 400

        response, code = ChallanController.userlogincheck(cnic, password)
        print(response)
        return jsonify(response), code

    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500

    ########################################  Violations  ############################################
# Route to get all violations with fines
@app.route('/violations', methods=['GET'])
def get_all_violations():
    try:
        violations = ChallanController.get_all_violations()
        return jsonify(violations)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/violationsbyid', methods=['POST'])
def get_violation_by_id():
    try:
        data = request.get_json()
        violation_id = data.get('violation_id')

        if violation_id is None:
            return jsonify({"error": "violation_id is required"}), 400

        violation = ChallanController.get_violation_by_id(violation_id)
        return jsonify(violation)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# Route to add a new violation
@app.route('/violation', methods=['POST'])
def add_violation():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        limitValue=data.get('limitValue')
        fine=data.get('fine')

        if not name and not fine:
            return jsonify({"error": "Violation name and fine is required"}), 400

        result = ChallanController.add_violation(name, fine,description ,limitValue )
        return jsonify(result), 201
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500

# Route to delete a violation by ID
@app.route('/deleteviolation', methods=['DELETE'])
def delete_violation():
    try:
        data = request.get_json()
        violation_name = data.get('violation_name')
        result = ChallanController.delete_violation(violation_name)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Route to update a violation
@app.route('/updateviolation', methods=['PUT'])
def update_violation():
    try:
        data = request.get_json()
        violation_id=data.get('violation_id')
        new_name = data.get('new_name')
        new_description = data.get('new_description')
        limit_value=data.get('newlimitValue')
        fine=data.get('newfine')
        start_date =data.get('start_date')
        end_date = data.get('end_date')
        print(start_date)

        result,code = ChallanController.update_violation(violation_id, new_name, new_description ,limit_value,fine,start_date, end_date)
        return jsonify(result)
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500

@app.route('/updateviolationstatus', methods=['PUT'])
def update_violation_status():
    try:
        data = request.get_json()
        violation_id=data.get('violation_id')
        Status = data.get('Status')


        result,code = ChallanController.update_violations_status(violation_id,Status)
        return jsonify(result),code
    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500
########################################  ViolationsFine  ############################################
# Route to add a fine to a violation
@app.route('/violationfine', methods=['POST'])
def add_violation_fine():
    try:
        data = request.get_json()
        violation_id=data.get('violation_id')
        created_date = datetime.today().strftime('%Y-%m-%d')
        fine = data.get('fine')

        if  not fine  or not violation_id:
            return jsonify({"error": "Violation_id and fine amount are required"}), 400

        result = ChallanController.add_violation_fine(violation_id, created_date, fine)
        return jsonify(result), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Route to delete a fine
@app.route('/fine/<int:fine_id>', methods=['DELETE'])
def delete_violation_fine(fine_id):
    try:
        result = ChallanController.delete_violation_fine(fine_id)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  ViolationsHistory & Its Details ############################################
@app.route('/addviolationsrecord', methods=['POST'])
def create_violation():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id')
        date = data.get('date')
        location = data.get('location')
        status = data.get('status', 'Pending')  # Default to 'Pending'
        imagepath = data.get('imagepath')
        camera_id = data.get('camera_id')
        violation_ids = data.get('violation_ids')

        if not all([vehicle_id, date, location, camera_id, violation_ids]):
            return jsonify({"error": "Missing required fields"}), 400

        success = ChallanController.add_violation_history_and_details(vehicle_id, date, location, status, imagepath, camera_id, violation_ids)

        if success:
            return jsonify(success)

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getviolationsrecord_for_nakaid', methods=['POST'])
def get_violation_records():
    try:
        data = request.json
        chowki_id=data.get('chowki_id')
        vehicle_id = data.get('vehicle_id')
        date = data.get('date')
        camera_id = data.get('camera_id')
        warden_id=data.get('warden_id')
        if not chowki_id and not warden_id:
            return jsonify({"error":"Plz Pass Chowki ID or warden id"})
        result = ChallanController.get_violation_history_with_details(chowki_id,vehicle_id, date,warden_id)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/updateviolationsrecord', methods=['PUT'])
def update_violation_records():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id')
        date = data.get('date')
        camera_id = data.get('camera_id')
        updates = data.get('updates') #get dictionary

        result = ChallanController.update_violation_history(vehicle_id, date, camera_id, updates)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/deleteviolationsrecord', methods=['DELETE'])
def delete_violation_records():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id')
        date = data.get('date')
        camera_id = data.get('camera_id')
        print(camera_id)

        result = ChallanController.delete_violation_history(vehicle_id, date, camera_id)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500




######################################################Challan & Challan Details#############################################################################
@app.route('/addchallanrecord', methods=['POST'])
def create_challan():
    try:
        data = request.json
        violation_history_id = data.get('violation_history_id')
        violation_ids = data.get('violation_ids') #List
        violator_cnic = data.get('violator_cnic')
        violator_name = data.get('violator_name')
        mobile_number=data.get('mobile_number')
        vehicle_number=data.get('vehicle_number')
        warden_id = data.get('warden_id')
        fine_amount = data.get('fine_amount')
        status = data.get('status')

        if not all([violation_history_id, violation_ids, violator_cnic,violator_name,mobile_number,vehicle_number,warden_id, fine_amount, status]):
            return jsonify({"error": "Missing required fields"}), 400


        date =  datetime.now()  # Assuming you want to use the current UTC time for the date

        success, challan_id = ChallanController.add_challan_history_and_details(
            date, status, violation_ids, violation_history_id,violator_cnic,violator_name,mobile_number,vehicle_number, warden_id, fine_amount
        )

        if success:
            response = Controller.ImageControllerAndNotification.add_notification(
                recipient_type="User",
                recipient_id=violator_cnic,
                type_="Violation Alert",
                message=f"⚠️ {violator_name}, your vehicle ({vehicle_number}) has committed a traffic violation .check your challan details."

            ,violation_id=violation_history_id
            )
            print(f"🔔 Notification Generated for Violator with Cnic: {violator_cnic}")

            return jsonify({"success": True, "challan_id": challan_id}), 201
        else:
            return jsonify({"error": "Failed to add challan record"}), 500

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getchallans', methods=['POST'])
def retrieve_challans():
    try:
        data = request.json
        challan_id = data.get('challan_id')
        user_id = data.get('user_id')
        warden_id = data.get('warden_id')

        print(user_id)

        success, result = ChallanController.get_challans(challan_id, user_id, warden_id)

        if success:
            return jsonify(result), 200
        else:
            return jsonify({"error": result}), 404 if challan_id else 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/updatechallanstatus', methods=['PUT'])
def update_challan():
    try:
        data = request.json
        challan_id = data.get('challan_id')
        new_status = data.get('new_status')

        if not challan_id or not new_status:
            return jsonify({"error": "Missing required fields"}), 400

        success, result = ChallanController.update_challan_status(challan_id, new_status)

        if success:
            return jsonify(result), 200
        else:
            return jsonify({"error": result}), 404

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

#########################################################################################################################################

# Specify the folder to save uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'Predictions')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/autoupload-image', methods=['POST'])
def autoupload_image():
    try:
        # Check if the request contains a file
        if 'image' not in request.files:
            return "No image file provided", 400

        file = request.files['image']
        bikenumber = request.form.get('bikenumber')
        text_value = request.form.get('camera_id')


        # Read and open the image using PIL
        if file.filename != '':
            image = Image.open(io.BytesIO(file.read()))

            # Save the image in the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            image.save(file_path)
            model_path = r'C:\Drive D\Pycharm\TrafficGuardian\yolov8mtrafficmodel.pt'
            model_pathr= r'C:\Drive D\Pycharm\TrafficGuardian\yolov8s.pt'
            preprocessed_image=YoloController.preprocess_image(image)

            print("Preprocessed image shape:", preprocessed_image.shape)
            violations_and_plates = YoloController.detect_violations_from_Image(file_path, model_path, model_pathr)

            try:
                camera = CameraChowkiController.get_camera_by_id(text_value)[0]
                camera_location = camera['Direction']
            except Exception as e:
                return jsonify({"message": f"An error occurred in getting location: {str(e)}"}), 500



            try:
                bike = ChallanController.get_vehicle_by_licenseplate(bikenumber)
                if 'error' in bike:
                    message = ChallanController.add_vehicle(bikenumber, 'Bike')
                    if 'Successfully' in message:
                        bike = ChallanController.get_vehicle_by_licenseplate(bikenumber)
                print(bike['id'], "bike id")
            except Exception as e:
                return jsonify({"message": f"An error occurred in getting Bike: {str(e)}"}), 500

            print(bike)
            status = 'Pending'
            created_date = datetime.today().strftime('%Y-%m-%d')
            print(text_value, bikenumber, camera_location, status, created_date)
            violations_ids=[]
            try:

                detected_violations=violations_and_plates[0]["violations"]
                print(detected_violations)

                for i in detected_violations:
                    if i == 'No Helmet':
                        violations_ids.append(1)
                    elif i == 'Side Mirror':
                        violations_ids.append(3)
                    elif i.__contains__('Oversitting'):
                        violations_ids.append(2)

            except Exception as e:
                return jsonify({"message": f"An error occurred getting Violations: {str(e)}"}), 500

            try:

                 response, code = ChallanController.add_violation_history_and_details(bike['id'], created_date,
                                                                                     camera_location, status,file_path,text_value,violations_ids)
            except Exception as e:
                return jsonify({"message": f"An error occurred Add Violation History: {str(e)}"}), 500

            # Return the result in JSON format
            return jsonify({
                'message': 'Image uploaded and processed successfully',
                'violations_and_plates': violations_and_plates
            }), 200
        else:
            return jsonify({"message": "File has no filename"}), 400

    except Exception as e:
        # Handle exceptions that may occur
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route('/upload-image', methods=['POST'])
def upload_image():
    try:
        # Check if the request contains a file
        if 'image' not in request.files:
            return "No image file provided", 400

        file = request.files['image']

        # Read and open the image using PIL
        if file.filename != '':
            image = Image.open(io.BytesIO(file.read()))

            # Save the image in the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            image.save(file_path)
            model_path = r'C:\Users\Syed Mohsin Ali\PycharmProjects\TrafficGuardian\yolov8s.pt'
            preprocessed_image=YoloController.preprocess_image(image)
            print("Preprocessed image shape:", preprocessed_image.shape)
            violations_and_plates = YoloController.detect_violations_from_Image(file_path, model_path)

            # Return the result in JSON format
            return jsonify({
                'message': 'Image uploaded and processed successfully',
                'violations_and_plates': violations_and_plates
            }), 200
        else:
            return jsonify({"message": "File has no filename"}), 400

    except Exception as e:
        # Handle exceptions that may occur
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

################################################################################################
# Multi Camera Feed

# In-memory image storage dictionary
camera_images_list = [] # Format: [{'camera_id': image_file}]

import traceback

@app.route('/upload-multicameraimages', methods=['POST'])
def upload_images():
    try:
        print("==> Incoming request to /upload-multicameraimages")
        print("Form Data:", request.form)
        print("Files Received:", request.files)

        indices_str = request.form.get('image_indices', '')
        indices = indices_str.split(',') if indices_str else []

        print(f"Parsed indices: {indices}")

        uploaded_info = []
        camera_images_list = []

        files = request.files.getlist('images')
        print(f"Number of images received: {len(files)}")

        for i, image_file in enumerate(files):
            if i < len(indices):
                camera_id = indices[i]
            else:
                camera_id = str(i)

            print(f"Processing image {i}: camera_id={camera_id}, filename={image_file.filename}")

            if image_file.filename != '':
                try:
                    image = Image.open(io.BytesIO(image_file.read()))
                    camera_images_list.append({
                        "cam_id": camera_id,
                        "image": image
                    })

                    uploaded_info.append({
                        'camera_id': camera_id,
                        'filename': image_file.filename,
                        'status': 'stored in memory'
                    })

                except Exception as img_err:
                    print(f"[ERROR] Failed to read image {i}: {img_err}")
                    continue

        print("Calling detection logic with images:")
        print(f"camera_images_list: {[item['cam_id'] for item in camera_images_list]}")

        # Call the detection function
        response, code = ChallanController.autoviolationdetection_fromcameraimage(camera_images_list)
        print("Detection completed. Returning response.")
        return response, code

    except Exception as e:
        print("[ERROR] Exception in /upload-multicameraimages:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/parallel_simulation-multicameraimages', methods=['POST'])
def parallel_simulation_upload_images():
    try:
        print("==> Incoming request to /parallel_simulation-multicameraimages")
        print("Form Data:", request.form)
        print("Files Received:", request.files)

        indices_str = request.form.get('image_indices', '')
        indices = indices_str.split(',') if indices_str else []

        print(f"Parsed indices: {indices}")

        uploaded_info = []
        camera_images_list = []

        files = request.files.getlist('images')
        print(f"Number of images received: {len(files)}")

        for i, image_file in enumerate(files):
            if i < len(indices):
                camera_id = indices[i]
            else:
                camera_id = str(i)

            print(f"Processing image {i}: camera_id={camera_id}, filename={image_file.filename}")

            if image_file.filename != '':
                try:
                    image = Image.open(io.BytesIO(image_file.read()))
                    camera_images_list.append({
                        "cam_id": camera_id,
                        "image": image
                    })

                    uploaded_info.append({
                        'camera_id': camera_id,
                        'filename': image_file.filename,
                        'status': 'stored in memory'
                    })

                except Exception as img_err:
                    print(f"[ERROR] Failed to read image {i}: {img_err}")
                    continue

        print("Calling detection logic with images:")
        print(f"camera_images_list: {[item['cam_id'] for item in camera_images_list]}")

        # Call the detection function
        response, code = ChallanController.SimulationParallel_autoviolationdetection_fromcameraimage(camera_images_list)
        print("Detection completed. Returning response.")
        return response, code

    except Exception as e:
        print("[ERROR] Exception in /parallel_simulation-multicameraimages:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



@app.route('/get-images/<int:id>', methods=['GET'])
def get_images_by_violationid (id):
    try:
        # Query to fetch user images by CNIC (replace with actual query logic)
        violation_img=ImageControllerAndNotification.get_all_img_violationid(id)
        if not violation_img :
            return jsonify({"message": "No images found for this Violation ID."}), 404

        # Prepare image data to return in the response



        return jsonify({"image_data": violation_img }), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    # Check if the file exists in the directory
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({"error": "File not found"}), 404

# 1. Add Notification
@app.route('/notifications', methods=['POST'])
def create_notification():
    data = request.json
    required_fields = ['recipient_type', 'recipient_id', 'type', 'message']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    result = ImageControllerAndNotification.add_notification(
        recipient_type=data['recipient_type'],
        recipient_id=data['recipient_id'],
        type_=data['type'],
        message=data['message']
    )
    return jsonify(result)


@app.route('/getnotifications', methods=['POST'])
def get_all_notifications():
    data = request.get_json()

    recipient_type = data.get('recipient_type')
    recipient_id = data.get('recipient_id')

    print(recipient_type)
    print(recipient_id)

    result = ImageControllerAndNotification.get_notifications(
        recipient_type=recipient_type,
        recipient_id=recipient_id
    )

    return jsonify(result)


# 3. Update Notification
@app.route('/notifications/<int:notification_id>', methods=['PUT'])
def update_existing_notification(notification_id):
    data = request.json
    result = ImageControllerAndNotification.update_notification(
        notification_id,
        type_=data.get('type'),
        message=data.get('message')
    )
    return jsonify(result)

# 4. Delete Notification
@app.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_existing_notification(notification_id):
    result =ImageControllerAndNotification.delete_notification(notification_id)
    return jsonify(result)

# 5. Mark Notification as Read/Unread
@app.route('/notifications/<int:notification_id>/mark', methods=['PUT'])
def mark_notification(notification_id):
    data = request.json
    is_read = data.get('is_read', True)
    result = ImageControllerAndNotification.mark_notification_status(notification_id, is_read)
    return jsonify(result)


@app.route('/getnotificationsforuser', methods=['POST'])
def get_all_notifications_user():
    data = request.get_json()

    recipient_type = data.get('recipient_type')
    recipient_id = data.get('recipient_id')

    print(recipient_type)
    print(recipient_id)

    result = ImageControllerAndNotification.get_notifications(
        recipient_type=recipient_type,
        recipient_id=recipient_id
    )

    return jsonify(result)

@app.route('/on_duty_wardens/<int:camera_id>', methods=['GET'])
def on_duty_wardens(camera_id):
      # if your function is in another file

    wardens = CameraChowkiController.get_on_duty_wardens(camera_id)

    result = [{
        'id': w.id,
        'name': w.name,

    } for w in wardens]

    return jsonify({'status': 'success', 'wardens': result})

####################################################################################

# Get all naka connections              useless
@app.route('/nakagrapg', methods=['GET'])
def get_all_nakas():
    try:
        return NakaGraphController.get_all_connections()
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# Get all naka connections              useless
@app.route('/nakagrapgforflutter', methods=['GET'])
def get_all_nakas_forFlutter():
    try:
        return NakaGraphController.get_naka_graph_for_flutter()
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Get naka by ID (query param: ?id=1)
@app.route('/naka/id', methods=['GET'])
def get_naka_by_id():
    try:
        naka_id = request.args.get('id')
        if not naka_id:
            return jsonify({'error': 'Naka ID is required'}), 400
        return NakaGraphController.get_naka_by_id(naka_id)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Update naka connection
@app.route('/naka', methods=['PUT'])
def update_naka():
    try:
        data = request.get_json()
        naka_id = data.get('id')
        from_id = data.get('FromNakaID')
        to_id = data.get('ToNakaID')
        distance = data.get('DistanceKM')

        if not all([naka_id, from_id, to_id, distance]):
            return jsonify({'error': 'id, FromNakaID, ToNakaID, and DistanceKM are required'}), 400

        return NakaGraphController.update_connection(naka_id, from_id, to_id, distance)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Delete naka connection by name (body param)
@app.route('/deletelinknaka', methods=['DELETE'])
def delete_naka():
    try:
        data = request.get_json()
        naka_id = data.get('id')
        to_naka = data.get('tonakaid')
        if not naka_id or not to_naka:
            return jsonify({'error': 'Naka ID and Link Naka id is required'}), 400

        print(naka_id,to_naka)
        return NakaGraphController.delete_connection(naka_id,to_naka)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

# Delete naka connection by name (now using GET with query parameters)
@app.route('/rdeletelinknaka', methods=['DELETE'])
def rdelete_naka():
    try:
        naka_id = request.args.get('id')
        to_naka = request.args.get('tonakaid')
        if not naka_id or not to_naka:
            return jsonify({'error': 'Naka ID and Link Naka ID are required'}), 400

        print(naka_id, to_naka)
        return NakaGraphController.delete_connection(naka_id, to_naka)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# Delete naka connection by query param (?id=1)
@app.route('/linknaka/deletebyid', methods=['DELETE'])
def delete_naka_by_query():
    try:
        naka_id = request.args.get('id')
        to_naka = request.args.get('tonakaid')

        if not naka_id or not to_naka:
            return jsonify({'error': 'Naka ID and Link Naka id is required as query parameter'}), 400
        print(naka_id, to_naka)
        return NakaGraphController.delete_connection(naka_id,to_naka)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



# this rule return graph as well as All Naka of custom hops

@app.route('/getgraph', methods=['GET'])
def initialize_naka_graph():
    try:
        data = request.get_json()
        naka_id = data.get('naka_id')
        max_hops = data.get('max_hops')

        if naka_id is None or max_hops is None:
            return jsonify({'error': 'naka_id and max_hops are required'}), 400

        # Load the graph and alerts using the NakaGraphController
        return NakaGraphController.load_graph_and_alerts(start=naka_id, max_hops=max_hops)

    except Exception as exp:
        print(f"Error in /getgraph: {str(exp)}")
        return jsonify({'error': str(exp)}), 500




# @app.route('/naka/<int:naka_id>/nexthops/<int:max_hops>', methods=['GET'])
# def get_next_hops(naka_id, max_hops):
#     return NakaGraphController.get_next_hops(naka_id, max_hops)


# This Only Show  Next Custom Hobs List of Specific Naka each Hob Seperate
@app.route('/naka/nexthops', methods=['POST'])
def get_next_hops():
    try:
        data = request.get_json()
        naka_id = data.get('naka_id')
        max_hops = data.get('max_hops')

        if naka_id is None or max_hops is None:
            return jsonify({"error": "naka_id and max_hops are required"}), 400

        return NakaGraphController.get_next_hops(naka_id, max_hops)

    except Exception as exp:
        print(f"Error in /naka/nexthops: {str(exp)}")
        return jsonify({'error': str(exp)}), 500


@app.route('/linkNakawithnaka', methods=['POST'])
def add_NakawithNaka():
    try:
        data = request.get_json()
        from_id = data.get('FromNakaID')
        to_id_list = data.get('ToNakaID')         # Should be a list
        distance_list = data.get('DistanceKM')    # Should be a list

        # Check if inputs exist and are lists of same length
        if not all([from_id, to_id_list, distance_list]):
            return jsonify({'error': 'FromNakaID, ToNakaID, and DistanceKM are required'}), 400

        if not isinstance(to_id_list, list) or not isinstance(distance_list, list):
            return jsonify({'error': 'ToNakaID and DistanceKM should be lists'}), 400

        if len(to_id_list) != len(distance_list):
            return jsonify({'error': 'ToNakaID and DistanceKM lists must be the same length'}), 400

        message,code = NakaGraphController.add_connection(from_id, to_id_list, distance_list)
        return jsonify(message), code

    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500



@app.route('/getonesidegraph', methods=['GET'])
def onesidegraph():
    return jsonify( NakaGraphController.build_graphoneway_from_db())

@app.route('/gettwosidegraph', methods=['GET'])
def twosidegraph():
    return jsonify( NakaGraphController.build_graph_from_db())

# im using it to get direct naka Connection
@app.route('/getnakadirectlink', methods=['POST'])  # Changed to POST
def get_NakaDirection():
    try:
        data = request.get_json()
        naka_id = data.get('FromNakaID')


        if not naka_id:
            return jsonify({'error': 'FromNakaID is required'}), 400
        print(naka_id)
        # Load graph and alerts from controller
        response = NakaGraphController.load_graph_and_alerts(start=naka_id, max_hops=1)

        chowki_details = CameraChowkiController.get_chowkis_by_ids_forNakaLink(response["alerts"])

        # Build final response
        # response = {
        #     "alerts": response['alerts'],
        #     "chowkis": chowki_details,
        #     "graph": response['graph']
        # }

        return jsonify(chowki_details), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500

@app.route('/testing_get_naka', methods=['POST'])  # Changed to POST
def get_testing():
    try:
        data = request.get_json()
        naka_id = data.get('FromNakaID')
        bike_number = data.get('bike')
        maxhops = data.get('hops')
        location=data.get('location')
        violationhistory_id=data.get('violationhistory_id')
        if not maxhops:
            maxhops=1
        if not naka_id or not bike_number or not location or not violationhistory_id:
            return jsonify({'error': 'FromNakaID ,location and bike Number  and violationhistory_id is required '}), 400
        print(naka_id)
        # Load graph and alerts from controller
        response = ChallanController.get_custom_hops_naka_of_naka([naka_id],bike_number, location,maxhops,violationhistory_id)


        return jsonify(response), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


    except Exception as exp:
        print(str(exp))
        return jsonify({'error': str(exp)}), 500






# ✅ Get all stolen bikes
@app.route('/stolenbike', methods=['GET'])
def get_all_stolen_bikes():
    try:
        bikes = StolenBikeController.get_all_bikes()
        return jsonify(bikes), 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# ✅ Get stolen bike by ID
@app.route('/stolenbikebyid', methods=['POST'])
def get_stolen_bike_by_id():
    try:
        data = request.get_json()
        bike_id = data.get('id')
        if not bike_id:
            return jsonify({"error": "Bike ID is required"}), 400

        bike = StolenBikeController.get_bike_by_id(bike_id)
        return jsonify(bike), 200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# ✅ Get stolen bike by number plate
@app.route('/stolenbikebyplate', methods=['POST'])
def get_stolen_bike_by_plate():
    try:
        data = request.get_json()
        plate = data.get('NumberPlate')
        if not plate:
            return jsonify({"error": "Number Plate is required"}), 400

        result = StolenBikeController.get_bike_by_number_plate(plate)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# ✅ Add new stolen bike
@app.route('/addstolenbike', methods=['POST'])
def add_stolen_bike():
    try:
        data = request.get_json()
        plate = data.get('NumberPlate')
        if not plate:
            return jsonify({"error": "Number Plate is required"}), 400

        result = StolenBikeController.add_bike(data)
        if 'error' in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# ✅ Delete stolen bike by plate
@app.route('/deletestolenbikebyplate', methods=['DELETE'])
def delete_stolen_bike_by_plate():
    try:
        plate = request.args.get('NumberPlate')
        if not plate:
            return jsonify({"error": "Number Plate is required as query parameter"}), 400

        message, code = StolenBikeController.delete_bike_by_plate(plate)
        return jsonify(message), code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# ✅ Update stolen bike by plate
@app.route('/updatestolenbike', methods=['PUT'])
def update_stolen_bike():
    try:
        data = request.get_json()
        plate = data.get('NumberPlate')
        if not plate:
            return jsonify({"error": "Number Plate is required"}), 400

        result = StolenBikeController.update_bike_by_plate(plate, data)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


# ✅ Change status of a stolen bike
@app.route('/changestolenbikestatus', methods=['PUT'])
def change_stolen_bike_status():
    try:
        data = request.get_json()
        plate = data.get('NumberPlate')
        new_status = data.get('new_status')

        if not plate or not new_status:
            return jsonify({"error": "Number Plate and new_status are required"}), 400

        result, code = StolenBikeController.change_bike_status(plate, new_status)
        return jsonify(result), code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/check_challanallowed', methods=['POST'])
def check_challan_allowed():
    try:
        data = request.get_json()
        license_plate = data.get("license_plate")

        if not license_plate:
            return jsonify({"status": "Error", "reason": "license_plate is required"}), 400
        response=ChallanController.is_challan_allowed(license_plate)
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "status": "Error",
            "reason": str(e)
        }), 500



@app.route("/assign-warden-duty", methods=["POST"])
def assign_warden_duty():
    try:
        data = request.get_json()
        return WardenChowkiController.assign_warden_duties(data)
    except Exception as e:
        print(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # cleanup_thread = threading.Thread(target=ChallanController.clean_old_vehicles(), daemon=True)
    # cleanup_thread.start()

    app.run(host='0.0.0.0', port=4321, debug=True)

#
# def get_local_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         # doesn't have to be reachable
#         s.connect(('10.255.255.255', 1))
#         IP = s.getsockname()[0]
#     except Exception:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     return IP
# local_ip = get_local_ip()
# port = 4321
# print(f" * Running on local IP: http://{local_ip}:{port}")
# print(f" * Serving on all interfaces: http://0.0.0.0:{port}")
#
# serve(Model.Configure.app, host='0.0.0.0', port=4321, threads=50)
#
