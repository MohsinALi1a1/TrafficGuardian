# CREATE TABLE Challan (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     violation_id INT,
#     user_id INT,
#     warden_id INT,
#     challan_date DATE,
#     fineamount DECIMAL(10, 2) NOT NULL,
#     status VARCHAR(50) DEFAULT 'Issued',
#     FOREIGN KEY (violation_id) REFERENCES ViolationHistory(id),
#     FOREIGN KEY (user_id) REFERENCES User(id),
#     FOREIGN KEY (warden_id) REFERENCES TrafficWarden(id)
# );
from Model.Configure import  db