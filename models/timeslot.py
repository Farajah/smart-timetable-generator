# Represents a single time slot in the timetable

class Timeslot:
    def __init__(self, id, day, period, start_time, end_time, duration, slot_type):
        self.id = id

        # Day of the week (e.g "Monday")
        self.day = day

        # Period number (used for scheduling logic)
        self.period = period

        # Start time of the slot (for UI/display)
        self.start_time = start_time

        # End time of the slot
        self.end_time = end_time

        # Duration in minutes
        self.duration = duration

         # Type of slot:
        # "Lesson", "Break", "Lunch", "Cleaning", etc.
        self.slot_type = slot_type  # Lesson, Break, Lunch, etc.