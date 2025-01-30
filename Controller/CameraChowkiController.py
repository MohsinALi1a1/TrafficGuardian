from Model import Camera, Place, Direction, db, Chowki, CameraChowki, City


class CameraChowkiController:

    @staticmethod
    def get_all_camera(place_name ,direction_name):
        place = db.session.query(Place).filter(Place.name == place_name).first()
        if not place:
            return {"error": f"Specified Place {place_name} not exist"},404
        direction = db.session.query(Direction).filter(Direction.name == direction_name , Direction.place_id==place.id).first()
        if  not direction:
            return {"error": f"Specified Direction {direction_name} on Place {place_name} not exist "} ,404
        cameras = db.session.query(Camera).filter(Camera.direction_id == direction.id).all()
        return [{'id': camera.id, 'name': camera.name, 'place_name': place_name ,'direction' : direction.name ,'Type' : camera.type} for camera in cameras],200
    
    @staticmethod
    def get_camera_by_id(ID):
        camera = Camera.query.get(ID)
        if not camera:
            return {"error": "Invalid Camera ID "},409
        direction= Direction.query.get_or_404(camera.direction_id)
        if camera:
            return {'id': camera.id, 'name': camera.name, 'Camera Type': camera.type , "Direction" : direction.name},200
        else:
            return {"error": "Camera not found"},404


    @staticmethod
    def get_camera_by_name(camera_name):

        cameras = db.session.query(Camera).filter(Camera.name == camera_name).all()

        if cameras:
            direction_ids = {camera.direction_id for camera in cameras}
            directions = {direction.id: direction.name for direction in Direction.query.filter(Direction.id.in_(direction_ids)).all()}

            camera_info = [{ 'id': camera.id,'name': camera.name,'camera_type': camera.type,'direction': directions.get(camera.direction_id, "Unknown direction")}for camera in cameras]

            return camera_info, 200
        else:
            return {"error": "Camera not found"}, 404

    @staticmethod
    def add_camera(name, direction_name,camera_type):
        direction = db.session.query(Direction).filter(Direction.name == direction_name).first()
        if not direction:
            return {"error": f"Direction {direction_name} not found "}, 404
        if camera_type  == 'front' or camera_type  == 'side':
            new_camera = Camera(name=name, direction_id=direction.id,type=camera_type)
            db.session.add(new_camera)
            db.session.commit()
            return {'Sucessfully': f'camera {name} is Sucessfully install  on  Direction {direction_name}'},200
        else:
            return {"error": f"Camera type  {camera_type} is invalid "}, 409

    @staticmethod
    def delete_camera(camera_name, direction_name,camera_type):
        # Fetch the Camera  by name
        direction = db.session.query(Direction).filter(Direction.name == direction_name).first()
        if not direction:
            return {"error": f"Direction {direction_name} not found "}, 404
        if camera_type == 'front' or camera_type == 'side':
            camera= db.session.query(Camera).filter(Camera.name == camera_name,Camera.direction_id==direction.id , Camera.type==camera_type).first()
            if  not camera:
                return {"error": f"Camera not exsist in Direction {direction_name}  "}, 404
            db.session.delete(camera)
            db.session.commit()
            return {'Successfully': f'{camera_name} is successfully deleted'}, 201
        else:
            return {"error": f"Camera type  {camera_type} is invalid "}, 409
