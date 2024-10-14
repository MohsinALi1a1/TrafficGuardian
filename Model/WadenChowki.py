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