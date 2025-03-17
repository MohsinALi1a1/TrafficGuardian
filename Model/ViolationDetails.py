# CREATE TABLE ViolationDetails (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_history_id INT,
#     violation_id INT,
#     FOREIGN KEY (violation_history_id) REFERENCES ViolationHistory(id) ON DELETE CASCADE,
#     FOREIGN KEY (violation_id) REFERENCES Violation(id) ON DELETE CASCADE  -- Ensure this references a Violation table
# );

from Model.Configure import  db

class ViolationDetails(db.Model):
    __tablename__ = 'ViolationDetails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    violation_history_id = db.Column(db.Integer, db.ForeignKey('ViolationHistory.id'), nullable=False)

    violation_id = db.Column(db.Integer, db.ForeignKey('Violation.id'), nullable=True)

    # Relationships
    violation_histories = db.relationship("ViolationHistory", back_populates="violation_details")

    violation = db.relationship("Violation", back_populates="violation_details")


