from Model import City,Place,Direction ,db



class LocationController:

    @staticmethod
    def get_all_City():
        cities=City.query.all()
        return [{'id':city.id ,'name':city.name }for city in cities]

    @staticmethod
    def get_city_name_by_id(ID):
        city = City.query.get_or_404(ID)
        return city.name


    @staticmethod
    def get_city_by_id(ID):
        city = City.query.get_or_404(ID)
        if city:
            return {'id':city.id ,'name':city.name }
        else:
            return {"error": "City not found"}

    @staticmethod
    def get_city_by_name(city_name):
        city = db.session.query(City).filter(City.name == city_name).first()
        if city:
            return {'id': city.id, 'name': city.name}
        else:
            return {"error": "City not found"}

    @staticmethod
    def add_city(city_name):
         # Check if the city already exists
        existing_city =  db.session.query(City).filter(City.name == city_name).first()
        if existing_city :
            return {"error": "City already exists"}, 409
        # Create city instance
        new_city = City(name=city_name)
        db.session.add(new_city)
        db.session.commit()
        print(new_city.id ,new_city.name)
        return {'Sucessfully':f'{new_city} is SucessFully Added'}

    @staticmethod
    def delete_city(city_name):
        # Fetch the city by name
        city = db.session.query(City).filter(City.name == city_name).first()
        if not city:
            return {"error": "City not found"}, 404

        db.session.delete(city)
        db.session.commit()
        return {'Successfully': f'{city.name} is successfully deleted'},201


    @staticmethod
    def update_city(city_name,new_name):
        # Fetch the city by name
        city = db.session.query(City).filter(City.name == city_name).first()

        if not city:
            return {"error": "City not found"}, 404

        # Update the city's name
        city.name = new_name
        db.session.commit()
        return {"message": f"City name updated from {city_name} to {new_name}"}, 201


#################################  Place ########################################################

    @staticmethod
    def get_all_Places(city_name):
        city = db.session.query(City).filter(City.name == city_name).first()

        if not city:
            return []  # Return an empty list if the city doesn't exist

        places = db.session.query(Place).filter(Place.city_id == city.id).all()
        return [{'id': place.id, 'name': place.name, 'city_id': place.city_id} for place in places]

    @staticmethod
    def get_place_by_id(ID):
        place = Place.query.get_or_404(ID)
        if place:
            return {'id':place.id ,'name':place.name ,'city_id':place.city_id}
        else:
            return {"error": "Place not found"}

    @staticmethod
    def get_place_by_name(place_name):
        place = db.session.query(Place).filter(Place.name == place_name)
        if place:
            return [{'id':pl.id ,'name':pl.name ,'city_id':pl.city_id}for pl in place]
        else:
            return {"error": "Place not found"}

    @staticmethod
    def add_place(city_name , place_name):
        place = db.session.query(Place).filter(Place.name == place_name)
        city= LocationController.get_city_by_name(city_name)
        if place :
            for pl in place:
                 if (pl.city_id == city['id']):
                    return {"error": f"Place {place_name} Already exist in City {city_name}"}
        # Create place instance
        new_place = Place(name=place_name,city_id=city['id'])
        db.session.add(new_place)
        db.session.commit()
        return {'Sucessfully':f'{place_name} is SucessFully Added in City {city_name}'}

    @staticmethod
    def delete_place(city_name,place_name):
        # Fetch the place by name
        city= LocationController.get_city_by_name(city_name)
        place = db.session.query(Place).filter(Place.name == place_name, Place.city_id==city['id']).first()
        if not place:
            return {"error": f"place {place_name} not found in City {city_name}"}, 404

        db.session.delete(place)
        db.session.commit()
        return {'Successfully': f'{place_name} is successfully deleted'}, 201

    @staticmethod
    def update_place(place_name, new_name):
        # Fetch the Place by name
        place = db.session.query(Place).filter(Place.name == place_name).first()

        if not place:
            return {"error": f"Place{place_name} not found"}, 404

        # Update the Place's name
        place.name = new_name
        db.session.commit()
        return {"message": f"Place name updated from {place_name} to {new_name}"}, 201

############################################  Directions ########################################################

    @staticmethod
    def get_all_Directions(place_name):
        place = db.session.query(Place).filter(Place.name == place_name).first()
        if not place:
            return []  # Return an empty list if the place doesn't exist
        directions=db.session.query(Direction).filter(Direction.place_id == place.id).all()
        return [{'id':direction.id ,'name':direction.name ,'place_name':place_name}for direction in directions]



    @staticmethod
    def get_direction_by_id(ID):
        direction = Direction.query.get_or_404(ID)
        if direction:
            return {'id':direction.id ,'name':direction.name ,'place_id':direction.place_id}
        else:
            return {"error": "Direction not found"}



    @staticmethod
    def get_direction_by_name(direction_name):
        directions = db.session.query(Direction).filter(Direction.name == direction_name)
        if directions:
            return [{'id':direction.id , 'name':direction.name , 'place_id':direction.place_id} for direction in directions]
        else:
            return {"error": "Direction  not found"}

    @staticmethod
    def add_direction(place_name, direction_name):
        direction = db.session.query(Direction).filter(Direction.name == direction_name)

        place = db.session.query(Place).filter(Place.name == place_name).first()
        if direction:
            for dir in direction:
                if (dir.place_id == place.id):
                    return {"error": f"Direction {direction_name} Already exist in Place {place_name}"}
        # Create place instance
        new_direction = Direction(name=direction_name, place_id=place.id)
        db.session.add(new_direction)
        db.session.commit()
        return {'Sucessfully': f'{direction_name} is SucessFully Added in place {place_name}'}

    @staticmethod
    def delete_direction(place_name, direction_name):
        # Fetch the place by name
        place = db.session.query(Place).filter(Place.name == place_name).first()
        direction= db.session.query(Direction).filter(Direction.name == direction_name, Direction.place_id == place.id).first()
        if not direction:
            return {"error": f"Direction {direction_name} not found in place {place_name}"}, 404

        db.session.delete(direction)
        db.session.commit()
        return {'Successfully': f'{direction_name} is successfully deleted'}, 201

    @staticmethod
    def update_direction(place_name,direction_name, new_name):
        # Fetch the Place by name
        place = db.session.query(Place).filter(Place.name == place_name).first()
        print(place)
        if not place:
            return {"error": f" {direction_name} not found"}, 404 # Return an empty list if the place doesn't exist
        direction = db.session.query(Direction).filter(Direction.place_id == place.id,Direction.name==direction_name).first()
        print(direction)
        if not direction:
            return {"error": f"Direction {direction_name} not found"}, 404

        # Update the Direction's name
        direction.name = new_name
        db.session.commit()
        return {"message": f"Direction name updated from {direction_name} to {new_name}"}, 201
