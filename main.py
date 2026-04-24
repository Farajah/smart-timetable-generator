# =========================================================
# MAIN ENTRY POINT OF THE TIMETABLE SYSTEM
# =========================================================
# This file orchestrates the full workflow:
#
# 1. Initialize system data (subjects, classes, teachers, slots)
# 2. Validate constraints + generate lesson blocks
# 3. Run scheduling engine (core AI logic)
# 4. Display final timetable
# 5. Debug + validation checks
# =========================================================


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from data.sample_data import initialize_data
from core.scheduler import schedule_lessons


# =========================================================
# STEP 1: INITIALIZE SYSTEM DATA
# =========================================================
# This function builds the entire dataset:
#
# ✔ Validates templates (structure correctness)
# ✔ Generates full timeslot grid (includes breaks/lunch)
# ✔ Extracts usable lesson slots
# ✔ Generates lesson blocks (what must be scheduled)
# ✔ Creates teacher pool
# ✔ Runs capacity validation (Required vs Available)
# =========================================================

data = initialize_data()

timeslots = data["timeslots"]          # Full weekly grid (lessons + breaks)
lesson_slots = data["lesson_slots"]    # Only usable lesson periods
lesson_blocks = data["lesson_blocks"]  # All lessons to be scheduled
teachers = data["teachers"]            # Teacher pool (critical for scheduling)
capacity_ok = data["capacity_ok"]      # True if demand <= available slots


# =========================================================
# STEP 2: CAPACITY WARNING HANDLING
# =========================================================
# STRICT_MODE (in sample_data.py) controls behavior:
#
# ✔ True  → system stops if overloaded
# ✔ False → system continues but warns user
# =========================================================

if not capacity_ok:
    print(
        "⚠️ WARNING: Insufficient lesson slots detected.\n"
        "Some lessons may not be scheduled properly.\n"
    )


# =========================================================
# STEP 3: RUN SCHEDULING ENGINE (CORE LOGIC)
# =========================================================
# This is the AI-like decision system that:
#
# ✔ Assigns lessons to slots
# ✔ Matches teachers to lessons
# ✔ Prevents conflicts (time + teacher + class)
# ✔ Respects workload constraints
# =========================================================

timetable = schedule_lessons(
    lesson_blocks,
    lesson_slots,
    teachers
)


# =========================================================
# STEP 4: SYSTEM SUMMARY (DIAGNOSTICS)
# =========================================================
# Helps verify system correctness before reviewing output
# =========================================================

print("\n====================================")
print("SYSTEM SUMMARY")
print("====================================")

total_required_periods = sum(block.block_size for block in lesson_blocks)

print(f"Total Timeslots: {len(timeslots)}")
print(f"Lesson Slots: {len(lesson_slots)}")
print(f"Lesson Blocks: {len(lesson_blocks)}")
print(f"Total Required Periods: {total_required_periods}")
print(f"Scheduled Periods: {len(timetable)}")


# =========================================================
# STEP 5: DISPLAY FINAL TIMETABLE
# =========================================================
# Iterates through all lesson slots in order
#
# Shows:
# ✔ Subject assigned
# ✔ OR FREE slot
#
# (Future upgrade: show teacher name here)
# =========================================================

print("\n====================================")
print("GENERATED TIMETABLE")
print("====================================\n")

for slot in lesson_slots:

    block = timetable.get(slot.id)

    if block:
        subject = block.subject

        # OPTIONAL: include teacher name if assigned
        teacher_name = block.teacher.name if block.teacher else "No Teacher"

        print(
            f"{slot.day} | Period {slot.period} "
            f"({slot.start_time}-{slot.end_time}) → "
            f"{subject} ({teacher_name})"
        )
    else:
        print(
            f"{slot.day} | Period {slot.period} "
            f"({slot.start_time}-{slot.end_time}) → FREE"
        )


# =========================================================
# STEP 6: UNSCHEDULED LESSON DETECTION
# =========================================================
# Identifies:
# ✔ Missing assignments
# ✔ Capacity issues
# ✔ Scheduling inefficiencies
# =========================================================

scheduled_blocks = set(timetable.values())

unscheduled_blocks = [
    block for block in lesson_blocks
    if block not in scheduled_blocks
]

if unscheduled_blocks:

    print("\n====================================")
    print("UNSCHEDULED LESSONS")
    print("====================================\n")

    for block in unscheduled_blocks:
        print(
            f"{block.subject} "
            f"(Class {block.class_id}, Size {block.block_size})"
        )

else:
    print("\n✅ All lessons successfully scheduled.")


# =========================================================
# STEP 7: DEBUGGING SECTION (DEVELOPER INSIGHTS)
# =========================================================
# Helps verify internal system correctness
# Remove in production later if needed
# =========================================================

print("\n--- TIMESLOT SAMPLE CHECK ---")
for slot in timeslots[:5]:
    print(vars(slot))


print("\n--- LESSON BLOCK SAMPLE CHECK ---")
for block in lesson_blocks:
    print(vars(block))


# =========================================================
# STEP 8: VALIDATION CHECKS
# =========================================================

total_required = sum(block.block_size for block in lesson_blocks)

print("\nTOTAL REQUIRED PERIODS:", total_required)

print("\n--- SLOT UNIQUENESS CHECK ---")

print(len(timetable) == len(set(timetable.keys())))