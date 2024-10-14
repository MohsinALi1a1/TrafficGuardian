# CREATE TABLE Camera (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(100) NOT NULL,
#     type ENUM('front', 'side') NOT NULL,
#     direction_id INT,
#     FOREIGN KEY (direction_id) REFERENCES Direction(id)
# );

from Model.Configure import db


class Camera(db.Model):
    __tablename__ = 'Camera'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('front', 'side'), nullable=False)
    direction_id = db.Column(db.Integer, db.ForeignKey('Direction.id'))

    # Define the relationship with the Direction table
    directions = db.relationship('Direction', back_populates='cameras')

    # Define the many-to-many relationship with Chowki
    chowkis = db.relationship('CameraChowki', back_populates='cameras')
