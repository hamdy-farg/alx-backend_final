from extension import socketio
from models import RoomModel, BookModel
from flask_smorest import abort
from datetime import datetime
from models import StatusEnum, RoleEnum
from schema import (
    DATEFORMAT,
    TIMEFORMAT,
)


class BookingService:
    def get_avialable_time(self, room_id: str, date: str):
        """get available time slots to know which time room is available at

        - ARGUMENTS
            - room_id as string
            - date : as string
        - RETURN
            - success: List of avialable room
            - fial: dict{
                code: int,
                message: str,
                satus: bool}
        """
        room = RoomModel.query.filter(RoomModel.id == room_id).first()
        if room is None:
            abort(
                404,
                message="room with this id not found",
            )

        try:
            date = datetime.strptime(date, DATEFORMAT).date()
        except Exception:
            abort(403, message="invalid date formate")
        if date < datetime.now().date():
            abort(
                401,
                message="you can not select date in the past",
            )
        if date > room.end_date or date < room.start_date:
            abort(
                401,
                message="invalid date select is out of range",
            )
        default_start_time = room.start_time
        default_end_time = room.end_time

        bookings = BookModel.query.filter(
            BookModel.room_id == room.id,
            BookModel.date == date,
            BookModel.status == StatusEnum.approved,
            BookModel.status == StatusEnum.inProgress,
        ).all()

        available_slots = [(default_start_time, default_end_time)]
        for booking in bookings:
            new_slots = []
            for start, end in available_slots:
                if booking.start_time >= end or booking.end_time <= start:
                    new_slots.append((start, end))
                else:
                    if start < booking.start_time:
                        new_slots.append((start, booking.start_time))
                    if end > booking.end_time:
                        new_slots.append((booking.end_time, end))
                    available_slots = new_slots
        return available_slots

    def emit_availability_updated(self, room_id: str, date: str):
        """ " emit availability_updated event to get new slots hours update for specific hours
        - ARGUMENTS
            - room_id as string
            - date : as string
        - RETURN
            - Void
        """
        available_slots = BookingService().get_avialable_time(
            room_id=room_id, date=date
        )
        formatted_slots = [
            {
                "start_time": slot[0].strftime(TIMEFORMAT),
                "end_time": slot[1].strftime(TIMEFORMAT),
            }
            for slot in available_slots
        ]

        room_name = f"{room_id}_{date}"
        socketio.emit(
            "availability_updated",
            {"room_id": room_id, "date": date, "available_slots": formatted_slots},
            to=str(room_name),
        )