##################################################Chowki#############################################################################

    @staticmethod
    def get_all_Chowki(place_name):
        place = db.session.query(Place).filter(Place.name == place_name).first()

        if not place:
            return {"error": f"Specified Place {place_name} is Invalid "},409  # Return an empty list if the place doesn't exist
        chowkis = db.session.query(Chowki).filter(Chowki.place_id == place.id).all()
        if chowkis:
            return [{'id': chowki.id, 'name': chowki.name, 'place_name': place_name, } for chowki in chowkis],200
        else:
            return {"error": f"No Naka exist on Specified Place {place_name}"}, 404

    @staticmethod
    def get_chowki_by_id(ID):
        chowki = Chowki.query.get(ID)

        if chowki:
            return {'id': chowki.id, 'name': chowki.name, 'Place' : chowki.place_id },200
        else:
            return {"error": "Invalid Chowki ID "},409

    @staticmethod
    def get_chowki_by_name(chowki_name):
        chowki = db.session.query(Chowki).filter(Chowki.name == chowki_name).first()

        if chowki:
            place = db.session.query(Place).filter(Place.id == chowki.place_id).first()
            if not place:
                return {"error": " chowki Place is deleted "}, 404
            return {'id': chowki.id, 'name': chowki.name, 'Place ' : place.name  },200
        else:
            return {"error": " Chowki  not found"},404


    @staticmethod
    def add_chowki(name,place_name):
        place = db.session.query(Place).filter(Place.name == place_name).first()
        if not place:
            return {"error": f"Place {place_name} not found "}, 404

        new_chowki = Chowki(name=name, place_id=place.id)
        db.session.add(new_chowki)
        db.session.commit()
        return {'Sucessfully': f'Chowki {name} is Sucessfully added at Location {place_name}'},200

    @staticmethod
    def delete_chowki(name, place_name):
        # Fetch the Chowki  by name
        place= db.session.query(Place).filter(Place.name == place_name).first()
        if not place:
            return {"error": f"Place : {place_name} Is Not Valid"}, 404
        chowki = db.session.query(Chowki).filter(Chowki.name == name,Chowki.place_id==place.id).first()
        if  not chowki:
            return {"error": f"Chowki : {chowki} not exist at  Place : {place_name} "}, 404
        db.session.delete(chowki)
        db.session.commit()
        return {'Successfully': f'{chowki.name} is successfully deleted'}, 201
