# CREATE TABLE ViolationType (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(255) NOT NULL,
#     description TEXT,
# );

from Model.Configure import  db


class Violation(db.Model):
    __tablename__ = 'Violation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
# Back ref
    violation_fines=db.relationship("ViolationFine",back_populates="violation")
    violation_details = db.relationship("ViolationDetails", back_populates="violation")
    challan_violations = db.relationship('ChallanViolations', back_populates='violations')