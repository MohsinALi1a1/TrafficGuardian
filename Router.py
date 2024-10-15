from datetime import datetime

from Model.Configure import app
from flask import  request ,jsonify
from Controller import LocationController
from Controller import CameraChowkiController
from Controller import WardenChowkiController



########################################  City  ############################################

@app.route('/city', methods=['GET'])
def get_all_cities():
    try:
        city_list = LocationController.get_all_City()
        print(city_list)
        return jsonify(city_list)
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
        return jsonify(city)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/citybyname', methods=['GET'])
def get_city_by_name():
    try:
        city_name = request.args.get('name')
        city = LocationController.get_city_by_name(city_name)
        return jsonify(city)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addcity', methods=['POST'])
def add_city():
    try:
        data = request.get_json()
        city_name = data.get('name')

        if not city_name:
            return jsonify({"error": "City name is required"}), 400


        # Add the new city
        city=LocationController.add_city(city_name)
        return jsonify(city), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/deletecity', methods=['DELETE'])
def delete_city_by_name():
    try:
        data = request.get_json()
        city_name = data.get('name')
        if not city_name:
            return jsonify({"error": "City name is required"}), 400

        # Delete the city and get the success message
        message = LocationController.delete_city(city_name)
        return jsonify(message)
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

        message=LocationController.update_city(city_name, new_name)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


########################################  PLACE  ############################################


@app.route('/place', methods=['GET'])
def get_all_places():
    try:
        city_name = request.args.get('name')  # Use query parameter
        if not city_name:
            return jsonify({"error": "City name is required"}), 400

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
        return jsonify(place)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/placebyname', methods=['GET'])
def get_place_by_name():
    try:
        place_name = request.args.get('name')
        place = LocationController.get_place_by_name(place_name)
        return jsonify(place)
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

        # Add the new Place
        place=LocationController.add_place(city_name,place_name)
        return jsonify(place), 201
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/deleteplace', methods=['DELETE'])
def delete_place_by_name():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        city_name = data.get('cityname')
        if not place_name or not city_name:
            return jsonify({"error": "Place name & City Name  is required"}), 400

        # Delete the Place and get the success message
        message = LocationController.delete_place(city_name,place_name)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



# Route to update a Place
@app.route('/updateplace', methods=['PUT'])
def update_place():
    try:
        data = request.get_json()
        place_name = data.get('name')
        new_name = data.get('new_name')

        if not place_name or not new_name:
            return jsonify({"error": "Both current Place name and new name are required"}), 400

        message=LocationController.update_place(place_name, new_name)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


########################################  Directions  ############################################

@app.route('/directions', methods=['GET'])
def get_all_directions():
    try:
        data = request.get_json()
        place_name = data.get('name')
        print(place_name)
        if not place_name:
            return jsonify({"error": "Place name is required"}), 400
        directions = LocationController.get_all_Directions(place_name)
        if not directions:
            return jsonify({"error": "No Direction found for the specified Place"}), 404
        return jsonify(directions)
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
        return jsonify(directions)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/directionbyname', methods=['GET'])
def get_direction_by_name():
    try:
        direction_name = request.args.get('name')
        direction = LocationController.get_direction_by_name(direction_name)
        return jsonify(direction)
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

        # Add the new Direction
        direction=LocationController.add_direction(place_name,direction_name)
        return jsonify(direction), 201
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

        # Delete the Place and get the success message
        message = LocationController.delete_direction(place_name,direction_name)
        return jsonify(message)
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

        message=LocationController.update_direction(place_name,direction_name,new_name)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Camera  ############################################
@app.route('/camera', methods=['GET'])
def get_all_camera():
    try:
        data = request.get_json()
        place_name = data.get('placename')
        direction_name = data.get('directionname')

        print(place_name , direction_name)
        if not place_name or not  direction_name:
            return jsonify({"error": "Place name & direction name is required"}), 400

        cameras= CameraChowkiController.get_all_camera(place_name, direction_name)
        if not cameras:
            return jsonify({"error": f"No camera found for the specified Place {place_name} on Direction {direction_name}"}), 404
        return jsonify(cameras)
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
        type=data.get('type')

        if not name or not direction_name or not type:
            return jsonify({"error": " Camera,Direction name & Camera Type  is required"}), 400

        # Add the new Direction
        camera = CameraChowkiController.add_camera(name,direction_name,type)
        return jsonify(camera), 201
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

        # Delete the Camera and get the success message
        message = CameraChowkiController.delete_camera(camera_name,direction_name,camera_type)
        return jsonify(message)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500
########################################  Chowki  ############################################

@app.route('/chowki', methods=['GET'])
def get_all_chowki():
    try:
        data = request.get_json()
        place_name = data.get('placename')

        print(place_name )
        if not place_name :
            return jsonify({"error": "Place name  is required"}), 400

        chowki= CameraChowkiController.get_all_Chowki(place_name)
        if not chowki:
            return jsonify({"error": f"No Chowki found for the specified Place {place_name}"}), 404
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

        # Delete the Chowki and get the success message
        message = CameraChowkiController.delete_chowki(name,place_name)
        return jsonify(message)
    except Exception as exp:
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

        chowki_info = CameraChowkiController.get_all_ChowkiCamera_byplace(place_name)

        if not chowki_info:
            return jsonify({"error": f" Camera_Chowki not found for the specified Place {place_name}"}), 404

        return jsonify(chowki_info)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/linkcamerawithchowki', methods=['GET'])
def get_all_camera_with_chowki():
    try:
        data = request.get_json()
        chowki_name = data.get('chowkiname')

        print(chowki_name )
        if not chowki_name :
            return jsonify({"error": "Chowki name  is required"}), 400

        chowki_info = CameraChowkiController.get_all_linkCamera_with_Chowki(chowki_name)

        if not chowki_info:
            return jsonify({"error": f" Camera is linked for the specified Chowki {chowki_name}"}), 404

        return jsonify(chowki_info)
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

        # Convert string times to time objects
        shift_starttime = datetime.strptime(shift_starttime, "%H:%M:%S").time()
        shift_endtime = datetime.strptime(shift_endtime, "%H:%M:%S").time()

        # Add the new shift
        shift_response = WardenChowkiController.add_shift(shift_name, shift_starttime, shift_endtime)

        return jsonify(shift_response), 201
    except ValueError as ve:
        return jsonify({'error': 'Invalid time format. Use HH:MM:SS.'}), 400
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
        message = WardenChowkiController.update_shift(shift_name,shift_starttime,shift_endtime)
        return jsonify(message)
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



@app.route('/wardensincity', methods=['GET'])
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
        return jsonify({'error': str(exp)}), 500



#########################################################################################################################################



if __name__ == "__main__":
    app.run()