##########################################Warden Chowki###########################################################

    def get_all_Chowki_bycity(city_name):
        # Query the city to get its ID
        city = db.session.query(City).filter(City.name == city_name).first()
        if not city:
            return {'error':'Cityname  Is Invalid'},409


        # Query to get chowkis related to the city
        results = (
            db.session.query(
                City.name.label('city_name'),
                Place.name.label('place_name'),
                Chowki.id.label('chowki_id'),
                Chowki.name.label('chowki_name')
                # Add linked_cameras if it's a valid column or relationship
                # Chowki.linked_cameras.label('linked_cameras')
            )
            .select_from(City)  # Set the base entity for the query
            .join(Place, Place.city_id == City.id)  # Explicitly join Place
            .join(Chowki, Chowki.place_id == Place.id)  # Explicitly join Chowki
            .filter(City.id == city.id)  # Use city.id instead of city_name
            .group_by(City.name, Place.name, Chowki.id, Chowki.name)
            .all()
        )

        # Process results and create a list of dictionaries
        result_list = []
        for row in results:
            result_list.append({
                'city_name': row.city_name,
                'place_name': row.place_name,
                'chowki_id': row.chowki_id,
                'chowki_name': row.chowki_name,
                # Include linked_cameras if added in the query
                # 'linked_cameras': row.linked_cameras
            })

        return result_list,200

    ##################################################CameraChowki#############################################################################

    @staticmethod
    def get_all_ChowkiCamera_byplace(place_name):
        place = db.session.query(Place).filter(Place.name == place_name).first()
        if  not place:
            return {'error':'Place is Invlaid'},409

        results = (
            db.session.query(
                City.name.label('city_name'),
                Place.name.label('place_name'),
                Chowki.id.label('chowki_id'),
                Chowki.name.label('chowki_name'),
                db.func.group_concat(db.func.concat( Camera.name, ' (', Camera.type, ')   ||   ')).label(
                    'linked_cameras')
            )
            .join(Place, Place.city_id == City.id)
            .join(Chowki, Chowki.place_id == Place.id)
            .join(CameraChowki, CameraChowki.chowki_id == Chowki.id)
            .join(Camera, Camera.id == CameraChowki.camera_id)
            .group_by(City.name, Place.name, Chowki.id, Chowki.name)
            .filter(Place.name == place_name)
            .all()
        )

        # Process results and create a list of dictionaries
        result_list = []
        for row in results:
            city_name = row.city_name
            place_name = row.place_name
            chowki_name = row.chowki_name
            linked_cameras = row.linked_cameras


            result_list.append({
                'city_name': city_name,
                'place_name': place_name,
                'chowki_name': chowki_name,
                'linked_cameras': linked_cameras
            })
        return result_list,200

    @staticmethod
    def get_all_ChowkiCamera_bycity(city_name):
        city = db.session.query(City).filter(City.name == city_name).first()
        if not city:
            return {'error':'City name is Invalid'},409

        results = (
            db.session.query(
                City.name.label('city_name'),
                Place.name.label('place_name'),
                Chowki.id.label('chowki_id'),
                Chowki.name.label('chowki_name'),
                db.func.group_concat(db.func.concat( Camera.name, ' (', Camera.type, ')   ||   ')).label(
                    'linked_cameras')
            )
            .join(Place, Place.city_id == City.id)
            .join(Chowki, Chowki.place_id == Place.id)
            .join(CameraChowki, CameraChowki.chowki_id == Chowki.id)
            .join(Camera, Camera.id == CameraChowki.camera_id)
            .group_by(City.name, Place.name, Chowki.id, Chowki.name)
            .filter(City.name == city_name)
            .all()
        )

        # Process results and create a list of dictionaries
        result_list = []
        for row in results:
            city_name = row.city_name
            place_name = row.place_name
            chowki_name = row.chowki_name
            linked_cameras = row.linked_cameras


            result_list.append({
                'city_name': city_name,
                'place_name': place_name,
                'chowki_name': chowki_name,
                'linked_cameras': linked_cameras
            })
        return result_list,200



    @staticmethod
    def get_all_linkCamera_with_Chowki(chowki_name):

        chowki = db.session.query(Chowki).filter(Chowki.name == chowki_name).first()
        if not chowki:
            return {'error':'Chowki Not found '},404

        results = (
            db.session.query(
                Place.name.label('place_name'),
                Chowki.id.label('chowki_id'),
                Chowki.name.label('chowki_name'),
                Camera.name.label('camera_name'),
                Camera.type.label('camera_type'),
            )
            .join(Chowki, Chowki.place_id == Place.id)
            .join(CameraChowki, CameraChowki.chowki_id == Chowki.id)
            .join(Camera, Camera.id == CameraChowki.camera_id)
            .filter(Chowki.name == chowki_name)
            .all()
        )

        result_list = []
        for row in results:
            result_list.append({
                'place_name': row.place_name,
                'chowki_name': row.chowki_name,
                'camera_name': row.camera_name,
                'camera_type': row.camera_type
            })

        return result_list,200

    @staticmethod
    def get_all_linkChowki_with_Camera(camera_name):

        camera = db.session.query(Camera).filter(Camera.name == camera_name).first()
        if not camera:
            return {'error':f'Camera {camera_name}is not Found '},404

        results = (
            db.session.query(
                Place.name.label('place_name'),
                Chowki.id.label('chowki_id'),
                Chowki.name.label('chowki_name'),
                Camera.name.label('camera_name'),
                Camera.type.label('camera_type'),
            )
            .join(Chowki, Chowki.place_id == Place.id)
            .join(CameraChowki, CameraChowki.chowki_id == Chowki.id)
            .join(Camera, Camera.id == CameraChowki.camera_id)
            .filter(Camera.name == camera_name)
            .all()
        )

        result_list = []
        for row in results:
            result_list.append({
                'place_name': row.place_name,
                'chowki_name': row.chowki_name,
                'camera_name': row.camera_name,
                'camera_type': row.camera_type
            })

        return result_list,200


    def link_camera_to_chowki(chowki_name, camera_list):

        chowki = db.session.query(Chowki).filter(Chowki.name == chowki_name).first()

        if not chowki:
            return f"Chowki '{chowki_name}' not found.",404

        linked_cameras = []
        not_found_cameras = []

        for camera_name in camera_list:
            # Get cameras by name
            cameras = db.session.query(Camera).filter(Camera.name == camera_name).all()

            if not cameras:
                not_found_cameras.append(camera_name)
                continue  # Skip to the next camera name

            for cam in cameras:
                camera_chowki = CameraChowki(camera_id=cam.id, chowki_id=chowki.id)
                db.session.add(camera_chowki)
                linked_cameras.append(cam.name)

        db.session.commit()

        if not_found_cameras:
            return (f"Successfully linked cameras {linked_cameras} to chowki '{chowki_name}'. "
                    f"However, the following cameras were not found: {not_found_cameras}.") ,201

        return f"Successfully linked cameras {linked_cameras} to chowki '{chowki_name}'." ,201




    def unlink_camera_from_chowki(chowki_name, camera_list):

        chowki = db.session.query(Chowki).filter(Chowki.name == chowki_name).first()

        if not chowki:
            return f"Chowki '{chowki_name}' not found.",404

        unlinked_cameras = []
        not_found_cameras = []

        for camera_name in camera_list:

            cameras = db.session.query(Camera).filter(Camera.name == camera_name).all()

            if not cameras:
                not_found_cameras.append(camera_name)
                continue

            for cam in cameras:

                camera_chowki = (
                    db.session.query(CameraChowki)
                    .filter(CameraChowki.camera_id == cam.id, CameraChowki.chowki_id == chowki.id)
                    .first()
                )
                if camera_chowki:
                    db.session.delete(camera_chowki)  # Remove the link
                    unlinked_cameras.append(cam.name)  # Append the actual camera name


        db.session.commit()


        if not_found_cameras:
            return (f"Successfully unlinked cameras {unlinked_cameras} from chowki '{chowki_name}'. "
                    f"However, the following cameras were not found: {not_found_cameras}."),201

        return f"Successfully unlinked cameras {unlinked_cameras} from chowki '{chowki_name}'.",201





    def update_linked_cameras_with_chowki(chowki_name, cameras_to_link, cameras_to_unlink):
        chowki = db.session.query(Chowki).filter(Chowki.name == chowki_name).first()

        if not chowki:
            return f"Chowki '{chowki_name}' not found." ,404

        # Unlink cameras from the chowki
        unlinked_cameras = []
        not_found_cameras = []

        for camera_name in cameras_to_unlink:
            cameras = db.session.query(Camera).filter(Camera.name == camera_name).all()

            if not cameras:
                not_found_cameras.append(camera_name)
                continue

            for camera in cameras:
                # Find the CameraChowki entry to unlink
                camera_chowki = (
                    db.session.query(CameraChowki)
                    .filter(CameraChowki.camera_id == camera.id, CameraChowki.chowki_id == chowki.id)
                    .first()
                )

                if camera_chowki:
                    db.session.delete(camera_chowki)  # Remove the link
                    unlinked_cameras.append(camera_name)

        # Link new cameras to the chowki
        linked_cameras = []

        for camera_name in cameras_to_link:
            cameras = db.session.query(Camera).filter(Camera.name == camera_name).all()  # Use .all()

            if not cameras:
                not_found_cameras.append(camera_name)
                continue  # Skip to the next camera name

            for camera in cameras:
                # Check if already linked to avoid duplicates
                existing_link = (
                    db.session.query(CameraChowki)
                    .filter(CameraChowki.camera_id == camera.id, CameraChowki.chowki_id == chowki.id)
                    .first()
                )

                if not existing_link:
                    new_camera_chowki = CameraChowki(camera_id=camera.id, chowki_id=chowki.id)
                    db.session.add(new_camera_chowki)
                    linked_cameras.append(camera_name)


        db.session.commit()
        response = []

        if unlinked_cameras:
            response.append(f"Successfully unlinked cameras: {', '.join(set(unlinked_cameras))}")

        if linked_cameras:
            response.append(f"Successfully linked cameras: {', '.join(set(linked_cameras))}")

        if not_found_cameras:
            response.append(f"The following cameras were not found: {', '.join(set(not_found_cameras))}")

        return " ".join(response) if response else "No changes made." , 200


