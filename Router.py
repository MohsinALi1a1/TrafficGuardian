import io
import os
from PIL import Image
from datetime import datetime
from Model.Configure import app
from flask import  request ,jsonify
from Controller import LocationController, ChallanController
from Controller import CameraChowkiController
from Controller import WardenChowkiController
from Controller import yolov8


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

        if not city_id:
            return jsonify({"error": "City id is required"}), 400
        city ,code = LocationController.get_city_by_id(city_id)
        return jsonify(city),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/citybyname', methods=['GET'])
def get_city_by_name():
    try:
        city_name = request.args.get('name')
        city ,code= LocationController.get_city_by_name(city_name)
        return jsonify(city),code
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
        city,code=LocationController.add_city(city_name)
        return jsonify(city), code
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
        message,code = LocationController.delete_city(city_name)
        return jsonify(message),code
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

        message,code=LocationController.update_city(city_name, new_name)
        return jsonify(message),code
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
        place,code = LocationController.get_place_by_id(place_id)
        return jsonify(place),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/placebyname', methods=['GET'])
def get_place_by_name():
    try:
        place_name = request.args.get('name')
        place ,code= LocationController.get_place_by_name(place_name)
        return jsonify(place),code
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
        place,code=LocationController.add_place(city_name,place_name)
        return jsonify(place), code
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
        message,code = LocationController.delete_place(city_name,place_name)
        return jsonify(message),code
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

        message,code=LocationController.update_place(place_name, new_name)
        return jsonify(message),code
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
        directions,code = LocationController.get_all_Directions(place_name)
        return jsonify(directions),code
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
        directions,code = LocationController.get_direction_by_id(direction_id)
        return jsonify(directions),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/directionbyname', methods=['GET'])
def get_direction_by_name():
    try:
        direction_name = request.args.get('name')
        direction,code = LocationController.get_direction_by_name(direction_name)
        return jsonify(direction),code
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
        direction,code=LocationController.add_direction(place_name,direction_name)
        return jsonify(direction), code
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
        message ,code= LocationController.delete_direction(place_name,direction_name)
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

        message, code=LocationController.update_direction(place_name,direction_name,new_name)
        return jsonify(message),code
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

        cameras,code= CameraChowkiController.get_all_camera(place_name, direction_name)

        return jsonify(cameras),code
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
        camera ,code= CameraChowkiController.get_camera_by_id(camera_id)
        return jsonify(camera),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/camerabyname', methods=['GET'])
def get_camera_by_name():
    try:
        camera_name = request.args.get('name')
        if not camera_name:
            return jsonify({'error':'Camera name is required in argument'}),400

        camera ,code=CameraChowkiController.get_camera_by_name(camera_name)
        return jsonify(camera),code
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

        camera,code = CameraChowkiController.add_camera(name,direction_name,cam_type)
        return jsonify(camera), code
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
        message ,code = CameraChowkiController.delete_camera(camera_name,direction_name,camera_type)
        return jsonify(message),code
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
        chowki,code= CameraChowkiController.get_all_Chowki(place_name)
        return jsonify(chowki),code
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
        chowki ,code= CameraChowkiController.get_chowki_by_id(chowki_id)
        return jsonify(chowki),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/chowkibyname', methods=['GET'])
def get_chowki_by_name():
    try:
        data = request.get_json()
        chowki_name = data.get('name')
        if not chowki_name:
            return jsonify({'error': 'Naka Name is Required'}),400
        chowki,code =CameraChowkiController.get_chowki_by_name(chowki_name)
        return jsonify(chowki),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

