# CREATE TABLE Violation (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(255) NOT NULL,
#     description TEXT,
#     limit_value INT NOT NULL DEFAULT -1,
# status VARCHAR(50) NOT NULL DEFAULT 'Active'
# start_date DATETIME DEFAULT NULL,
# end_date DATETIME DEFAULT NULL;
# );


from Model.Configure import  db


class Violation(db.Model):
    __tablename__ = 'Violation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    limit_value = db.Column(db.Integer, nullable=False, default=-1)
    status = db.Column(db.String(50), default="Active", nullable=False)
    start_date = db.Column(db.DateTime, nullable=True, default=None)
    end_date = db.Column(db.DateTime, nullable=True, default=None)
# Back ref
    violation_fines=db.relationship("ViolationFine",back_populates="violation")
    violation_details = db.relationship("ViolationDetails", back_populates="violation")
    challan_violations = db.relationship('ChallanViolations', back_populates='violations')