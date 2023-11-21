# crud.py

from flask import current_app
from . import db  # dbはFlask-SQLAlchemyのインスタンス

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text)

# Create
def create_reservation(date, time, user_id, details=None):
    reservation = Reservation(date=date, time=time, user_id=user_id, details=details)
    db.session.add(reservation)
    db.session.commit()
    return reservation

# Read
def get_reservations():
    return Reservation.query.all()

def get_reservation_by_id(reservation_id):
    return Reservation.query.get(reservation_id)

# Update
def update_reservation(reservation_id, date, time, details):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        reservation.date = date
        reservation.time = time
        reservation.details = details
        db.session.commit()
        return reservation
    return None

# Delete
def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
        return True
    return False
