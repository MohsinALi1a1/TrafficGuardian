# CREATE TABLE CameraChowki (
#     camera_id INT,
#     chowki_id INT,
#     PRIMARY KEY (camera_id, chowki_id),
#     FOREIGN KEY (camera_id) REFERENCES Camera(id),
#     FOREIGN KEY (chowki_id) REFERENCES Chowki(id)
# );


from Model.Configure import db


class CameraChowki(db.Model):
    __tablename__ = 'CameraChowki'

    camera_id = db.Column(db.Integer, db.ForeignKey('Camera.id'), primary_key=True)
    chowki_id = db.Column(db.Integer, db.ForeignKey('Chowki.id'), primary_key=True)

    # Define the relationships with Camera and Chowki tables
    cameras = db.relationship('Camera', back_populates='chowkis')
    chowki = db.relationship('Chowki', back_populates='cameras')

