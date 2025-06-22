from sqlalchemy import desc

import Controller
from Controller import CameraChowkiController, OCR, ImageControllerAndNotification
from Model import User, Vehicle, db, Violation, ViolationFine, ViolationHistory, ViolationDetails, Challan, \
    ChallanViolations, ViolationImages, NakaGraph
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import cv2
import io
import os
from PIL import Image
from Model.Configure import app
from flask import  request ,jsonify
import re

from Model.Notification import Notification


class ChallanController:
    #################################  Vehicle ########################################################
    @staticmethod
    def get_all_vehicles():
        vehicles = Vehicle.query.all()
        return [{'id': vehicle.id, 'licenseplate': vehicle.licenseplate, 'vehicletype': vehicle.vehicletype} for vehicle in vehicles]

    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        vehicle = Vehicle.query.get_or_404(vehicle_id)
        return {'id': vehicle.id, 'licenseplate': vehicle.licenseplate, 'vehicletype': vehicle.vehicletype}

    @staticmethod
    def get_vehicle_by_licenseplate(licenseplate):
        vehicle = db.session.query(Vehicle).filter(Vehicle.licenseplate == licenseplate).first()
        if vehicle:
            return {'id': vehicle.id, 'licenseplate': vehicle.licenseplate, 'vehicletype': vehicle.vehicletype}
        else:
            return {"error": "Vehicle not found"}

    @staticmethod
    def add_vehicle(licenseplate, vehicletype):
        existing_vehicle = db.session.query(Vehicle).filter(Vehicle.licenseplate == licenseplate).first()
        if existing_vehicle:
            return {"error": "Vehicle already exists"}, 409
        new_vehicle = Vehicle(licenseplate=licenseplate, vehicletype=vehicletype)
        db.session.add(new_vehicle)
        db.session.commit()
        return {'Successfully': f'Vehicle with license plate {new_vehicle.licenseplate} is successfully added'}

    @staticmethod
    def delete_vehicle(licenseplate):
        vehicle = db.session.query(Vehicle).filter(Vehicle.licenseplate == licenseplate).first()
        if not vehicle:
            return {"error": "Vehicle not found"}, 404

        db.session.delete(vehicle)
        db.session.commit()
        return {'Successfully': f'Vehicle with license plate {vehicle.licenseplate} is successfully deleted'}, 201

    @staticmethod
    def update_vehicle(licenseplate, new_licenseplate, new_vehicletype="Bike"):
        vehicle = db.session.query(Vehicle).filter(Vehicle.licenseplate == licenseplate).first()

        if not vehicle:
            return {"error": "Vehicle not found"}, 404

        vehicle.licenseplate = new_licenseplate
        vehicle.vehicletype = new_vehicletype
        db.session.commit()
        return {"message": f"Vehicle updated to license plate {new_licenseplate} and type {new_vehicletype}"}, 201

    #################################  User ########################################################

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [{'id': user.id, 'name': user.name, 'cnic': user.cnic,
                 'mobilenumber': user.mobilenumber, 'email': user.email} for user in users]

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'name': user.name, 'cnic': user.cnic,
                'mobilenumber': user.mobilenumber, 'email': user.email}

    @staticmethod
    def get_user_by_cnic(cnic):
        user = db.session.query(User).filter(User.cnic == cnic).first()
        if user:
            return {'id': user.id, 'name': user.name, 'cnic': user.cnic,
                    'mobilenumber': user.mobilenumber, 'email': user.email}
        else:
            return {"error": "User not found"}

    @staticmethod
    def add_user(name, cnic, mobilenumber, email):
        existing_user = db.session.query(User).filter(User.cnic == cnic).first()
        if existing_user:
            return {"error": "User already exists"}, 409
        new_user = User(name=name, cnic=cnic, mobilenumber=mobilenumber, email=email)
        db.session.add(new_user)
        db.session.commit()
        return {'Successfully': f'User {new_user.name} is successfully added'}

    @staticmethod
    def delete_user(cnic):
        user = db.session.query(User).filter(User.cnic == cnic).first()
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {'Successfully': f'User {user.name} is successfully deleted'}, 201

    @staticmethod
    def update_user(cnic, new_name=None, new_mobilenumber=None, new_email=None):
        user = db.session.query(User).filter(User.cnic == cnic).first()

        if not user:
            return {"error": "User not found"}, 404

        if new_name:
            user.name = new_name
        if new_mobilenumber:
            user.mobilenumber = new_mobilenumber
        if new_email:
            user.email = new_email

        db.session.commit()
        return {"message": f"User {user.name} updated successfully"}, 201

    @staticmethod
    def userlogincheck(cnic, password):
        # Search for the warden using the badge number
        user = User.query.filter_by(cnic=cnic).first()

        # If warden not found
        if not user:
            return {"message": "Cnic number or password does not match"}, 401

        # If passwords are hashed, use this:
        # if not check_password_hash(warden.password, password):

        # If passwords are stored as plain text (not recommended), use this:
        if user.password != password:
            return {"message": "Badge number or password does not match"}, 401

        # Login successful - return relevant data
        return {
            "userid": user.id,

        }, 200
    #################################  Violations & Fine ########################################################

    @staticmethod
    def get_all_violations():
        violations = Violation.query.all()
        return [{
            'id': violation.id,
            'name': violation.name,
            'description': violation.description,
            'limitValue': violation.limit_value,
            'status': violation.status,
            'start_date': violation.start_date.isoformat() if violation.start_date else None,
            'end_date': violation.end_date.isoformat() if violation.end_date else None,
            'fines': [
                {
                    'id': fine.id,
                    'created_date': fine.created_date,
                    'violation_id': violation.id,
                    'active': fine.active,
                    'fine': float(fine.fine)
                }
                for fine in violation.violation_fines if fine.active == 1
            ]
        } for violation in violations]

    @staticmethod
    def get_violation_by_id(violation_id):
        violation = Violation.query.get_or_404(violation_id)
        return {
            'id': violation.id,
            'name': violation.name,
            'description': violation.description,
            'limitValue': violation.limit_value,
            'status': violation.status,
            'start_date': violation.start_date.isoformat() if violation.start_date else None,
            'end_date': violation.end_date.isoformat() if violation.end_date else None,
            'fines': [{'id': fine.id, 'created_date': fine.created_date,'violation_id':violation.id,'active':fine.active, 'fine': float(fine.fine)} for fine in
                      violation.violation_fines if fine.active == 1]

        }

    @staticmethod
    def get_violation_by_name(violation_name):
        violation = Violation.query.filter_by(name=violation_name).first_or_404()
        return {
            'id': violation.id,
            'name': violation.name,
            'description': violation.description,
            'limitValue': violation.limit_value,
            'status': violation.status,
            'start_date': violation.start_date.isoformat() if violation.start_date else None,
            'end_date': violation.end_date.isoformat() if violation.end_date else None,
            'fines': [
                {
                    'id': fine.id,
                    'created_date': fine.created_date,
                    'violation_id': violation.id,
                    'active': fine.active,
                    'fine': float(fine.fine)
                }
                for fine in violation.violation_fines if fine.active == 1
            ]
        }

    @staticmethod
    def add_violation(name, fine,description=None ,limitValue=-1 ):
        existing_violation = db.session.query(Violation).filter(Violation.name == name).first()
        if existing_violation:
            return {"error": "Violation already exists"}, 409
        new_violation = Violation(name=name, description=description ,limit_value=limitValue)
        db.session.add(new_violation)
        db.session.commit()
        created_date = datetime.today().strftime('%Y-%m-%d')
        ChallanController.add_violation_fine(new_violation.id ,created_date,fine)
        return {'Successfully': f'Violation {new_violation.name} is successfully added'}

    @staticmethod
    def delete_violation(violation_name):
        violation = db.session.query(Violation).filter(Violation.name == violation_name).first()
        if not violation:
            return {"error": "Violation not found"}, 404

        db.session.delete(violation)
        db.session.commit()
        return {'Successfully': f'Violation {violation.name} is successfully deleted'}, 201



    @staticmethod
    def update_violation(violation_id, new_name=None, new_description=None, limit_value=None,
                         fine=None, start_date=None, end_date=None):
        violation = db.session.query(Violation).get(violation_id)

        if not violation:
            return {"error": "Violation not found"}, 404

        # Update basic violation details if provided
        if new_name and violation.name != new_name:
            violation.name = new_name
        if new_description and violation.description != new_description:
            violation.description = new_description
        if limit_value is not None and violation.limit_value != limit_value:
            violation.limit_value = limit_value
            violation.start_date=None
            violation.end_date=None
        if start_date is not None:
            violation.start_date = start_date
        if end_date is not None:
            violation.end_date = end_date

        db.session.commit()  # Commit violation updates first

        if fine:
            # First, change the status of the old fine
            status, code = ChallanController.update_violation_status(violation.id)

            if code == 201:
                # Once the old fine status is updated, add the new fine
                created_date = datetime.today().strftime('%Y-%m-%d')
                ChallanController.add_violation_fine(violation.id, created_date, fine)

        return {"message": "Violation updated successfully"}, 200

    @staticmethod
    def update_violations_status(violation_id,Status):
        violation = db.session.query(Violation).get(violation_id)

        if not violation:
            return {"error": "Violation not found"}, 404

        # Update basic violation details if provided
        if Status and violation.status != Status:
            violation.status = Status


        db.session.commit()  # Commit violation updates first


        return {"message": "Violation updated successfully"}, 200

    @staticmethod
    def add_violation_fine(violation_id, created_date, fine):
        violation = db.session.query(Violation).filter(Violation.id == violation_id).first()
        if not violation:
            return {"error": "Violation not found"}, 404
        new_fine = ViolationFine(violation_id=violation.id, created_date=created_date, fine=fine ,active=1)
        db.session.add(new_fine)
        db.session.flush()  # Ensures the object is registered before committing
        db.session.commit()
        return {'Successfully': f'Fine of {fine} added to violation {violation.name}'}

    @staticmethod
    def update_violation_status(violation_id):
        fines = db.session.query(ViolationFine).filter(
            ViolationFine.violation_id == violation_id and
            ViolationFine.active == 1
        ).all()

        if not fines:
            return {"error": "No active fines found"}, 404

        for fine in fines:
            fine.active = 0

        db.session.commit()
        return {'message': f'{len(fines)} fine(s) deactivated successfully'}, 201

    @staticmethod
    def delete_violation_fine(fine_id):
        fine = db.session.query(ViolationFine).get(fine_id)
        if not fine:
            return {"error": "Fine not found"}, 404

        db.session.delete(fine)
        db.session.commit()
        return {'Successfully': f'Fine {fine.id} deleted successfully'}, 201

    @staticmethod
    def get_violation_fine(violation_id):
        fine = db.session.query(ViolationFine).filter(
            (ViolationFine.violation_id == violation_id) & (ViolationFine.active == 1)
        ).first()

        if not fine:
            return {"error": "Fine not found"}, 404

        return {'fine': fine.fine}, 201

    #################################  ViolationsHistory & Its Details ########################################################
    @staticmethod
    def update_violation_history_status(violation_history_id,status):
        try:
            violation_history = db.session.query(ViolationHistory).filter(ViolationHistory.id==violation_history_id).first()
            print(violation_history_id)
            if not violation_history:
                print("ViolationHistory _id not found for status update")
                return {"error": "ViolationHistory not found"}, 404

            violation_history.status = status
            db.session.commit()

            return {"message": "ViolationHistory status updated to 'Issue'"}, 200
            print("ViolationHistory _id  found  status updated sucessfully")
        except Exception as e:
            print(f"ViolationHistory   status exception {str(e)}")
            db.session.rollback()
            return {"error": f"Failed to update status: {str(e)}"}, 500

    @staticmethod
    def add_violation_history_and_details(vehicle_id,  location, status, camera_id, violation_ids,image_list,bikenumber=None):
        try:
            # Validate inputs here if necessary

            violation_history = ViolationHistory(
                vehicle_id=vehicle_id,
                location=location,
                status=status,
                camera_id=camera_id
            )

            db.session.add(violation_history)
            db.session.flush()

            for violation_id in violation_ids:
                violation_detail = ViolationDetails(
                    violation_history_id=violation_history.id,
                    violation_id=violation_id
                )
                db.session.add(violation_detail)

            db.session.commit()

            print("Violation history and details added successfully.")
            save_imag_path_list= ChallanController.save_images(image_list,violation_history.id)
            for path in save_imag_path_list:
                violation_images = ViolationImages(
                    violation_id=violation_history.id,
                    image_path=path
                )
                db.session.add(violation_images)

            db.session.commit()

            # Get on-duty wardens for the camera
            wardens = CameraChowkiController.get_on_duty_wardens(camera_id)

            # Check if any wardens were found
            if not wardens:
                print(f"No on-duty wardens found for camera_id={camera_id}")
            else:
                for warden in wardens:
                    response =Controller.ImageControllerAndNotification.add_notification(
                        recipient_type="TrafficWarden",
                        recipient_id=warden.id,
                        type_="Violation Alert",
                        message=f"🚨 Vehicle {bikenumber} has committed a violation in your assigned area: {location}. Please review and take action.",
                        violation_id=violation_history.id
                    )
                    print(f"🔔 Notification sent to Warden ID: {warden.id}")

            return {
                "successfully": "Violation history and details added successfully",
                "violation_history_id": violation_history.id
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            return {
                "error": "Failed to add violation history and details",
                "details": str(e)
            }, 500

    @staticmethod
    def get_custom_hops_naka_of_naka(naka_ids_list, bike, location, maxhops , link_id):
        visited_nakas = set(naka_ids_list)  # To avoid duplicates
        current_level = set(naka_ids_list)  # Nakas to explore at this hop

        for _ in range(maxhops):
            if not current_level:
                break

            # Query all to_naka where from_naka is in current level
            next_level_records = db.session.query(NakaGraph.ToNakaID).filter(
                NakaGraph.FromNakaID.in_(current_level)
            ).all()

            next_level_nakas = set()
            for record in next_level_records:
                to_naka_id = record[0]  # unpack from tuple
                if to_naka_id not in visited_nakas:
                    next_level_nakas.add(to_naka_id)

            visited_nakas.update(next_level_nakas)
            current_level = next_level_nakas  # move to next level

        # Exclude the original starting naka ids
        naka_list = list(visited_nakas - set(naka_ids_list))

        print("📌 Linked naka(s) found (excluding starting nakas):", naka_list)

        # Send notifications for these linked nakas
        ChallanController.send_notification_to_linknaka(naka_list, bike, location,link_id)
        ChallanController.update_violation_history_status(link_id, "Runner")
        return naka_list

    @staticmethod
    def send_notification_to_linknaka(naka_ids_list, bikenumber, location ,link_id):
        try:
            for naka_id in naka_ids_list:
                print(f"📡 Processing Naka ID: {naka_id} for violation alert...")  # 👈 Added print here

                try:
                    # Get on-duty wardens for the current naka
                    wardens = CameraChowkiController.get_on_duty_wardens_of_naka([naka_id])

                    if not wardens:
                        print(f"⚠️ No on-duty wardens found at Naka ID: {naka_id}")
                    else:
                        for warden in wardens:
                            try:
                                response = Controller.ImageControllerAndNotification.add_notification(
                                    recipient_type="TrafficWarden",
                                    recipient_id=warden.id,
                                    type_="Violation Alert",
                                    message=(
                                        f"🚨 Vehicle {bikenumber} ran from {location} "
                                        f"and is coming to your assigned area (Naka ID: {naka_id}). "
                                        "Be ready to stop it."

                                    ),
                                    violation_id=link_id
                                )
                                print(f"🔔 Notification sent to Warden ID: {warden.id} (Naka ID: {naka_id})")
                            except Exception as e:
                                print(
                                    f"❌ Failed to send notification to Warden ID {warden.id} at Naka ID {naka_id}: {e}")
                except Exception as inner_e:
                    print(f"❌ Error retrieving wardens for Naka ID {naka_id}: {inner_e}")

        except Exception as e:
            print(f"🔥 Error in sending notifications to Link Naka list: {e}")

    @staticmethod
    def save_images(image_list, violation_id, base_name="bike"):
        # Create folder like Predictions/saved_images1 (if violation_id is 1)
        save_folder = os.path.join("Predictions", f"saved_images{violation_id}")
        os.makedirs(save_folder, exist_ok=True)

        saved_paths = []

        for idx, image in enumerate(image_list, start=1):
            # Generate file name
            filename = f"{violation_id}_{base_name}_{idx}.jpg"

            # Full save path
            save_path = os.path.join(save_folder, filename)

            # Save the image
            image.save(save_path)

            # Get only the path from 'saved_imagesX/filename.jpg'
            relative_path = os.path.relpath(save_path, start="Predictions")
            clean_path = relative_path.replace("\\", "/")

            # Append to saved paths list
            saved_paths.append(clean_path)

        return saved_paths
# this function Get violation history w.r.t to connect naka bottom function is also same but it will work on notification
    # @staticmethod
    # def get_violation_history_with_details(naka_id,vehicle_id=None, date=None ):
    #     try:
    #         cameras_ids=[]
    #         query = (
    #             db.session.query(ViolationHistory)
    #             .join(ViolationDetails)
    #         )
    #
    #
    #         if(naka_id):
    #            camera_list= CameraChowkiController.get_all_linkCamera_with_Chowkibyid(naka_id)
    #            if camera_list is not None and len(camera_list) > 0:
    #                # Loop through the camera_list and populate the data
    #                for camera in camera_list:
    #                    cameras_ids.append(camera['camera_id'])
    #                if vehicle_id:
    #                    query = query.filter(ViolationHistory.vehicle_id == vehicle_id)
    #                if date:
    #                    query = query.filter(ViolationHistory.date == date)
    #                if cameras_ids:
    #                    query = query.filter(ViolationHistory.camera_id.in_(cameras_ids))
    #                    violation_histories = query.all()
    #
    #            else:
    #                violation_histories = []
    #                print("No cameras found for this naka_id.")
    #
    #
    #
    #         if not violation_histories:
    #             return {"message": "No violation records found."}
    #
    #         result = []
    #         for history in violation_histories:
    #             violation_details = [
    #                 {
    #                     "violation_name": db.session.query(Violation.name).filter(Violation.id==detail.violation_id).scalar()
    #
    #                 }
    #                 for detail in history.violation_details
    #             ]
    #
    #             vehicle= ChallanController.get_vehicle_by_id(history.vehicle_id)
    #
    #             result.append({
    #                 "id": history.id,
    #                 "vehicle_id": history.vehicle_id,
    #                 "licenseplate":vehicle['licenseplate'],
    #                 "vehicletype":vehicle['vehicletype'],
    #                 "violation_datetime": history.violation_datetime,
    #                 "location": history.location,
    #                 "status": history.status,
    #                 "camera_id": history.camera_id,
    #                 "violation_details": violation_details
    #             })
    #
    #         return {
    #             "violation_histories": result
    #         }
    #
    #     except SQLAlchemyError as e:
    #         print(f"Error occurred: {e}")
    #         return {
    #             "error": "Failed to retrieve violation history with details",
    #             "details": str(e)
    #         }

    #this Function i create if notification receive then violation details are shown
    @staticmethod
    def get_violation_history_with_details(naka_id=None, vehicle_id=None, date=None, warden_id=None):
        try:
            cameras_ids = []
            violation_histories = []

            # Case 1: If warden_id is provided
            if warden_id:
                # Get all violation_history_ids where recipient is the warden
                notification_query = (
                    db.session.query(Notification.link_id)
                    .filter(Notification.recipient_id == warden_id)
                    .filter(Notification.recipient_type == 'TrafficWarden')
                )
                violation_ids = [row[0] for row in notification_query.all()]

                if not violation_ids:
                    return {"message": "No violation notifications found for this warden."}

                # Fetch full violation history records
                query = (
                    db.session.query(ViolationHistory)
                    .join(ViolationDetails)
                    .filter(ViolationHistory.id.in_(violation_ids))
                )

                violation_histories = query.order_by(desc(ViolationHistory.id)).all()

            # Case 2: If naka_id is provided (existing logic)
            elif naka_id:
                camera_list = CameraChowkiController.get_all_linkCamera_with_Chowkibyid(naka_id)

                if camera_list is not None and len(camera_list) > 0:
                    for camera in camera_list:
                        cameras_ids.append(camera['camera_id'])

                    query = (
                        db.session.query(ViolationHistory)
                        .join(ViolationDetails)
                    )

                    if vehicle_id:
                        query = query.filter(ViolationHistory.vehicle_id == vehicle_id)
                    if date:
                        query = query.filter(ViolationHistory.date == date)
                    if cameras_ids:
                        query = query.filter(ViolationHistory.camera_id.in_(cameras_ids))

                    violation_histories = query.order_by(desc(ViolationHistory.id)).all()
                else:
                    print("No cameras found for this naka_id.")
                    violation_histories = []

            if not violation_histories:
                return {"message": "No violation records found."}

            result = []
            for history in violation_histories:
                violation_details = [
                    {
                        "violation_name": db.session.query(Violation.name)
                        .filter(Violation.id == detail.violation_id)
                        .scalar()
                    }
                    for detail in history.violation_details
                ]

                vehicle = ChallanController.get_vehicle_by_id(history.vehicle_id)

                result.append({
                    "id": history.id,
                    "vehicle_id": history.vehicle_id,
                    "licenseplate": vehicle['licenseplate'],
                    "vehicletype": vehicle['vehicletype'],
                    "violation_datetime": history.violation_datetime,
                    "location": history.location,
                    "status": history.status,
                    "camera_id": history.camera_id,
                    "violation_details": violation_details
                })

            return {
                "violation_histories": result
            }

        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            return {
                "error": "Failed to retrieve violation history with details",
                "details": str(e)
            }

    @staticmethod
    def update_violation_history(vehicle_id=None, date=None, camera_id=None, updates=None):
        # Update is a dict
        try:

            query = (
                db.session.query(ViolationHistory)
                .join(ViolationDetails)
            )

            if vehicle_id:
                query = query.filter(ViolationHistory.vehicle_id == vehicle_id)
            if date:
                query = query.filter(ViolationHistory.date == date)
            if camera_id:
                query = query.filter(ViolationHistory.camera_id == camera_id)

            violation_histories = query.all()

            if not violation_histories:
                return {"message": "No violation records found."}
            if updates:
                for history in violation_histories:
                    if 'location' in updates:
                        history.location = updates['location']
                    if 'status' in updates:
                        history.status = updates['status']
                    if 'imagepath' in updates:
                        history.imagepath = updates['imagepath']
                    if 'camera_id' in updates:
                        history.camera_id = updates['camera_id']

                    # Add any other fields you want to update here

                db.session.commit()

            return {
                "message": "Violation records updated successfully",
                "updated_records": [
                    {
                        "id": history.id,
                        "vehicle_id": history.vehicle_id,
                        "date": history.date,
                        "location": history.location,
                        "status": history.status,
                        "imagepath": history.imagepath,
                        "camera_id": history.camera_id,
                    }
                    for history in violation_histories
                ]
            }

        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            return {
                "error": "Failed to update violation history",
                "details": str(e)
            }

    @staticmethod
    def delete_violation_history(vehicle_id=None, date=None, camera_id=None):
        try:
            # Query for the ViolationHistory records
            query = db.session.query(ViolationHistory).outerjoin(ViolationDetails)
            print(camera_id)
            print(query)
            if vehicle_id:
                print("vehicle")
                query = query.filter(ViolationHistory.vehicle_id == vehicle_id)
            if date:
                print("date")
                query = query.filter(ViolationHistory.date == date)
            if camera_id:
                print("camera")
                query = query.filter(ViolationHistory.camera_id == camera_id)

            violation_histories = query.all()
            print(violation_histories)
            if not violation_histories:
                return {"message": "No violation records found."}

            # Delete associated ViolationDetails first
            for history in violation_histories:
                for detail in history.violation_details:
                    db.session.delete(detail)  # Delete each ViolationDetail

                db.session.delete(history)  # Delete the ViolationHistory record

            db.session.commit()  # Commit the changes to the database

            return {
                "message": "Violation records deleted successfully"
            }

        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            return {
                "error": "Failed to delete violation history",
                "details": str(e)
            }


#################################  Challan & Its Details ########################################################
    @staticmethod
    def add_challan_history_and_details(date, status, violation_ids, violation_history_id,
                                        violator_cnic,violator_name,mobile_number,vehicle_number, warden_id, fine_amount):
        try:
            new_challan = Challan(
                violation_history_id=violation_history_id,
                violator_cnic=violator_cnic,
                violator_name=violator_name,
                mobile_number=mobile_number,
                vehicle_number=vehicle_number,
                warden_id=warden_id,
                challan_date=date,
                fine_amount=fine_amount,
                status=status
            )

            db.session.add(new_challan)
            db.session.flush()  # Flush to get the new challan ID before committing

            for violation_id in violation_ids:
               fine,code= ChallanController.get_violation_fine(violation_id)
               if code==201:
                    new_challan_violation = ChallanViolations(
                        challan_id=new_challan.id,
                        violation_id=violation_id,
                        fine=fine['fine']
                    )
                    db.session.add(new_challan_violation)

            db.session.commit()
            ChallanController.update_violation_history_status(violation_history_id,"Issue")
            return True, new_challan.id

        except Exception as exp:
            db.session.rollback()
            print(f"Error while adding challan: {exp}")
            return False, None  # Return failure and no ID

    @staticmethod
    def get_challans(challan_id=None, violator_cnic=None, warden_id=None):
        try:
            query = db.session.query(Challan)

            if challan_id:
                challan = query.filter_by(id=challan_id).first()
                if challan is None:
                    return False, "Challan not found"

                challan_details = db.session.query(ChallanViolations).filter(
                    ChallanViolations.challan_id == challan.id).all()

                violation_list = []

                for detail in challan_details:
                    violation = ChallanController.get_violation_by_id(detail.violation_id)
                    if violation and violation['fines']:
                        active_fine = violation['fines'][0]['fine']
                        violation_list.append({
                            "violation": violation['name'],
                            "fine": active_fine
                        })

                return True, {
                    "challan": {
                        "id": challan.id,
                        "violation_history_id": challan.violation_history_id,
                        "violator_name": challan.violator_name,
                        "violator_cnic": challan.violator_cnic,
                        "mobile_number": challan.mobile_number,
                        "vehicle_number": challan.vehicle_number,
                        "warden_id": challan.warden_id,
                        "challan_date": challan.challan_date,
                        "fine_amount": challan.fine_amount,
                        "status": challan.status,
                        "violation_details": violation_list
                    }
                }

            # Filter by CNIC and/or WardenID if provided
            if violator_cnic:
                query = query.filter_by(violator_cnic=violator_cnic)
            if warden_id:
                query = query.filter_by(warden_id=warden_id)

            challans = query.all()
            result = []

            for challan in challans:
                challan_details = db.session.query(ChallanViolations).filter(
                    ChallanViolations.challan_id == challan.id).all()

                violation_list = []

                for detail in challan_details:
                    violation = ChallanController.get_violation_by_id(detail.violation_id)
                    if violation and violation['fines']:
                        active_fine = violation['fines'][0]['fine']
                        violation_list.append({
                            "violation": violation['name'],
                            "fine": active_fine
                        })

                result.append({
                    "id": challan.id,
                    "violation_history_id": challan.violation_history_id,
                    "violator_name": challan.violator_name,
                    "violator_cnic": challan.violator_cnic,
                    "mobile_number": challan.mobile_number,
                    "vehicle_number": challan.vehicle_number,
                    "warden_id": challan.warden_id,
                    "challan_date": challan.challan_date,
                    "fine_amount": challan.fine_amount,
                    "status": challan.status,
                    "violation_details": violation_list
                })

            return True, result

        except Exception as exp:
            print(f"Error while retrieving challans: {exp}")
            return False, str(exp)

    @staticmethod
    def update_challan_status(challan_id, new_status):
        try:

            challan = db.session.query(Challan).filter_by(id=challan_id).first()

            if challan is None:
                return False, "Challan not found"


            challan.status = new_status
            db.session.commit()

            return True, {"challan_id": challan.id, "new_status": challan.status}

        except Exception as exp:
            db.session.rollback()  # Rollback in case of an error
            print(f"Error while updating challan status: {exp}")
            return False, str(exp)

    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def autoviolationdetection_fromcameraimage(camera_images):
        try:

            if  camera_images:
                image_list = []
                for item in camera_images:
                    cam_id = item['cam_id']
                    image = item['image']

                    # print(type(cam_id)) # Check Cameraid datatype
                    # print(cam_id) # PRint the id for verification of data
                    try:
                        icam_id = int(cam_id) # Change the camera id str to int
                        # print(type(icam_id))
                    except ValueError:
                        print("Invalid string for conversion")

                    camera=CameraChowkiController.get_camera_by_id(cam_id)


                    if 'error' not in camera:
                        camera_location=camera.get('Direction')
                        camera_type = camera.get('Camera Type')
                        match camera_type:
                            case "front":
                                print("This is the front camera.")
                                image_list.append(image)
                                violations_and_plates=Controller.YoloController.detect_violations_from_frontImage(image)

                                for i, item in enumerate(violations_and_plates):
                                    print(f"\nResult Front #{i + 1}")
                                    violations = item.get('violations', [])
                                    cropped_plate = item.get('cropped_license_plate')

                                    if violations:
                                        print("Violations Detected:")
                                        for violation in violations:
                                            print(f" - {violation}")
                                    else:
                                        print("No violations detected.")

                                    if cropped_plate is not None:

                                        extracted_plate_text=Controller.OCR.NumberExtractor(cropped_plate)
                                        print(f"return number plate from ocr to challan {extracted_plate_text}")
                                        cv2.imshow(f"Cropped License Plate {i + 1}", cropped_plate)
                                        cv2.waitKey(0)
                                        cv2.destroyAllWindows()
                                        cropped_plate = Image.fromarray(cropped_plate)
                                        image_list.append(cropped_plate)
                                    else:
                                        print("No license plate image found.")

                            case "side":
                                print("This is the side camera.")
                                image_list.append(image)
                                detectedviolations = Controller.YoloController.detect_violations_from_sideImage(image)
                                for i, item in enumerate(detectedviolations):
                                    print(f"\nResult Side #{i + 1}")
                                    violations = item.get('violations', [])


                                    if violations:
                                        print("Violations Detected:")
                                        for violation in violations:
                                            print(f" - {violation}")
                                    else:
                                        print("No violations detected.")
                            case _:
                                print("Unknown camera type.")


                bikenumber=extracted_plate_text
                print(f"Bike Number of Violator is {bikenumber}")
                try:
                    bike = ChallanController.get_vehicle_by_licenseplate(bikenumber)
                    if 'error' in bike:
                        message = ChallanController.add_vehicle(bikenumber, 'Bike')
                        if 'Successfully' in message:
                            bike = ChallanController.get_vehicle_by_licenseplate(bikenumber)
                    print(bike['id'], "bike id")
                except Exception as e:
                    print(f"error in bike : {str(e)}")
                    return jsonify({"message": f"An error occurred in getting Bike: {str(e)}"}), 500

                print(bike)
                status = 'Pending'
                created_date = datetime.today().strftime('%Y-%m-%d')
                print(cam_id, bikenumber, camera_location, status, created_date)
                violations_ids = []
                try:

                    detection_fromfront = violations_and_plates[0]["violations"]
                    print("Front Camera Violation: " + ', '.join(detection_fromfront))


                    detection_fromside = detectedviolations[0]["violations"]
                    print("Side Camera Violation: " + ', '.join(detection_fromside))
                    for i in detection_fromfront:
                        if i == 'Side Mirrors' and  "Side Mirrors" in detection_fromside:
                            violations_ids.append(3)



                    for i in detection_fromside:
                        if i == 'Helmet':
                            violations_ids.append(1)
                        elif i.__contains__('Persons'):
                            violations_ids.append(2)
                except Exception as e:
                    print(f"error in adding violation : {str(e)}")
                    return jsonify({"message": f"An error occurred getting Violations: {str(e)}"}), 500

                try:
                    print(f"Image Length Which Save against this violation {len(image_list)}")
                    response, code = ChallanController.add_violation_history_and_details(bike['id'],
                                                                                         camera_location, status,
                                                                                         cam_id,
                                                                                         violations_ids,image_list ,bikenumber)

                except Exception as e:
                    print(f"error in add Violation History : {str(e)}")
                    return jsonify({"message": f"An error occurred Add Violation History: {str(e)}"}), 500

               # Return the result in JSON format
                return response,200
            else:
                print("message File has no filename")
                return jsonify({"message": "File has no filename"}), 400

        except Exception as e:
            # Handle exceptions that may occur
            print(str(e))
            return {"message": f"An error occurred: {str(e)}"}, 500

