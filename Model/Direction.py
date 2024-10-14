# CREATE TABLE Direction (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL,
#     place_id INT,
#     FOREIGN KEY (place_id) REFERENCES Place(id)
# );

from Model.Configure import db

class Direction(db.Model):
    __tablename__ = 'Direction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('Place.id'))

    # Relationship with Place
    places = db.relationship('Place', back_populates='directions')

    # Define the relationship with the Camera table
    cameras = db.relationship('Camera', back_populates='directions')
