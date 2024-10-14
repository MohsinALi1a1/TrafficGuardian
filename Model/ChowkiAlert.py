# CREATE TABLE ChowkiAlert (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_id INT,
#     chowki_id INT,
#     received_time DATETIME,
#     waden_id INT,
#     status ENUM('Pending', 'Processed') DEFAULT 'Pending',
#     FOREIGN KEY (violation_id) REFERENCES ViolationHistory(id),
#     FOREIGN KEY (chowki_id) REFERENCES Chowki(id),
#     FOREIGN KEY (waden_id) REFERENCES TrafficWarden(id)
# );

from Model.Configure import  db