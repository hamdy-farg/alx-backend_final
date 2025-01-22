from extension import socketio
from models import RoomModel, BookModel
from datetime import datetime
from models import StatusEnum, RoleEnum
from schema import (
    DATEFORMAT,
    TIMEFORMAT,
)


class BookingService:
    def get_rejected_and_unselected_time(self, room_id: str, date: str):
        """Get time slots that are rejected or not selected.

        - ARGUMENTS
            - room_id as string
            - date as string
        - RETURN
            - success: List of rejected or unselected time slots
            - fail: dict {
                code: int,
                message: str,
                status: bool
            }
        """
        room = RoomModel.query.filter(RoomModel.id == room_id).first()
        if room is None:
            abort(404, message="Room with this ID not found")

        try:
            date = datetime.strptime(date, DATEFORMAT).date()
        except Exception:
            abort(403, message="Invalid date format")

        if date < datetime.now().date():
            abort(401, message="You cannot select a date in the past")
        if date > room.end_date or date < room.start_date:
            abort(401, message="Invalid date, selection is out of range")

        # Default available time range for the room
        default_start_time = room.start_time
        default_end_time = room.end_time
        default_slots = [(default_start_time, default_end_time)]

        # Retrieve approved and in-progress bookings
        active_bookings = BookModel.query.filter(
            BookModel.room_id == room.id,
            BookModel.date == date,
            BookModel.status.in_([StatusEnum.approved, StatusEnum.inProgress]),
        ).all()

        # Subtract active bookings from the default available time
        available_slots = default_slots
        for booking in active_bookings:
            new_slots = []
            for start, end in available_slots:
                if booking.start_time >= end or booking.end_time <= start:
                    # No overlap
                    new_slots.append((start, end))
                else:
                    # Split the slot to remove the booked time
                    if start < booking.start_time:
                        new_slots.append((start, booking.start_time))
                    if end > booking.end_time:
                        new_slots.append((booking.end_time, end))
            available_slots = new_slots

        # Retrieve rejected bookings
        rejected_bookings = BookModel.query.filter(
            BookModel.room_id == room.id,
            BookModel.date == date,
            BookModel.status == StatusEnum.rejected,
        ).all()

        # Extract rejected slots
        rejected_slots = [
            (booking.start_time, booking.end_time) for booking in rejected_bookings
        ]

        # Combine rejected and unselected slots
        all_slots = available_slots + rejected_slots
        all_slots.sort()  # Sort by time for clarity

        return all_slots

    def emit_rejected_and_unselected_time(self, room_id: str, date: str):
        """Emit event to get rejected and unselected time slots for specific hours.

        - ARGUMENTS
            - room_id as string
            - date as string
        - RETURN
            - Void
        """
        slots = self.get_rejected_and_unselected_time(room_id=room_id, date=date)
        formatted_slots = [
            {
                "start_time": slot[0].strftime(TIMEFORMAT),
                "end_time": slot[1].strftime(TIMEFORMAT),
            }
            for slot in slots
        ]

        room_name = f"{room_id}_{date}"
        socketio.emit(
            "availability_updated",
            {"room_id": room_id, "date": date, "slots": formatted_slots},
            to=str(room_name),
        )
