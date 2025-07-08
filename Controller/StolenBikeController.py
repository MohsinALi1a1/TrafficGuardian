from Model import StolenBike
from Model.Configure import db
from datetime import datetime


from Model.Configure import db
from datetime import datetime


class StolenBikeController:

    @staticmethod
    def get_all_bikes():
        bikes = StolenBike.query.all()
        return [{
            'id': bike.StolenBikeID,
            'NumberPlate': bike.NumberPlate,
            'OwnerName': bike.OwnerName,
            'ContactNumber': bike.ContactNumber,
            'FIRNumber': bike.FIRNumber,
            'FIRDate': bike.FIRDate.isoformat() if bike.FIRDate else None,
            'City': bike.City,
            'Place': bike.Place,
            'Status': bike.Status,
            'ReportedDate': bike.ReportedDate.isoformat()
        } for bike in bikes]

    @staticmethod
    def get_bike_by_id(bike_id):
        bike = StolenBike.query.get_or_404(bike_id)
        return {
            'id': bike.StolenBikeID,
            'NumberPlate': bike.NumberPlate,
            'OwnerName': bike.OwnerName,
            'ContactNumber': bike.ContactNumber,
            'FIRNumber': bike.FIRNumber,
            'FIRDate': bike.FIRDate.isoformat() if bike.FIRDate else None,
            'City': bike.City,
            'Place': bike.Place,
            'Status': bike.Status,
            'ReportedDate': bike.ReportedDate.isoformat()
        }

    @staticmethod
    def get_bike_by_number_plate(plate):
        bike = db.session.query(StolenBike).filter(StolenBike.NumberPlate == plate).first()
        if bike:
            return {
                'id': bike.StolenBikeID,
                'NumberPlate': bike.NumberPlate,
                'OwnerName': bike.OwnerName,
                'ContactNumber': bike.ContactNumber,
                'FIRNumber': bike.FIRNumber,
                'FIRDate': bike.FIRDate.isoformat() if bike.FIRDate else None,
                'City': bike.City,
                'Place': bike.Place,
                'Status': bike.Status,
                'ReportedDate': bike.ReportedDate.isoformat()
            }
        else:
            return {"error": "Stolen bike not found"}, 404

    @staticmethod
    def add_bike(data):
        existing = db.session.query(StolenBike).filter_by(NumberPlate=data['NumberPlate']).first()
        if existing:
            return {"error": "Bike with this number plate already exists"}, 400

        bike = StolenBike(
            NumberPlate=data['NumberPlate'],
            OwnerName=data.get('OwnerName'),
            ContactNumber=data.get('ContactNumber'),
            FIRNumber=data.get('FIRNumber'),
            FIRDate=datetime.strptime(data['FIRDate'], '%Y-%m-%d') if data.get('FIRDate') else None,
            City=data.get('City'),
            Place=data.get('Place'),
            Status=data.get('Status', 'Active')
        )
        db.session.add(bike)
        db.session.commit()
        return {'Successfully': f'Bike {bike.NumberPlate} is successfully added'}

    @staticmethod
    def delete_bike_by_plate(plate):
        bike = db.session.query(StolenBike).filter(StolenBike.NumberPlate == plate).first()
        if not bike:
            return {"error": "Stolen bike not found"}, 404

        db.session.delete(bike)
        db.session.commit()
        return {'Successfully': f'{plate} is successfully deleted'}, 200

    @staticmethod
    def update_bike_by_plate(plate, updated_data):
        bike = db.session.query(StolenBike).filter(StolenBike.NumberPlate == plate).first()
        if not bike:
            return {"error": "Stolen bike not found"}, 404

        # Update fields
        bike.OwnerName = updated_data.get('OwnerName', bike.OwnerName)
        bike.ContactNumber = updated_data.get('ContactNumber', bike.ContactNumber)
        bike.FIRNumber = updated_data.get('FIRNumber', bike.FIRNumber)
        if updated_data.get('FIRDate'):
            bike.FIRDate = datetime.strptime(updated_data['FIRDate'], '%Y-%m-%d')
        bike.City = updated_data.get('City', bike.City)
        bike.Place = updated_data.get('Place', bike.Place)
        bike.Status = updated_data.get('Status', bike.Status)

        db.session.commit()
        return {"message": f"Bike with plate {plate} updated successfully"}, 200

    @staticmethod
    def change_bike_status(plate, new_status):
        bike = db.session.query(StolenBike).filter_by(NumberPlate=plate).first()
        if not bike:
            return {"error": "Stolen bike not found"}, 404

        bike.Status = new_status
        db.session.commit()
        return {"message": f"Status for bike {plate} changed to {new_status}"}, 200
