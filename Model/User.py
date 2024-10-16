# CREATE TABLE User (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(255) NOT NULL,
#     cnic VARCHAR(20) NOT NULL UNIQUE,
#     mobilenumber VARCHAR(15) NOT NULL,
#     email VARCHAR(255)
# );

from Model.Configure import  db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    cnic = db.Column(db.String(20), nullable=False, unique=True)
    mobilenumber = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255))