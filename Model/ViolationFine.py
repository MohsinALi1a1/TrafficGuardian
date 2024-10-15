# CREATE TABLE ViolationFine (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_id INT,
#     created_date DATE NOT NULL,
#     fine DECIMAL(10, 2) NOT NULL,
#     FOREIGN KEY (violation_id) REFERENCES Violation(id)
# );
from Model.Configure import  db


class ViolationFine(db.Model):
     __tablename__ = 'ViolationFine'
     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     violation_id = db.Column(db.Integer, db.ForeignKey('Violation.id'), nullable=False)
     created_date = db.Column(db.Date, nullable=False)
     fine = db.Column(db.Numeric(10, 2), nullable=False)

     # Relationship to ViolationType (if needed)
     violation = db.relationship("Violation", back_populates="violation_fines")

