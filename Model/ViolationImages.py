# CREATE TABLE ViolationImages (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_id INT,
#     image_path VARCHAR(255) NOT NULL,
#     FOREIGN KEY (violation_id) REFERENCES ViolationHistory(id) ON DELETE RESTRICT
# );
from Model.Configure import  db


class ViolationImages(db.Model):
    __tablename__ = 'ViolationImages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    violation_id = db.Column(db.Integer, db.ForeignKey('ViolationHistory.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)


    # Relationships
    violation_histories = db.relationship("ViolationHistory", back_populates="violation_images")




