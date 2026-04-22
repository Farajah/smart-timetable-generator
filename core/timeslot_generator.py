from datetime import datetime, timedelta
from models.timeslot import Timeslot

# ---------------------------------------------------------
# FUNCTION: generate_timeslots
# ---------------------------------------------------------
# PURPOSE:
#   Generates all timeslots for the entire school week.
#
# INPUT:
#   week_structure → dictionary defining number of periods per day
#   templates → dictionary mapping each day to its slot structure
#   start_time → string representing when the school day starts
#
# OUTPUT:
#   A list of Timeslot objects covering the whole week
# ---------------------------------------------------------

def generate_timeslots(week_structure, templates, start_time="08:00"):
    
    # This will store all generated timeslots
    timeslots = []
   
    # Unique identifier for each timeslot
    slot_id = 1

    # LOOP THROUGH EACH DAY IN THE WEEK
    for day, periods in week_structure.items():
        
        # Get the time structure (template) for this specific day
        # Example: Monday may include break/lunch, Saturday may not
        template = templates[day]

        # Convert string time to datetime object
        # This allows us to perform time arithmetic (add durations)
        current_time = datetime.strptime(start_time, "%H:%M")

        # LOOP THROUGH EACH PERIOD IN THE DAY
        for period_index in range(periods):
            
            # Get the slot definition for this period
            # Example: {"type": "Lesson", "duration": 40}
            slot = template[period_index]

            # Start time is the current running time
            start = current_time
            end = start + timedelta(minutes=slot["duration"]) # End time is calculated by adding duration to start time

             # CREATE A TIMESLOT OBJECT
            timeslots.append(
                Timeslot(
                    id=slot_id,
                    day=day,
                    period=period_index + 1,
                    start_time=start.strftime("%H:%M"),
                    end_time=end.strftime("%H:%M"),
                    duration=slot["duration"],
                    slot_type=slot["type"]
                )
            )

            # ensures next slot starts where this one ends
            current_time = end
            # Increment slot ID for uniqueness
            slot_id += 1

    return timeslots # Return the full list of generated timeslots


# ---------------------------------------------------------
# FUNCTION: get_lesson_slots
# ---------------------------------------------------------
# PURPOSE:
#   Filters and returns only "Lesson" slots.
#
# WHY:
#   The scheduler should ONLY assign lessons to valid lesson slots.
#   Other slots (Break, Lunch, Cleaning) are not schedulable.
#
# INPUT:
#   timeslots → full list of all generated timeslots
#
# OUTPUT:
#   List of timeslots where slot_type == "Lesson"
# ---------------------------------------------------------
def get_lesson_slots(timeslots):
    return [slot for slot in timeslots if slot.slot_type == "Lesson"]