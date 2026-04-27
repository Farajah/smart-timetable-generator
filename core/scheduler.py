# =========================================================
# IMPORTS
# =========================================================

from collections import defaultdict


# =========================================================
# HELPER FUNCTION: FIND AVAILABLE TEACHER
# =========================================================

def find_available_teacher(block, slot_ids, teachers):
    """
    Selects the best available teacher for a lesson block.

    PRIORITY ORDER:
    1. Teachers within normal workload (preferred)
    2. Teachers within overload zone (allowed if needed)
    3. Reject if no valid teacher found

    CONDITIONS CHECKED:
    - Subject compatibility
    - Class compatibility
    - Availability (no double booking)
    - Workload constraints
    """

    normal_candidates = []
    overload_candidates = []

    for teacher in teachers:

        # -------------------------------------------------
        # SUBJECT MATCH
        # -------------------------------------------------
        if not teacher.can_teach(block.subject):
            continue

        # -------------------------------------------------
        # CLASS MATCH
        # -------------------------------------------------
        if block.class_id not in teacher.classes:
            continue

        # -------------------------------------------------
        # AVAILABILITY CHECK
        # -------------------------------------------------
        # Must be free for ALL slots (important for doubles)
        if not all(teacher.is_available(slot_id) for slot_id in slot_ids):
            continue

        # -------------------------------------------------
        # WORKLOAD CLASSIFICATION
        # -------------------------------------------------

        if teacher.within_normal_load():
            normal_candidates.append(teacher)

        elif teacher.within_absolute_limit():
            overload_candidates.append(teacher)

        # Beyond absolute max → ignore completely

    # -------------------------------------------------
    # FINAL SELECTION
    # -------------------------------------------------

    if normal_candidates:
        return normal_candidates[0]

    elif overload_candidates:
        return overload_candidates[0]

    return None


# =========================================================
# MAIN FUNCTION: SCHEDULE LESSONS
# =========================================================

def schedule_lessons(lesson_blocks, lesson_slots, teachers):
    """
    CORE SCHEDULER ENGINE

    RESPONSIBILITIES:
    - Assign lesson blocks to time slots
    - Assign teachers to lessons
    - Prevent:
        ✔ Slot conflicts
        ✔ Teacher double-booking
        ✔ Invalid assignments
        ✔ Overloading teachers beyond limits

    NEW FEATURE:
    - Subject distribution control (prevents clustering)
    """

    # -----------------------------------------------------
    # OUTPUT STRUCTURES
    # -----------------------------------------------------

    timetable = {}          # slot_id → LessonBlock
    occupied_slots = set()  # Tracks used slots

    # -----------------------------------------------------
    # 🔥 SUBJECT DISTRIBUTION TRACKER (NEW)
    # -----------------------------------------------------
    # Prevents:
    # Math → Math → Math → Math in same day
    #
    # Structure:
    # subject_daily_count[day][subject] = count
    # -----------------------------------------------------

    subject_daily_count = defaultdict(lambda: defaultdict(int))

    # Maximum times a subject can appear per day
    MAX_PER_SUBJECT_PER_DAY = 2


    # =====================================================
    # MAIN SCHEDULING LOOP
    # =====================================================

    for block in lesson_blocks:

        # =================================================
        # SINGLE LESSON (block_size = 1)
        # =================================================
        if block.block_size == 1:

            for slot in lesson_slots:

                # Skip if slot already occupied
                if slot.id in occupied_slots:
                    continue

                # -------------------------------------------------
                # 🔥 DISTRIBUTION CHECK (ANTI-CLUSTERING)
                # -------------------------------------------------

                current_count = subject_daily_count[slot.day][block.subject]

                if current_count >= MAX_PER_SUBJECT_PER_DAY:
                    continue

                # -------------------------------------------------
                # FIND AVAILABLE TEACHER
                # -------------------------------------------------

                teacher = find_available_teacher(block, [slot.id], teachers)

                if teacher:
                    # Assign lesson to timetable
                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)

                    # -------------------------------------------------
                    # UPDATE DISTRIBUTION TRACKER
                    # -------------------------------------------------
                    subject_daily_count[slot.day][block.subject] += 1

                    # -------------------------------------------------
                    # LINK LESSON BLOCK
                    # -------------------------------------------------
                    block.assign_teacher(teacher)
                    block.assign_slot(slot.id)

                    # -------------------------------------------------
                    # UPDATE TEACHER STATE
                    # -------------------------------------------------
                    teacher.assign_slot(slot.id)
                    teacher.assign_lesson(block)

                    break  # move to next lesson block


        # =================================================
        # DOUBLE LESSON (block_size = 2)
        # =================================================
        elif block.block_size == 2:

            for i in range(len(lesson_slots) - 1):

                slot1 = lesson_slots[i]
                slot2 = lesson_slots[i + 1]

                # -------------------------------------------------
                # CHECK CONSECUTIVE VALID SLOTS
                # -------------------------------------------------

                if (
                    slot1.day == slot2.day and
                    slot2.period == slot1.period + 1 and
                    slot1.id not in occupied_slots and
                    slot2.id not in occupied_slots
                ):

                    # -------------------------------------------------
                    # 🔥 DISTRIBUTION CHECK (DOUBLE LESSON)
                    # -------------------------------------------------

                    current_count = subject_daily_count[slot1.day][block.subject]

                    # Double lesson counts as 2
                    if current_count + 2 > MAX_PER_SUBJECT_PER_DAY:
                        continue

                    slot_ids = [slot1.id, slot2.id]

                    # -------------------------------------------------
                    # FIND TEACHER FOR BOTH SLOTS
                    # -------------------------------------------------

                    teacher = find_available_teacher(block, slot_ids, teachers)

                    if teacher:
                        # Assign both slots
                        timetable[slot1.id] = block
                        timetable[slot2.id] = block

                        occupied_slots.add(slot1.id)
                        occupied_slots.add(slot2.id)

                        # -------------------------------------------------
                        # UPDATE DISTRIBUTION TRACKER
                        # -------------------------------------------------
                        subject_daily_count[slot1.day][block.subject] += 2

                        # -------------------------------------------------
                        # LINK LESSON BLOCK
                        # -------------------------------------------------
                        block.assign_teacher(teacher)
                        block.assign_slot(slot1.id)
                        block.assign_slot(slot2.id)

                        # -------------------------------------------------
                        # UPDATE TEACHER STATE
                        # -------------------------------------------------
                        teacher.assign_slot(slot1.id)
                        teacher.assign_slot(slot2.id)
                        teacher.assign_lesson(block)

                        break  # move to next lesson block

    return timetable