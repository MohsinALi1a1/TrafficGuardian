# -- Adding an alert status column to CameraViolation table
# CREATE TABLE CameraViolation (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     camera_id INT,
#     violation_id INT,
#     alert_status ENUM('Pending', 'Sent') DEFAULT 'Pending',
#     FOREIGN KEY (camera_id) REFERENCES Camera(id),
#     FOREIGN KEY (violation_id) REFERENCES ViolationHistory(id)
# );

from Model.Configure import  db