from Model import User, Vehicle, db, Violation, ViolationFine, ViolationHistory, ViolationDetails, Challan, \
    ChallanViolations
from sqlalchemy.exc import SQLAlchemyError

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

    #################################  Violations & Fine ########################################################

    @staticmethod
    def get_all_violations():
        violations = Violation.query.all()
        return [{
            'id': violation.id,
            'name': violation.name,
            'description': violation.description,
            'fines': [{'id': fine.id, 'created_date': fine.created_date, 'fine': float(fine.fine)} for fine in
                      violation.violation_fines]
        } for violation in violations]

    @staticmethod
    def get_violation_by_id(violation_id):
        violation = Violation.query.get_or_404(violation_id)
        return {
            'id': violation.id,
            'name': violation.name,
            'description': violation.description,
            'fines': [{'id': fine.id, 'created_date': fine.created_date, 'fine': float(fine.fine)} for fine in
                      violation.violation_fines]
        }

    @staticmethod
    def add_violation(name, description=None):
        existing_violation = db.session.query(Violation).filter(Violation.name == name).first()
        if existing_violation:
            return {"error": "Violation already exists"}, 409
        new_violation = Violation(name=name, description=description)
        db.session.add(new_violation)
        db.session.commit()
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
    def update_violation(violation_id, new_name=None, new_description=None):
        violation = db.session.query(Violation).get(violation_id)

        if not violation:
            return {"error": "Violation not found"}, 404

        if new_name:
            violation.name = new_name
        if new_description:
            violation.description = new_description

        db.session.commit()
        return {"message": f"Violation updated successfully"}, 201

    @staticmethod
    def add_violation_fine(violation_name, created_date, fine):
        violation = db.session.query(Violation).filter(Violation.name == violation_name).first()
        if not violation:
            return {"error": "Violation not found"}, 404
        new_fine = ViolationFine(violation_id=violation.id, created_date=created_date, fine=fine)
        db.session.add(new_fine)
        db.session.commit()
        return {'Successfully': f'Fine of {fine} added to violation {violation.name}'}

    @staticmethod
    def delete_violation_fine(fine_id):
        fine = db.session.query(ViolationFine).get(fine_id)
        if not fine:
            return {"error": "Fine not found"}, 404

        db.session.delete(fine)
        db.session.commit()
        return {'Successfully': f'Fine {fine.id} deleted successfully'}, 201



#################################  ViolationsHistory & Its Details ########################################################

    @staticmethod
    def add_violation_history_and_details(vehicle_id, date, location, status, imagepath, camera_id, violation_ids):
        try:
            # Validate inputs here if necessary

            violation_history = ViolationHistory(
                vehicle_id=vehicle_id,
                date=date,
                location=location,
                status=status,
                imagepath=imagepath,
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
    def get_violation_history_with_details(vehicle_id=None, date=None, camera_id=None):
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

            result = []
            for history in violation_histories:
                violation_details = [
                    {
                        "violation_name": db.session.query(Violation.name).filter(Violation.id==detail.violation_id).scalar()

                    }
                    for detail in history.violation_details
                ]
                result.append({
                    "id": history.id,
                    "vehicle_id": history.vehicle_id,
                    "date": history.date,
                    "location": history.location,
                    "status": history.status,
                    "imagepath": history.imagepath,
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
                                        user_id, warden_id, fine_amount):
        try:
            new_challan = Challan(
                violation_history_id=violation_history_id,
                user_id=user_id,
                warden_id=warden_id,
                challan_date=date,
                fine_amount=fine_amount,
                status=status
            )

            db.session.add(new_challan)
            db.session.flush()  # Flush to get the new challan ID before committing

            for violation_id in violation_ids:
                new_challan_violation = ChallanViolations(
                    challan_id=new_challan.id,
                    violation_id=violation_id
                )
                db.session.add(new_challan_violation)

            db.session.commit()

            return True, new_challan.id

        except Exception as exp:
            db.session.rollback()
            print(f"Error while adding challan: {exp}")
            return False, None  # Return failure and no ID

    @staticmethod
    def get_challans(challan_id=None, user_id=None, warden_id=None):
        try:
            query = db.session.query(Challan)

            if challan_id:

                challan = query.filter_by(id=challan_id).first()
                if challan is None:
                    return False, "Challan not found"


                challan_details = db.session.query(ChallanViolations).filter(
                    ChallanViolations.challan_id == challan.id).all()

                violation_names = []
                for violation in challan_details:
                    violation_name = db.session.query(Violation.name).filter(
                        Violation.id == violation.violation_id).scalar()
                    if violation_name:
                        violation_names.append({"violation": violation_name})

                return True, {
                    "challan": {
                        "id": challan.id,
                        "violation_history_id": challan.violation_history_id,
                        "user_id": challan.user_id,
                        "warden_id": challan.warden_id,
                        "challan_date": challan.challan_date,
                        "fine_amount": challan.fine_amount,
                        "status": challan.status,
                        "violation_names": violation_names
                    }
                }


            if user_id:
                query = query.filter_by(user_id=user_id)
            if warden_id:
                query = query.filter_by(warden_id=warden_id)


            challans = query.all()
            result = []
            for challan in challans:

                challan_details = db.session.query(ChallanViolations).filter(
                    ChallanViolations.challan_id == challan.id).all()

                violation_names = []
                for violation in challan_details:
                    violation_name = db.session.query(Violation.name).filter(
                        Violation.id == violation.violation_id).scalar()
                    if violation_name:
                        violation_names.append({"violation": violation_name})

                result.append({
                    "id": challan.id,
                    "violation_history_id": challan.violation_history_id,
                    "user_id": challan.user_id,
                    "warden_id": challan.warden_id,
                    "challan_date": challan.challan_date,
                    "fine_amount": challan.fine_amount,
                    "status": challan.status,
                    "violation_names": violation_names  # Add violation names to each challan
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
