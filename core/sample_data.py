from models.subject import Subject
from models.class_model import ClassModel
from core.timeslot_generator import generate_timeslots, get_lesson_slots
from core.lesson_block_generator import generate_lesson_blocks


# =========================================================
# CONFIGURATION FLAGS
# =========================================================

# Controls behavior when Required > Available
STRICT_MODE = True   # True → stop execution, False → allow but warn


# =========================================================
# SUBJECT DEFINITIONS
# =========================================================

math = Subject(1, "Math", 6, 9, 1)
english = Subject(2, "English", 5, 7, 0)
science = Subject(3, "Science", 4, 8, 1, requires_lab=True)


# =========================================================
# CLASS DEFINITION
# =========================================================

class_7A = ClassModel(
    id=1,
    name="7A",
    grade=7,
    subjects=[math, english, science]
)


# =========================================================
# WEEK STRUCTURE
# =========================================================

week_structure = {
    "Monday": 8,
    "Tuesday": 8,
    "Wednesday": 8,
    "Thursday": 8,
    "Friday": 8,
    "Saturday": 4
}


# =========================================================
# DAILY TEMPLATES
# =========================================================

daily_template = [
    {"type": "Lesson", "duration": 40},
    {"type": "Lesson", "duration": 40},
    {"type": "Break", "duration": 20},
    {"type": "Lesson", "duration": 40},
    {"type": "Lesson", "duration": 40},
    {"type": "Lunch", "duration": 40},
    {"type": "Lesson", "duration": 40},
    {"type": "Lesson", "duration": 40}
]

saturday_template = [
    {"type": "Lesson", "duration": 40},
    {"type": "Lesson", "duration": 40},
    {"type": "Lesson", "duration": 40},
    {"type": "Lesson", "duration": 40}
]


templates = {
    "Monday": daily_template,
    "Tuesday": daily_template,
    "Wednesday": daily_template,
    "Thursday": daily_template,
    "Friday": daily_template,
    "Saturday": saturday_template
}


# =========================================================
# VALIDATION FUNCTIONS
# =========================================================

def validate_templates(week_structure, templates):
    """
    Ensures that each day's template matches the number of periods defined.
    Prevents index errors during timeslot generation.
    """
    for day, periods in week_structure.items():
        if day not in templates:
            raise ValueError(f"Missing template for {day}")

        if len(templates[day]) != periods:
            raise ValueError(
                f"Template mismatch for {day}: "
                f"expected {periods} slots, got {len(templates[day])}"
            )


def check_capacity(lesson_blocks, lesson_slots, class_name):
    """
    Compares required lesson periods vs available lesson slots.
    Returns deficit if any.
    """
    total_required = sum(block.block_size for block in lesson_blocks)
    total_available = len(lesson_slots)

    if total_required > total_available:
        deficit = total_required - total_available

        message = (
            f"\n⚠️ Capacity Issue Detected for {class_name}\n"
            f"Required Lessons: {total_required}\n"
            f"Available Slots: {total_available}\n"
            f"Deficit: {deficit}\n"
        )

        if STRICT_MODE:
            raise ValueError(message)
        else:
            print(message)

        return False, deficit

    return True, 0


# =========================================================
# INITIALIZATION PIPELINE (SAFE SETUP)
# =========================================================

def initialize_data():
    """
    Runs all setup steps:
    1. Validate templates
    2. Generate timeslots
    3. Extract lesson slots
    4. Generate lesson blocks
    5. Check capacity
    """

    # Step 1: Validate structure
    validate_templates(week_structure, templates)

    # Step 2: Generate full timetable grid
    timeslots = generate_timeslots(week_structure, templates)

    # Step 3: Extract usable lesson slots
    lesson_slots = get_lesson_slots(timeslots)

    # Step 4: Generate lesson blocks for class
    lesson_blocks = generate_lesson_blocks(class_7A)

    # Step 5: Check capacity constraints
    is_valid, deficit = check_capacity(
        lesson_blocks,
        lesson_slots,
        class_7A.name
    )

    return {
        "timeslots": timeslots,
        "lesson_slots": lesson_slots,
        "lesson_blocks": lesson_blocks,
        "capacity_ok": is_valid
    }