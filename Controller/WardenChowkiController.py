from flask import jsonify

from Model import Camera, Place, Direction, db, Chowki, CameraChowki, City, Shift, TrafficWarden
from Controller import LocationController, CameraChowkiController
import random

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

    @staticmethod
    def get_warden_by_cnic(warden_cnic):
        warden = db.session.query(TrafficWarden).filter(TrafficWarden.cnic == warden_cnic).first()
        if warden:
            return {'id': warden.id, 'name': warden.name, 'badge_number': warden.badge_number,
                 'address': warden.address, 'cnic': warden.cnic, 'email': warden.email,
                 'mobile_number': warden.mobile_number,
                 'city_Name': LocationController.get_city_name_by_id(warden.city_id)}
        else:
            return {"error": "Warden not found"}

    @staticmethod
    def add_warden(name, badge_number, address, cnic, email, mobile_number, city_name):
        # Check if the warden already exists
        existing_warden = db.session.query(TrafficWarden).filter(TrafficWarden.cnic == cnic).first()
        if existing_warden:
            return {"error": f"Warden already exists against CNIC {cnic}"}, 409

        # Check if the city exists
        city = db.session.query(City).filter(City.name == city_name).first()
        if not city:
            return {"error": f"City '{city_name}' does not exist."}, 404

        # Create a new Warden instance
        new_warden = TrafficWarden(
            name=name,
            badge_number=badge_number,
            address=address,
            cnic=cnic,
            email=email,
            mobile_number=mobile_number,
            city_id=city.id
        )

        db.session.add(new_warden)
        db.session.commit()

        return {
            'message': f'Successfully added Warden: {name}',
            'warden': {
                'id': new_warden.id,
                'name': new_warden.name,
                'badge_number': new_warden.badge_number,
                'address': new_warden.address,
                'cnic': new_warden.cnic,
                'email': new_warden.email,
                'mobile_number': new_warden.mobile_number,
                'city_id': new_warden.city_id
            }
        }, 201

    @staticmethod
    def delete_warden(cnic):
        # Check if the warden exists
        warden = db.session.query(TrafficWarden).filter(TrafficWarden.cnic == cnic).first()
        if not warden:
            return {"error": f"Warden with CNIC {cnic} not found."}, 404

        # Delete the warden
        db.session.delete(warden)
        db.session.commit()

        return {'message': f'Successfully deleted Warden with CNIC: {cnic}'}, 200

    @staticmethod
    def update_warden(cnic, name=None, badge_number=None, address=None, email=None, mobile_number=None, city_name=None):
        # Check if the warden exists
        warden = db.session.query(TrafficWarden).filter(TrafficWarden.cnic == cnic).first()
        if not warden:
            return {"error": f"Warden with CNIC {cnic} not found."}, 404

        # Update fields if provided
        if name:
            warden.name = name
        if badge_number:
            warden.badge_number = badge_number
        if address:
            warden.address = address
        if email:
            warden.email = email
        if mobile_number:
            warden.mobile_number = mobile_number
        if city_name:
            city = db.session.query(City).filter(City.name == city_name).first()
            if not city:
                return {"error": f"City '{city_name}' does not exist."}, 404
            warden.city_id = city.id

        # Commit the changes
        db.session.commit()

        return {
            'message': f'Successfully updated Warden with CNIC: {cnic}',
            'warden': {
                'id': warden.id,
                'name': warden.name,
                'badge_number': warden.badge_number,
                'address': warden.address,
                'cnic': warden.cnic,
                'email': warden.email,
                'mobile_number': warden.mobile_number,
                'city_id': warden.city_id
            }
        }, 200

################################################## WardenChowki #########################################################################

    @staticmethod
    def calculate_wardens_requirement(total_wardens, total_chowkis, total_shifts):
        if total_chowkis == 0 or total_shifts == 0:
            raise ValueError("Total chowkis and shifts must be greater than zero.")

        # Calculate warden requirement per chowki
        warden_requirement_per_chowki = total_wardens / (total_chowkis * total_shifts)

        # Ensure at least one warden per chowki if possible
        return max(round(warden_requirement_per_chowki), 1)


    @staticmethod
    def create_duty_roster():
        schedule = {}
        cities = City.query.all()
        dutyroster=[]

        for city in cities:
            print(city.name)
            wardens = WardenChowkiController.get_all_warden_city(city.name)
            chowkis = CameraChowkiController.get_all_Chowki_bycity(city.name)
            shifts = WardenChowkiController.get_all_Shift()

            total_wardens = len(wardens)
            total_chowkis = len(chowkis)
            total_shifts = len(shifts)
            print("Numbers of Wardens = ",total_wardens ,"Numbers of Chowki = ", total_chowkis ,"Numbers of Shifts = ",total_shifts)
            if not chowkis or not wardens:
                continue
            available_wardens = wardens.copy()
            # Calculate the warden requirement per chowki
            wardens_per_chowki = WardenChowkiController.calculate_wardens_requirement(total_wardens, total_chowkis,
                                                                                      total_shifts)
            print("Waden per Chowki  = ",wardens_per_chowki)
            # Initialize the schedule

            for chowki in chowkis:

                chowki_place = chowki['place_name']
                chowki_city = chowki['city_name']
                chowki_name = chowki['chowki_name']


                #print(chowki_city,chowki_place,chowki_name)
                schedule[chowki_name] = {"shifts": [],"chowkicity":chowki_city,"chowkiplace":chowki_place}


                for shift_index in range(total_shifts):
                    random.shuffle(available_wardens)

                    if len(available_wardens) < wardens_per_chowki:
                        raise ValueError("Not enough wardens available for assignment.")

                    assigned_wardens = available_wardens[:wardens_per_chowki]
                    schedule[chowki_name]["shifts"].append({
                        "shift_index": shift_index,
                        "assigned_wardens": assigned_wardens
                    })

                    # Remove assigned wardens from available pool
                    available_wardens = [warden for warden in available_wardens if warden not in assigned_wardens]


        for chowki_name, chowki_data in schedule.items():

            print(f"Chowki: {chowki_name}")
           # print(f"ChowkiDate {chowki_data['shifts']}")
            for shift in chowki_data["shifts"]:
                assignment = {}
                assignment['chowki'] = chowki_name
                print(f"  Shift Index: {shift['shift_index']}")
                assignment['shift'] = shift['shift_index']
                assign_wardens=shift['assigned_wardens']
                assignment['warden']=assign_wardens
                assignment['city']=  chowki_data["chowkicity"]
                assignment['place'] = chowki_data["chowkiplace"]
                count=1

                dutyroster.append(assignment)
                for war in assign_wardens:
                    if(count<= len(assign_wardens)):
                        print(f"    Assigned Wardens: {war}")


            print()


        return dutyroster
