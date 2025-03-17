# CREATE TABLE Challan (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_history_id INT,  -- Corrected name to match ViolationHistory
#     user_id INT,
#     warden_id INT,
#     challan_date DATE,
#     fine_amount DECIMAL(10, 2) NOT NULL,
#     status VARCHAR(50) DEFAULT 'Issued',
#     FOREIGN KEY (violation_history_id) REFERENCES ViolationHistory(id) ON DELETE CASCADE,  -- Fixed foreign key
#     FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
#     FOREIGN KEY (warden_id) REFERENCES TrafficWarden(id) ON DELETE CASCADE
# );


from Model.Configure import  db

class Challan(db.Model):
    __tablename__ = 'Challan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    violation_history_id = db.Column(db.Integer, db.ForeignKey('ViolationHistory.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    warden_id = db.Column(db.Integer, db.ForeignKey('TrafficWarden.id'), nullable=False)
    challan_date = db.Column(db.Date, nullable=False)
    fine_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='Issued')

    # Relationships
    violation_histories = db.relationship('ViolationHistory', back_populates='challans')
    user = db.relationship('User', back_populates='challans')
    warden = db.relationship('TrafficWarden', back_populates='challans')

    challan_violations = db.relationship('ChallanViolations', back_populates='challans')


