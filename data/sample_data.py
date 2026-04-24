# =========================================================
# IMPORTS
# =========================================================

from models.subject import Subject
from models.class_model import ClassModel
from models.teacher import Teacher  # 🔥 NEW

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

# Subject(id, name, lessons_per_week, difficulty_score, double_lessons, requires_lab)

math = Subject(1, "Math", 6, 9, 1)

english = Subject(2, "English", 5, 7, 0)

science = Subject(
    3,
    "Science",
    4,
    8,
    1,
    requires_lab=True  # 🔥 Subject-level lab capability
)


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
# TEACHER DEFINITIONS (🔥 NEW SECTION)
# =========================================================

# Teacher(id, name, subjects, classes, max_lessons, absolute_max)

math_teacher = Teacher(
    id=1,
    name="Mr. John",
    subjects=["Math"],
    classes=["7A"],
    max_lessons_per_week=10,           # Preferred load
    absolute_max_lessons_per_week=15   # 🔥 Hard cap
)

english_teacher = Teacher(
    id=2,
    name="Ms. Mary",
    subjects=["English"],
    classes=["7A"],
    max_lessons_per_week=10,
    absolute_max_lessons_per_week=15
)

science_teacher = Teacher(
    id=3,
    name="Mr. Peter",
    subjects=["Science"],
    classes=["7A"],
    max_lessons_per_week=10,
    absolute_max_lessons_per_week=15
)

# Master teacher list
teachers = [math_teacher, english_teacher, science_teacher]


# =========================================================
# WEEK STRUCTURE
# =========================================================

week_structure = {
    "Monday": 8,
    "Tuesday": 8,
    "Wednesday": 8,
    "Thursday": 8,
    "Friday": 8,
    "Saturday": 4   # 🔥 Short day support
}


# =========================================================
# DAILY TEMPLATES
# =========================================================

# Each entry represents a period slot with its type and duration

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
    Ensures each day's template matches defined number of periods.
    Prevents structural mismatch errors.
    """
    for day, periods in week_structure.items():

        if day not in templates:
            raise ValueError(f"Missing template for {day}")

        if len(templates[day]) != periods:
            raise ValueError(
                f"Template mismatch for {day}: "
                f"expected {periods}, got {len(templates[day])}"
            )


def check_capacity(lesson_blocks, lesson_slots, class_name):
    """
    Checks:
    Required lesson periods vs Available lesson slots

    Handles:
    - Strict mode (stop execution)
    - Flexible mode (warn only)
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
# INITIALIZATION PIPELINE
# =========================================================

def initialize_data():
    """
    Full system setup pipeline:

    1. Validate structure
    2. Generate timeslots
    3. Extract lesson slots
    4. Generate lesson blocks
    5. Check capacity
    """

    # Step 1: Validate templates
    validate_templates(week_structure, templates)

    # Step 2: Generate full timetable grid
    timeslots = generate_timeslots(week_structure, templates)

    # Step 3: Extract usable lesson slots
    lesson_slots = get_lesson_slots(timeslots)

    # Step 4: Generate lesson blocks
    lesson_blocks = generate_lesson_blocks(class_7A)

    # Step 5: Capacity validation
    is_valid, deficit = check_capacity(
        lesson_blocks,
        lesson_slots,
        class_7A.name
    )

    # 🔥 RETURN EVERYTHING NEEDED BY SYSTEM
    return {
        "timeslots": timeslots,
        "lesson_slots": lesson_slots,
        "lesson_blocks": lesson_blocks,
        "teachers": teachers,      # 🔥 NEW
        "capacity_ok": is_valid,
        "deficit": deficit         # 🔥 useful for analytics
    }