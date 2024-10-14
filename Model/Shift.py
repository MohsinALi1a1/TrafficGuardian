# CREATE TABLE Shift (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     shift_type ENUM('morning', 'evening', 'night') NOT NULL,
#     start_time TIME NOT NULL,
#     end_time TIME NOT NULL
# );

from Model.Configure import  db

class Shift(db.Model):
    __tablename__ = 'Shift'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shift_type = db.Column(db.Enum('morning', 'evening', 'night'), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)