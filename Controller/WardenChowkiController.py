from Model import Camera, Place, Direction, db, Chowki, CameraChowki, City, Shift, TrafficWarden
from Controller import LocationController

class WardenChowkiController:
    ##################################################Shift#########################################################################
    @staticmethod
    def get_all_Shift():
        shifts = Shift.query.all()
        return [{'id': shift.id, 'name': shift.shift_type,'start_time' : shift.start_time.strftime('%H:%M:%S') ,'end_time': shift.end_time.strftime('%H:%M:%S')} for shift in shifts]

    @staticmethod
    def get_shift_by_id(ID):
        shift = Shift.query.get_or_404(ID)
        if shift:
            return{'id': shift.id, 'name': shift.shift_type,'start_time' : shift.start_time.strftime('%H:%M:%S') ,'end_time': shift.end_time.strftime('%H:%M:%S')}
        else:
            return {"error": "Shift not found"}

    @staticmethod
    def get_shift_by_name(shift_name):
        shift = db.session.query(Shift).filter(Shift.shift_type == shift_name).first()
        if shift:
            return {'id': shift.id, 'name': shift.shift_type,'start_time' : shift.start_time.strftime('%H:%M:%S') ,'end_time': shift.end_time.strftime('%H:%M:%S')}
        else:
            return {"error": "Shift not found"}

    @staticmethod
    def add_shift(shift_type, start_time, end_time):
        # Check if the shift already exists
        existing_shift = db.session.query(Shift).filter(Shift.shift_type == shift_type).first()
        if existing_shift:
            return {"error": "Shift already exists"}, 409

        # Create a new shift instance
        new_shift = Shift(shift_type=shift_type, start_time=start_time, end_time=end_time)
        db.session.add(new_shift)
        db.session.commit()

        return {'message': f'Successfully added shift: {new_shift.shift_type}'}, 201

    @staticmethod
    def delete_shift(shifttype):
        # Fetch the shift by name
        shift = db.session.query(Shift).filter(Shift.shift_type == shifttype).first()
        if not shift:
            return {"error": "Shift not found"}, 404

        db.session.delete(shift)
        db.session.commit()
        return {'Successfully': f'{shifttype} is successfully deleted'}, 201

    @staticmethod
    def update_shift(shifttype,starttime,endtime):
        # Fetch the city by name
        existing_shift = db.session.query(Shift).filter(Shift.shift_type == shifttype).first()

        if not existing_shift:
            return {"error": "Shift doesn't  exists"}, 409
        ex_starttime=existing_shift.start_time
        ex_endtime=existing_shift.end_time
        # Update the shift's name
        existing_shift.start_time = starttime
        existing_shift.end_time = endtime
        db.session.commit()
        return {"message": f"shift  time updated from  start{ex_starttime } end {ex_endtime}   to  start {starttime} ,end {endtime}"}, 201

    ##################################################Traffic Warden #########################################################################
    @staticmethod
    def get_all_warden():
        wardens = TrafficWarden.query.all()
        return [{'id': warden.id, 'name': warden.name, 'badge_number': warden.badge_number,
                 'address': warden.address ,'cnic':warden.cnic ,'email':warden.email ,'mobile_number':warden.mobile_number ,'city_Name':LocationController.get_city_name_by_id(warden.city_id) }for warden in wardens]

    @staticmethod
    def get_all_warden_city(city_name):
        city=LocationController.get_city_by_name(city_name)

        wardens = db.session.query(TrafficWarden).filter(TrafficWarden.city_id == city['id']).all()
        return [{'id': warden.id, 'name': warden.name, 'badge_number': warden.badge_number,
                 'address': warden.address, 'cnic': warden.cnic, 'email': warden.email,
                 'mobile_number': warden.mobile_number,
                 'city_Name': LocationController.get_city_name_by_id(warden.city_id)} for warden in wardens]