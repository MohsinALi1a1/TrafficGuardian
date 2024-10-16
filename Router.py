from datetime import datetime

from Model.Configure import app
from flask import  request ,jsonify
from Controller import LocationController, ChallanController
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

@app.route('/wardentbycnic', methods=['GET'])
def get_warden_by_cnic():
    try:
        data = request.get_json()
        warden_cnic = data.get('cnic')
        warden = WardenChowkiController.get_warden_by_cnic(warden_cnic)
        return jsonify(warden)
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
        new_warden = WardenChowkiController.add_warden(name, badge_number, address, cnic, email, mobile_number, city_name)
        return jsonify(new_warden), 201
    except Exception as exp:
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
########################################  WardenChowki  ############################################

@app.route('/wardenassignments', methods=['POST'])
def warden_assignments():
    try:
        Duty=WardenChowkiController.create_duty_roster()
        return jsonify({"sucessfully":Duty})
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
        badge_number = data.get('badgenumber')
        dutyroster_list = WardenChowkiController.get_dutyroster_for_warden(badge_number)
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

#########################################################################################################################################



if __name__ == "__main__":
    app.run()