@app.route('/addchowki', methods=['POST'])
def add_chowki():
    try:
        data = request.get_json()
        chowkiname = data.get('name')
        place_name = data.get('placename')

        if not chowkiname or not place_name:
            return jsonify({"error": " Chowki Name,Place name is required"}), 400

        # Add the new Chowki
        chowki,code = CameraChowkiController.add_chowki(chowkiname,place_name)
        return jsonify(chowki), code
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
        message,code = CameraChowkiController.delete_chowki(name,place_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  CameraChowki  ############################################


@app.route('/chowkicameraincity', methods=['GET'])
def get_all_chowkicamera_bycity():
    try:
        data = request.get_json()
        city_name = data.get('cityname')

        print(city_name )
        if not city_name :
            return jsonify({"error": "city name  is required"}), 400

        chowki_info,code = CameraChowkiController.get_all_ChowkiCamera_bycity(city_name)

        if not chowki_info:
            return jsonify({"error": f" Camera_Chowki not found for the specified City {city_name}"}), 404

        return jsonify(chowki_info),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500




@app.route('/chowkicameraplace', methods=['GET'])
def get_all_chowkicamera_byplace():
    try:
        data = request.get_json()
        place_name = data.get('placename')

        print(place_name )
        if not place_name :
            return jsonify({"error": "place name  is required"}), 400

        chowki_info ,code= CameraChowkiController.get_all_ChowkiCamera_byplace(place_name)

        if not chowki_info:
            return jsonify({"error": f" Camera_Chowki not found for the specified Place {place_name}"}), 404

        return jsonify(chowki_info),code
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

        chowki_info,code = CameraChowkiController.get_all_linkCamera_with_Chowki(chowki_name)

        if not chowki_info:
            return jsonify({"error": f" No Camera is linked for the specified Chowki {chowki_name}"}), 404

        return jsonify(chowki_info),code
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

        chowki_info,code = CameraChowkiController.get_all_linkChowki_with_Camera(camera_name)

        if not chowki_info:
            return jsonify({"error": f" Camera is linked for the specified Chowki {camera_name}"}), 404

        return jsonify(chowki_info),code
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

        chowki,code = CameraChowkiController.link_camera_to_chowki(chowki_name, camera_list)
        return jsonify(chowki), code
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

        chowki,code = CameraChowkiController.unlink_camera_from_chowki(chowki_name, camera_list)
        return jsonify(chowki), code
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
        result ,code= CameraChowkiController.update_linked_cameras_with_chowki(
            chowki_name,
            link_camera_list or [],  # Default to empty list if no cameras to link
            unlink_camera_list or []  # Default to empty list if no cameras to unlink
        )

        return jsonify({"message": result}), code  # Return the result with a 200 status code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Shift  ############################################

@app.route('/shift', methods=['GET'])
def get_all_shift():
    try:
        shift_list = WardenChowkiController.get_all_Shift()
        print(shift_list)
        return jsonify(shift_list),200
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
        shift,code=WardenChowkiController.get_shift_by_id(shift_id)
        return jsonify(shift),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/shiftbyname', methods=['GET'])
def get_shift_by_name():
    try:
        data = request.get_json()
        shift_name = data.get('shiftname')
        if not shift_name:
            return jsonify({"error": "Shift name is required"}), 400
        shift,code = WardenChowkiController.get_shift_by_name(shift_name)
        return jsonify(shift),code
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
        message,code = WardenChowkiController.update_shift(shift_name,shift_starttime,shift_endtime)
        return jsonify(message),code
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

        message,code=LocationController.update_city(city_name, new_name)
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  Traffic Warden  ############################################

@app.route('/trafficwarden', methods=['GET'])
def get_all_trafficwarden():
    try:
        warden_list ,code= WardenChowkiController.get_all_warden()
        return jsonify(warden_list),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/wardensincity', methods=['GET'])
def get_warden_in_city():
    try:
        data = request.get_json()
        city_name = data.get('cityname')
        if not city_name:
            return jsonify({"error": "City name is required"}), 400
        warden,code=WardenChowkiController.get_all_warden_city(city_name)
        if warden:
            return jsonify(warden),code
        else:
            return jsonify({"Invalid": f"No traffic Warden exist from the location {city_name}"}), 400
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/wardentbycnic', methods=['GET'])
def get_warden_by_cnic():
    try:
        data = request.get_json()
        warden_cnic = data.get('cnic')
        if not warden_cnic:
            return jsonify({"error": "Warden Cnic is required"}), 400
        warden,code = WardenChowkiController.get_warden_by_cnic(warden_cnic)
        return jsonify(warden),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/addtrafficwarden', methods=['POST'])
def add_warden():
    try:
        data = request.get_json()
        name = data.get('name')
        badge_number = data.get('badgenumber')
        address = data.get('address')
        cnic = data.get('cnic')
        email = data.get('email')
        mobile_number = data.get('mobilenumber')
        city_name=data.get('cityname')

        if not name or not badge_number or not address or not cnic or not email or not mobile_number or not city_name:
            return jsonify({"error": "Warden name, badge_number , address, cnic , email, mobile_number, and city_name are required."}), 400

        # Add the new warden
        new_warden,code = WardenChowkiController.add_warden(name, badge_number, address, cnic, email, mobile_number, city_name)
        return jsonify(new_warden), code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



@app.route('/deletewarden', methods=['DELETE'])
def delete_warden_route():
    try:
        data = request.get_json()
        cnic = data.get('cnic')

        if not cnic:
            return jsonify({"error": "CNIC  is required"}), 400
        message,code=WardenChowkiController.delete_warden(cnic)
        return jsonify(message),code

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/updatewarden', methods=['PUT'])
def update_warden_route():

    try:
        data = request.get_json()
        cnic = data.get('cnic')
        if not cnic:
            return jsonify({'error':'Cnic Is required'}),400

        message,code=WardenChowkiController.update_warden(
            cnic,
            name=data.get('name'),
            badge_number=data.get('badgenumber'),
            address=data.get('address'),
            email=data.get('email'),
            mobile_number=data.get('mobilenumber'),
            city_name=data.get('cityname')
        )
        return jsonify(message),code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500
########################################  WardenChowki  ############################################

@app.route('/wardenassignments', methods=['POST'])
def warden_assignments():
    try:
        duty,code=WardenChowkiController.create_duty_roster()
        return jsonify({"sucessfully":duty}),code
    except Exception as exp:
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
        new_assignment,code = WardenChowkiController.assignwarden(warden_id, chowki_id, shift_id)
        return jsonify(new_assignment), code
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getassignjobs', methods=['GET'])
def get_all_dutyroster():
    try:

        dutyroster_list = WardenChowkiController.get_all_assignments_on_last_assign_date()

        print(dutyroster_list)
        return jsonify(dutyroster_list),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getassignjobofwarden', methods=['GET'])
def get_all_dutyroster_of_warden():
    try:
        data = request.get_json()
        badge_number = data.get('badgenumber')
        if not badge_number:
            return jsonify({'error':'Badge Number are required'}),400
        dutyroster_list = WardenChowkiController.get_dutyroster_for_warden(badge_number)
        print(dutyroster_list)
        return jsonify(dutyroster_list),200
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500



########################################  Vehicle  ########################################################
@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    try:
        vehicle_list = ChallanController.get_all_vehicles()
        return jsonify(vehicle_list)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/vehiclebyid', methods=['GET'])
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


@app.route('/userbyid', methods=['GET'])
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

        if not name or not cnic or not mobilenumber:
            return jsonify({"error": "Name, CNIC, and mobile number are required"}), 400

        user = ChallanController.add_user(name, cnic, mobilenumber, email)
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

    ########################################  Violations  ############################################
# Route to get all violations with fines
@app.route('/violations', methods=['GET'])
def get_all_violations():
    try:
        violations = ChallanController.get_all_violations()
        return jsonify(violations)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/violationsbyid', methods=['GET'])
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

        if not name:
            return jsonify({"error": "Violation name is required"}), 400

        result = ChallanController.add_violation(name, description)
        return jsonify(result), 201
    except Exception as exp:
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

        result = ChallanController.update_violation(violation_id, new_name, new_description)
        return jsonify(result)
    except Exception as exp:
        return jsonify({'error': str(exp)}), 500

########################################  ViolationsFine  ############################################
# Route to add a fine to a violation
@app.route('/violationfine', methods=['POST'])
def add_violation_fine():
    try:
        data = request.get_json()
        violation_name=data.get('violation_name')
        created_date = datetime.today().strftime('%Y-%m-%d')
        fine = data.get('fine')

        if  not fine  or not violation_name:
            return jsonify({"error": "Violation_id and fine amount are required"}), 400

        result = ChallanController.add_violation_fine(violation_name, created_date, fine)
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


@app.route('/getviolationsrecord', methods=['GET'])
def get_violation_records():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id')
        date = data.get('date')
        camera_id = data.get('camera_id')
        result = ChallanController.get_violation_history_with_details(vehicle_id, date, camera_id)
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
        user_id = data.get('user_id')
        warden_id = data.get('warden_id')
        fine_amount = data.get('fine_amount')
        status = data.get('status')

        if not all([violation_history_id, violation_ids, user_id, warden_id, fine_amount, status]):
            return jsonify({"error": "Missing required fields"}), 400


        date =  datetime.now()  # Assuming you want to use the current UTC time for the date

        success, challan_id = ChallanController.add_challan_history_and_details(
            date, status, violation_ids, violation_history_id, user_id, warden_id, fine_amount
        )

        if success:
            return jsonify({"success": True, "challan_id": challan_id}), 201
        else:
            return jsonify({"error": "Failed to add challan record"}), 500

    except Exception as exp:
        return jsonify({'error': str(exp)}), 500


@app.route('/getchallans', methods=['GET'])
def retrieve_challans():
    try:
        data = request.json
        challan_id = data.get('challan_id')
        user_id = data.get('user_id')
        warden_id = data.get('warden_id')

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
UPLOAD_FOLDER = 'uploads'
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
            preprocessed_image=yolov8.preprocess_image(image)

            print("Preprocessed image shape:", preprocessed_image.shape)
            violations_and_plates = yolov8.detect_violations_from_Image(file_path, model_path ,model_pathr)

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
            model_path = r'C:\Drive D\Pycharm\TrafficGuardian\yolov8mtrafficmodel.pt'
            model_pathr= r'C:\Drive D\Pycharm\TrafficGuardian\yolov8s.pt'
            preprocessed_image=yolov8.preprocess_image(image)

            print("Preprocessed image shape:", preprocessed_image.shape)
            violations_and_plates = yolov8.detect_violations_from_Image(file_path, model_path ,model_pathr)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4321, debug=True)