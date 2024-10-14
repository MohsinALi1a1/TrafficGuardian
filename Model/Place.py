# CREATE TABLE Place (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL,
#     city_id INT,
#     FOREIGN KEY (city_id) REFERENCES City(id)
# );
from Model.Configure import db

class Place(db.Model):
    __tablename__ = 'Place'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    city = db.relationship('City', back_populates='places')

    #Relationship with Chowki
    chowkis = db.relationship('Chowki', back_populates='places')

    # Relationship with Direction
    directions = db.relationship('Direction', back_populates='places')
