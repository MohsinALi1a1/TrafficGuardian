# CREATE TABLE ViolationHistory (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     vehicle_id INT,
#     date DATE,
#     location VARCHAR(255),
#     status VARCHAR(50) DEFAULT 'Pending',
#     camera_id INT,
#     FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id) ON DELETE CASCADE,
#     FOREIGN KEY (camera_id) REFERENCES Camera(id) ON DELETE CASCADE
# );
from sqlalchemy.sql import func

from Model.Configure import  db


class ViolationHistory(db.Model):
    __tablename__ = 'ViolationHistory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('Vehicle.id'), nullable=False)
    violation_datetime = db.Column(db.DateTime, server_default=func.current_timestamp(), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='Pending', nullable=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('Camera.id'), nullable=True)

    # Relationships
    vehicle = db.relationship("Vehicle", back_populates="violation_histories")
    violation_details = db.relationship("ViolationDetails", back_populates="violation_histories")
    camera = db.relationship("Camera", back_populates="violation_histories")

    challans = db.relationship('Challan', back_populates='violation_histories')

    violation_images = db.relationship("ViolationImages", back_populates="violation_histories")