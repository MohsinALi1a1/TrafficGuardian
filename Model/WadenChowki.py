# CREATE TABLE WardenChowki (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     warden_id INT,
#     chowki_id INT,
#     shift_id INT,
#     duty_date DATE,
#     FOREIGN KEY (warden_id) REFERENCES TrafficWarden(id),
#     FOREIGN KEY (chowki_id) REFERENCES Chowki(id),
#     FOREIGN KEY (shift_id) REFERENCES Shift(id)
# );

from Model.Configure import  db

class WardenChowki(db.Model):
    __tablename__ = 'WardenChowki'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    warden_id = db.Column(db.Integer, db.ForeignKey('TrafficWarden.id'))
    chowki_id = db.Column(db.Integer, db.ForeignKey('Chowki.id'))
    shift_id = db.Column(db.Integer, db.ForeignKey('Shift.id'))
    duty_date = db.Column(db.Date)

    # Relationships
    warden = db.relationship("TrafficWarden", back_populates="warden_chowkis")
    chowki = db.relationship("Chowki", back_populates="warden_chowkis")
    shift = db.relationship("Shift", back_populates="warden_chowkis")



