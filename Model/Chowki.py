# CREATE TABLE Chowki (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL,
#     place_id INT,
#     FOREIGN KEY (place_id) REFERENCES Place(id)
# );
from Model.Configure import db

class Chowki(db.Model):
    __tablename__ = 'Chowki'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))

    # Define the relationship with the Direction table
    places = db.relationship('Place', back_populates='chowkis')

    # Define the many-to-many relationship with Camera
    cameras = db.relationship('CameraChowki', back_populates='chowki')

    #back Relationship
    warden_chowkis = db.relationship("WardenChowki", back_populates="chowki")


