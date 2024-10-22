# CREATE TABLE ChallanViolations (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     challan_id INT NOT NULL,
#     violation_id INT NOT NULL,
#     FOREIGN KEY (challan_id) REFERENCES Challan(id) ON DELETE CASCADE,
#     FOREIGN KEY (violation_id) REFERENCES Violation(id) ON DELETE CASCADE  -- Ensure this references a Violation table
# );

from Model.Configure import db


class ChallanViolations(db.Model):
    __tablename__ = 'ChallanViolations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    challan_id = db.Column(db.Integer, db.ForeignKey('Challan.id'), nullable=False)
    violation_id = db.Column(db.Integer, db.ForeignKey('Violation.id'), nullable=False)

    # Relationships
    challans = db.relationship('Challan', back_populates='challan_violations')
    violations = db.relationship('Violation', back_populates='challan_violations')

