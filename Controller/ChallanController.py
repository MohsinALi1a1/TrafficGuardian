from Model import User, Vehicle, db, Violation, ViolationFine


class ChallanController():
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
