from Model.Configure import db
from datetime import datetime

class StolenBike(db.Model):
    __tablename__ = 'StolenBikes'

    StolenBikeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NumberPlate = db.Column(db.String(20), unique=True, nullable=False)
    OwnerName = db.Column(db.String(100), nullable=True)
    ContactNumber = db.Column(db.String(20), nullable=True)
    FIRNumber = db.Column(db.String(50), nullable=True)
    FIRDate = db.Column(db.Date, nullable=True)
    City = db.Column(db.String(50), nullable=True)
    Place = db.Column(db.String(100), nullable=True)
    Status = db.Column(db.Enum('Active', 'Recovered'), default='Active', nullable=False)
    ReportedDate = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional relationships (for alerts if needed in the future)
    # stolen_bike_alerts = db.relationship("StolenBikeAlert", back_populates="stolen_bike")
