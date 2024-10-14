# CREATE TABLE City (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL
# );

from Model.Configure import  db


class City(db.Model):
    __tablename__ = 'City'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship with Place
    places = db.relationship('Place', back_populates='city')

    # Relationship with TrafficWarden
    trafficwardens = db.relationship('TrafficWarden', back_populates='city')
