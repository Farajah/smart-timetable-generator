# ---------------------------------------------------------
# MAIN ENTRY POINT OF THE TIMETABLE SYSTEM
# ---------------------------------------------------------
# This file orchestrates the full flow:
# 1. Initialize data (validation + generation)
# 2. Run scheduler
# 3. Display timetable output
# ---------------------------------------------------------


# Import the centralized initialization pipeline
from core.sample_data import initialize_data

# Import the scheduling engine
from core.scheduler import schedule_lessons


# ---------------------------------------------------------
# STEP 1: INITIALIZE SYSTEM
# ---------------------------------------------------------
# This performs:
# - Template validation
# - Timeslot generation (full grid)
# - Lesson slot filtering (usable scheduling space)
# - Lesson block generation (what to schedule)
# - Capacity check (Required vs Available)
# ---------------------------------------------------------

data = initialize_data()

# Extract generated components
timeslots = data["timeslots"]          # Full timetable grid (includes breaks, lunch, etc.)
lesson_slots = data["lesson_slots"]    # Only usable lesson slots
lesson_blocks = data["lesson_blocks"]  # All lessons to be scheduled
capacity_ok = data["capacity_ok"]      # Indicates if demand <= supply


# ---------------------------------------------------------
# STEP 2: HANDLE CAPACITY STATUS
# ---------------------------------------------------------
# If capacity is not sufficient:
# - In STRICT_MODE → system would have already stopped
# - In FLEX MODE → we proceed with a warning
# ---------------------------------------------------------

if not capacity_ok:
    print("⚠️ Proceeding with insufficient lesson slots. Some lessons may not be scheduled.\n")


# ---------------------------------------------------------
# STEP 3: RUN SCHEDULER
# ---------------------------------------------------------
# This is the core engine:
# - Assigns lesson blocks to lesson slots
# - Handles single and double lessons
# - Avoids slot conflicts
# ---------------------------------------------------------

timetable = schedule_lessons(lesson_blocks, lesson_slots)


# ---------------------------------------------------------
# STEP 4: DEBUG SUMMARY (SYSTEM OVERVIEW)
# ---------------------------------------------------------
# Helps verify correctness before inspecting full timetable
# ---------------------------------------------------------

print("====================================")
print("SYSTEM SUMMARY")
print("====================================")

# Calculate actual required periods (important fix)
total_required_periods = sum(b.block_size for b in lesson_blocks)

print(f"Total Timeslots: {len(timeslots)}")
print(f"Lesson Slots: {len(lesson_slots)}")
print(f"Lesson Blocks: {len(lesson_blocks)}")
print(f"Total Required Periods: {total_required_periods}")
print(f"Scheduled Periods: {len(timetable)}")


# ---------------------------------------------------------
# STEP 5: DISPLAY GENERATED TIMETABLE
# ---------------------------------------------------------
# Iterates through lesson slots in order
# Prints assigned subject or EMPTY if unassigned
# ---------------------------------------------------------

print("\n====================================")
print("GENERATED TIMETABLE")
print("====================================\n")

for slot in lesson_slots:
    
    # If slot has an assigned lesson
    if slot.id in timetable:
        block = timetable[slot.id]
        subject = block.subject
    else:
        # Slot is empty (can happen if capacity issues exist)
        subject = "FREE"

    print(f"{slot.day} | Period {slot.period} ({slot.start_time}-{slot.end_time}) → {subject}")


# ---------------------------------------------------------
# STEP 6: UNSCHEDULED LESSON TRACKING (IMPORTANT)
# ---------------------------------------------------------
# This helps detect:
# - Capacity shortages
# - Scheduling inefficiencies
# ---------------------------------------------------------

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
        print(f"{block.subject} (Class {block.class_id}, Size {block.block_size})")

else:
    print("\n✅ All lessons successfully scheduled.")

# ---------------------------------------------------------
# TESTING
# ---------------------------------------------------------
#temporary debug (optional)
print("\n--- TIMESLOT CHECK ---")
for slot in timeslots[:5]:
    print(vars(slot))

# Verify lesson blocks
print("\n--- LESSON BLOCK CHECK ---")
for block in lesson_blocks:
    print(vars(block))

# Count Total required periods
total_required = sum(b.block_size for b in lesson_blocks)
print("TOTAL REQUIRED PERIODS:", total_required)

# Check if scheduling is logically correct
# Check 1: No slot overlap
print("\n--- SLOT UNIQUENESS CHECK ---")
print(len(timetable) == len(set(timetable.keys())))