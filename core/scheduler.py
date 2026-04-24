# =========================================================
# HELPER FUNCTION: FIND AVAILABLE TEACHER
# =========================================================

def find_available_teacher(block, slot_ids, teachers):
    """
    Selects the best available teacher for a lesson block.

    Priority:
    1. Teachers within normal workload (preferred)
    2. Teachers within overload zone (but below absolute max)
    3. Reject if no valid teacher found

    Conditions checked:
    - Subject compatibility
    - Class compatibility
    - Availability (no double booking)
    - Workload constraints
    """

    normal_candidates = []
    overload_candidates = []

    for teacher in teachers:

        # ----------------------------
        # SUBJECT MATCH
        # ----------------------------
        if not teacher.can_teach(block.subject):
            continue

        # ----------------------------
        # CLASS MATCH
        # ----------------------------
        if block.class_id not in teacher.classes:
            continue

        # ----------------------------
        # AVAILABILITY CHECK
        # ----------------------------
        # Teacher must be free for ALL slots (important for double lessons)
        if not all(teacher.is_available(slot_id) for slot_id in slot_ids):
            continue

        # ----------------------------
        # WORKLOAD CLASSIFICATION
        # ----------------------------

        # Preferred case: within normal workload
        if teacher.within_normal_load():
            normal_candidates.append(teacher)

        # Acceptable overload (but still under absolute max)
        elif teacher.within_absolute_limit():
            overload_candidates.append(teacher)

        # If beyond absolute max → ignore teacher completely

    # ----------------------------
    # PRIORITY SELECTION
    # ----------------------------

    if normal_candidates:
        return normal_candidates[0]

    elif overload_candidates:
        return overload_candidates[0]

    # No teacher available
    return None


# =========================================================
# MAIN FUNCTION: SCHEDULE LESSONS
# =========================================================

def schedule_lessons(lesson_blocks, lesson_slots, teachers):
    """
    Main scheduling function.

    Responsibilities:
    - Assign lesson blocks to available time slots
    - Assign valid teachers to each lesson
    - Prevent:
        * Slot conflicts
        * Teacher double-booking
        * Invalid subject assignments
        * Exceeding absolute workload

    Supports:
    - Single lessons (1 slot)
    - Double lessons (2 consecutive slots)
    """

    timetable = {}          # slot_id → LessonBlock
    occupied_slots = set()  # tracks used slots

    for block in lesson_blocks:

        # =================================================
        # SINGLE LESSON (block_size = 1)
        # =================================================
        if block.block_size == 1:

            for slot in lesson_slots:

                # Skip if slot already used
                if slot.id in occupied_slots:
                    continue

                # 🔥 Find a valid teacher for this slot
                teacher = find_available_teacher(block, [slot.id], teachers)

                if teacher:
                    # Assign lesson to timetable
                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)

                    # Link lesson block to teacher
                    block.assign_teacher(teacher)
                    block.assign_slot(slot.id)

                    # Update teacher state
                    teacher.assign_slot(slot.id)
                    teacher.assign_lesson(block)

                    # Move to next lesson block
                    break

        # =================================================
        # DOUBLE LESSON (block_size = 2)
        # =================================================
        elif block.block_size == 2:

            for i in range(len(lesson_slots) - 1):

                slot1 = lesson_slots[i]
                slot2 = lesson_slots[i + 1]

                # ----------------------------
                # CHECK CONSECUTIVE SLOTS
                # ----------------------------
                if (
                    slot1.day == slot2.day and
                    slot2.period == slot1.period + 1 and
                    slot1.id not in occupied_slots and
                    slot2.id not in occupied_slots
                ):

                    slot_ids = [slot1.id, slot2.id]

                    # 🔥 Find teacher available for BOTH slots
                    teacher = find_available_teacher(block, slot_ids, teachers)

                    if teacher:
                        # Assign both slots to timetable
                        timetable[slot1.id] = block
                        timetable[slot2.id] = block

                        occupied_slots.add(slot1.id)
                        occupied_slots.add(slot2.id)

                        # Link lesson block
                        block.assign_teacher(teacher)
                        block.assign_slot(slot1.id)
                        block.assign_slot(slot2.id)

                        # Update teacher state
                        teacher.assign_slot(slot1.id)
                        teacher.assign_slot(slot2.id)
                        teacher.assign_lesson(block)

                        break

    return timetable