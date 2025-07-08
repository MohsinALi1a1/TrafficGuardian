# CREATE TABLE Challan (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_history_id INT,
#     warden_id INT,
#     challan_date DATE,
#     fine_amount DECIMAL(10, 2) NOT NULL,
#     status VARCHAR(50) DEFAULT 'Issued',
#    violator_name VARCHAR(255) NOT NULL,
#     violator_cnic VARCHAR(20) NOT NULL,
#     mobile_number VARCHAR(15) NOT NULL,
#     vehicle_number VARCHAR(20) NOT NULL,
from datetime import datetime

#     FOREIGN KEY (violation_history_id) REFERENCES ViolationHistory(id) ON DELETE CASCADE,  -- Fixed foreign key
#     FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
#     FOREIGN KEY (warden_id) REFERENCES TrafficWarden(id) ON DELETE CASCADE
# );


from Model.Configure import  db

class Challan(db.Model):
    __tablename__ = 'Challan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    violation_history_id = db.Column(db.Integer, db.ForeignKey('ViolationHistory.id'), nullable=True)
    warden_id = db.Column(db.Integer, db.ForeignKey('TrafficWarden.id'), nullable=False)
    # challan_date = db.Column(db.Date, nullable=False)
    challan_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    fine_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='Issued')
    violator_name=db.Column(db.String(255), nullable=False)
    violator_cnic=db.Column(db.String(20), nullable=False)
    mobile_number=db.Column(db.String(15), nullable=False)
    vehicle_number=db.Column(db.String(20), nullable=False)

    # Relationships
    violation_histories = db.relationship('ViolationHistory', back_populates='challans')

    warden = db.relationship('TrafficWarden', back_populates='challans')

    challan_violations = db.relationship('ChallanViolations', back_populates='challans')


