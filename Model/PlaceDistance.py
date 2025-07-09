from Model.Configure import  db

class PlaceDistance(db.Model):

    __tablename__ = 'PlaceDistance'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FromPlaceID = db.Column(db.Integer, db.ForeignKey('Place.id'), nullable=False)
    ToPlaceID = db.Column(db.Integer, db.ForeignKey('Place.id'), nullable=False)
    DistanceKM = db.Column(db.Float, nullable=False)

    # Optional: Add relationships to get place names
    from_place = db.relationship('Place', foreign_keys=[FromPlaceID])
    to_place = db.relationship('Place', foreign_keys=[ToPlaceID])
