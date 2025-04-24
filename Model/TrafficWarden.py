# CREATE TABLE TrafficWarden (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL,
#     badge_number VARCHAR(50) UNIQUE NOT NULL,
#     address VARCHAR(255),
#     cnic VARCHAR(15) UNIQUE NOT NULL,
#     email VARCHAR(100) UNIQUE,
#     mobile_number VARCHAR(15) UNIQUE NOT NULL,
#     city_id INT,
# password VARCHAR(255) NOT NULL,
#image_path VARCHAR(255) DEFAULT NULL,
#     FOREIGN KEY (city_id) REFERENCES City(id)
# );


from Model.Configure import db

class TrafficWarden(db.Model):
    __tablename__ = 'TrafficWarden'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    badge_number = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255))
    cnic = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password=db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    image_path=db.Column(db.String(255) ,nullable=True)
    PermissionType = db.Column(db.Integer, default=1)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))

    # Relationship with City
    city = db.relationship('City', back_populates='trafficwardens')


    #BackRelationship
    warden_chowkis = db.relationship("WardenChowki", back_populates="warden")
    challans = db.relationship('Challan', back_populates='warden')