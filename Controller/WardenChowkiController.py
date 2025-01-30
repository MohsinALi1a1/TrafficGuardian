from Model import db, City, Shift, TrafficWarden, WardenChowki, Chowki, Place
from Controller import LocationController, CameraChowkiController
import random
from datetime import datetime

class WardenChowkiController:

    ##################################################Shift#########################################################################
    @staticmethod
    def get_all_Shift():
        shifts = Shift.query.all()
        return [{'id': shift.id, 'name': shift.shift_type,'start_time' : shift.start_time.strftime('%H:%M:%S') ,'end_time': shift.end_time.strftime('%H:%M:%S')} for shift in shifts]

    @staticmethod
    def get_shift_by_id(ID):
        shift = Shift.query.get(ID)
        if shift:
            return{'id': shift.id, 'name': shift.shift_type,'start_time' : shift.start_time.strftime('%H:%M:%S') ,'end_time': shift.end_time.strftime('%H:%M:%S')},200
        else:
            return {"error": "Shift not found"},404

    @staticmethod
    def get_shift_by_name(shift_name):
        shift = db.session.query(Shift).filter(Shift.shift_type == shift_name).first()
        if shift:
            return {'id': shift.id, 'name': shift.shift_type,'start_time' : shift.start_time.strftime('%H:%M:%S') ,'end_time': shift.end_time.strftime('%H:%M:%S')},200
        else:
            return {"error": "Shift not found"},404

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
                 'address': warden.address ,'cnic':warden.cnic ,'email':warden.email ,'mobile_number':warden.mobile_number ,'city_Name':LocationController.get_city_name_by_id(warden.city_id)[0] }for warden in wardens],200

    @staticmethod
    def get_all_warden_city(city_name):
        city,code=LocationController.get_city_by_name(city_name)
        if not city or code !=200:
            return {'error':'City not found'},409

        wardens = db.session.query(TrafficWarden).filter(TrafficWarden.city_id == city['id']).all()
        return [{'id': warden.id, 'name': warden.name, 'badge_number': warden.badge_number,
                 'address': warden.address, 'cnic': warden.cnic, 'email': warden.email,
                 'mobile_number': warden.mobile_number,
                 'city_Name': LocationController.get_city_name_by_id(warden.city_id)[0]} for warden in wardens],200

    @staticmethod
    def get_warden_by_cnic(warden_cnic):
        warden = db.session.query(TrafficWarden).filter(TrafficWarden.cnic == warden_cnic).first()
        if warden:
            return {'id': warden.id, 'name': warden.name, 'badge_number': warden.badge_number,
                 'address': warden.address, 'cnic': warden.cnic, 'email': warden.email,
                 'mobile_number': warden.mobile_number,
                 'city_Name': LocationController.get_city_name_by_id(warden.city_id)[0]},200
        else:
            return {"error": "Warden not found"},404

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
            wardens,code = WardenChowkiController.get_all_warden_city(city.name)
            chowkis ,code= CameraChowkiController.get_all_Chowki_bycity(city.name)
            shifts = WardenChowkiController.get_all_Shift()

            total_wardens = len(wardens)
            total_chowkis = len(chowkis)
            total_shifts = len(shifts)
            print("Numbers of Wardens = ",total_wardens ,"Numbers of Chowki = ", total_chowkis ,"Numbers of Shifts = ",total_shifts)
            if not chowkis or not wardens:
                continue
            wardenchowkis=db.session.query(WardenChowki).all()
            for warchowki in wardenchowkis:
                db.session.delete(warchowki)
            db.session.commit()
            available_wardens = wardens.copy()
            # Calculate the warden requirement per chowki
            wardens_per_chowki = WardenChowkiController.calculate_wardens_requirement(total_wardens, total_chowkis,
                                                                                      total_shifts)
            print("Warden per Chowki  = ",wardens_per_chowki)


            for chowki in chowkis:

                chowki_place = chowki['place_name']
                chowki_city = chowki['city_name']
                chowki_name = chowki['chowki_name']
                id=chowki['chowki_id']

                #print(chowki_city,chowki_place,chowki_name)
                schedule[chowki_name] = {"shifts": [],"chowkicity":chowki_city,"chowkiplace":chowki_place ,"chowkiid":id}

                for shift_index in range(1, total_shifts + 1):

                    random.shuffle(available_wardens)

                    if len(available_wardens) < wardens_per_chowki:
                        raise ValueError("Not enough wardens available for assignment.")

                    assigned_wardens = available_wardens[:wardens_per_chowki]
                    schedule[chowki_name]["shifts"].append({
                        "shift_index": shift_index,
                        "assigned_wardens": assigned_wardens
                    })


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
                assignment['id']=chowki_data["chowkiid"]
                count=1

                dutyroster.append(assignment)
                for war in assign_wardens:
                    if(count<= len(assign_wardens)):
                        print(f"    Assigned Wardens: {war}")

                        new_assignment = WardenChowkiController.assignwarden(war['id'], chowki_data["chowkiid"], shift['shift_index'])
            print()

        return dutyroster,200

    @staticmethod
    def assignwarden(warden_id, chowki_id, shift_id, duty_date=datetime.today().strftime('%Y-%m-%d')):

        if not warden_id or not chowki_id or not shift_id:
            return {"error": "warden_id, chowki_id, and shift_id are required."}, 400


        new_assignment = WardenChowki(warden_id=warden_id, chowki_id=chowki_id, shift_id=shift_id, duty_date=duty_date)

        try:
            db.session.add(new_assignment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": f"An error occurred while assigning the job: {str(e)}"}, 500

        return {
            'message': f'Successfully assigned Warden {warden_id} to chowki {chowki_id} for shift {shift_id} on {duty_date}.'
        }, 201

    @staticmethod
    def get_all_assignments_on_last_assign_date():
        # Step 1: Get the latest assignment date
        latest_assignment = (
            db.session.query(WardenChowki.duty_date)
            .order_by(db.desc(WardenChowki.duty_date))
            .first()
        )

        # Check if a last assignment was found
        if not latest_assignment:
            return []  # Return an empty list if no assignments exist

        last_assign_date = latest_assignment.duty_date

        # Step 2: Get all assignments on that date with detailed info
        assignments_on_last_date = (
            db.session.query(WardenChowki, TrafficWarden, Chowki, Place, Shift)
            .join(TrafficWarden, TrafficWarden.id == WardenChowki.warden_id)
            .join(Chowki, Chowki.id == WardenChowki.chowki_id)
            .join(Place, Place.id == Chowki.place_id)
            .join(Shift, Shift.id == WardenChowki.shift_id)
            .filter(WardenChowki.duty_date == last_assign_date)
            .all()
        )

        # Step 3: Process results into a list of dictionaries
        result_list = []
        for assignment, warden, chowki, place, shift in assignments_on_last_date:
            result_list.append({
                'warden_name': warden.name,
                'badge_number': warden.badge_number,
                'chowki_name': chowki.name,
                'chowki_place': place.name,
                'shift_name': shift.shift_type,
                'shift_time': shift.start_time.strftime('%H:%M')+" to "+ (shift.end_time.strftime('%H:%M')),  # Format the time as needed
                'duty_date': assignment.duty_date.strftime('%Y-%m-%d'),  # Format the date as needed
            })

        return result_list

    @staticmethod
    def get_dutyroster_for_warden(badge_number):
        # Step 1: Get the latest assignment date
        latest_assignment = (
            db.session.query(WardenChowki.duty_date)
            .order_by(db.desc(WardenChowki.duty_date))
            .first()
        )

        # Check if a last assignment was found
        if not latest_assignment:
            return []  # Return an empty list if no assignments exist

        last_assign_date = latest_assignment.duty_date

        # Step 2: Get all assignments on that date with detailed info
        assignments_on_last_date = (
            db.session.query(WardenChowki, TrafficWarden, Chowki, Place, Shift)
            .join(TrafficWarden, TrafficWarden.id == WardenChowki.warden_id)
            .join(Chowki, Chowki.id == WardenChowki.chowki_id)
            .join(Place, Place.id == Chowki.place_id)
            .join(Shift, Shift.id == WardenChowki.shift_id)
            .filter(WardenChowki.duty_date == last_assign_date)
            .filter(TrafficWarden.badge_number == badge_number)
            .all()
        )

        # Step 3: Process results into a list of dictionaries
        result_list = []
        for assignment, warden, chowki, place, shift in assignments_on_last_date:
            result_list.append({
                'warden_name': warden.name,
                'badge_number': warden.badge_number,
                'chowki_name': chowki.name,
                'chowki_place': place.name,
                'shift_name': shift.shift_type,
                'shift_time': shift.start_time.strftime('%H:%M') + " to " + (shift.end_time.strftime('%H:%M')),
                # Format the time as needed
                'duty_date': assignment.duty_date.strftime('%Y-%m-%d'),  # Format the date as needed
            })

        return result_list

