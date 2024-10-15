# CREATE TABLE Vehicle (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     licenseplate VARCHAR(20) NOT NULL UNIQUE,
#     vehicletype VARCHAR(50) NOT NULL
# );

from Model.Configure import  db


class Vehicle(db.Model):
    __tablename__ = 'Vehicle'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licenseplate = db.Column(db.String(20), nullable=False, unique=True)
    vehicletype = db.Column(db.String(50), nullable=False)

    #back ref
    violation_histories = db.relationship("ViolationHistory", back_populates="vehicle")