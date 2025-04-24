from Model import ViolationImages
from Model.Notification import Notification
from Model.Configure import db
from datetime import datetime

class ImageControllerAndNotification:
    @staticmethod
    def get_all_img_violationid(id):
        images =db.session.query(ViolationImages).filter(ViolationImages.violation_id == id).all()

        return [{'id': img.id, 'violation_id': img.violation_id, 'image_path': img.image_path} for img in images]


    # Add a new notification
    @staticmethod
    def add_notification(recipient_type, recipient_id, type_, message):
        try:
            notification = Notification(
                recipient_type=recipient_type,
                recipient_id=recipient_id,
                type=type_,
                message=message,
                created_at=datetime.utcnow(),
                is_read=False
            )
            db.session.add(notification)
            db.session.commit()
            return {"message": "Notification added successfully.", "id": notification.id}
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return {"error": str(e)}

    # Get all notifications (optionally filter by recipient)
    @staticmethod
    def get_notifications(recipient_type=None, recipient_id=None):
        try:
            query = Notification.query
            if recipient_type:
                query = query.filter_by(recipient_type=recipient_type)
            if recipient_id:
                query = query.filter_by(recipient_id=recipient_id)
            notifications = query.order_by(Notification.created_at.desc()).all()
            return [{
            "id": n.id,
            "recipient_type": n.recipient_type,
            "recipient_id": n.recipient_id,
            "type": n.type,
            "message": n.message,
            "created_at": n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "is_read": n.is_read
        } for n in notifications]
        except Exception as e:
            print( str(e))
            return {"error": str(e)}

    # Update a notification (message or type)
    @staticmethod
    def update_notification(notification_id, type_=None, message=None):
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                return {"error": "Notification not found"}

            if type_:
                notification.type = type_
            if message:
                notification.message = message
            db.session.commit()
            return {"message": "Notification updated successfully."}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    # Delete a notification
    @staticmethod
    def delete_notification(notification_id):
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                return {"error": "Notification not found"}
            db.session.delete(notification)
            db.session.commit()
            return {"message": "Notification deleted successfully."}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    # Mark notification as read or unread
    @staticmethod
    def mark_notification_status(notification_id, is_read=True):
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                return {"error": "Notification not found"}
            notification.is_read = is_read
            db.session.commit()
            return {"message": f"Notification marked as {'read' if is_read else 'unread'}."}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}



