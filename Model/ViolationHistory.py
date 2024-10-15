# CREATE TABLE ViolationHistory (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     vehicle_id INT,
#     violation_id INT,
#     date DATE,
#     location VARCHAR(255),
#     status VARCHAR(50) DEFAULT 'Pending',
#     imagepath VARCHAR(255),
#     camera_id INT,
#     FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id),
#     FOREIGN KEY (violation_id) REFERENCES Violation(id),
#     FOREIGN KEY (camera_id) REFERENCES Camera(id)
# );

from Model.Configure import  db


class ViolationHistory(db.Model):
    __tablename__ = 'ViolationHistory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.id'), nullable=False)
    violation_id = db.Column(db.Integer, db.ForeignKey('Violation.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='Pending', nullable=True)
    imagepath = db.Column(db.String(255), nullable=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('Camera.id'), nullable=True)

    # Relationships
    vehicle = db.relationship("Vehicle", back_populates="violation_histories")
    violation = db.relationship("Violation", back_populates="violation_histories")
    camera = db.relationship("Camera", back_populates="violation_histories")

