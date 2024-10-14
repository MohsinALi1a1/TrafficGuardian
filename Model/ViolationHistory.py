# CREATE TABLE ViolationHistory (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     vehicle_id INT,
#     violationtype_id INT,
#     violationdate DATE,
#     violationlocation VARCHAR(255),
#     violationstatus VARCHAR(50) DEFAULT 'Pending',
#     imagepath VARCHAR(255),
#     FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id),
#     FOREIGN KEY (violationtype_id) REFERENCES ViolationType(id)
# );

from Model.Configure import  db