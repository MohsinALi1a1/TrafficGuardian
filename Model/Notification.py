from datetime import datetime

from Model.Configure import db
class Notification(db.Model):
    __tablename__ = 'Notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipient_type = db.Column(db.Enum('User', 'TrafficWarden'), nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)