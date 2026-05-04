# =========================================================
# IMPORTS
# =========================================================

from collections import defaultdict
from random import shuffle


# =========================================================
# HELPER FUNCTION: FIND AVAILABLE TEACHER
# =========================================================

def find_available_teacher(block, slot_ids, teachers):

    normal_candidates = []
    overload_candidates = []

    for teacher in teachers:

        if not teacher.can_teach(block.subject):
            continue

        if block.class_id not in teacher.classes:
            continue

        if not all(teacher.is_available(slot_id) for slot_id in slot_ids):
            continue

        if teacher.within_normal_load():
            normal_candidates.append(teacher)

        elif teacher.within_absolute_limit():
            overload_candidates.append(teacher)

    if normal_candidates:
        return normal_candidates[0]

    elif overload_candidates:
        return overload_candidates[0]

    return None


# =========================================================
# MAIN FUNCTION: SCHEDULE LESSONS
# =========================================================

def schedule_lessons(lesson_blocks, lesson_slots, teachers):

    timetable = {}
    occupied_slots = set()

    # =====================================================
    # SUBJECT DISTRIBUTION TRACKER
    # =====================================================
    subject_daily_count = defaultdict(lambda: defaultdict(int))
    MAX_PER_SUBJECT_PER_DAY = 2

    # =====================================================
    # DOUBLE LESSON TRACKER
    # =====================================================
    double_lessons_per_day = defaultdict(int)
    MAX_DOUBLE_PER_DAY = 2

    # =====================================================
    # DAY LOAD TRACKER
    # =====================================================
    day_load = defaultdict(int)

    # =====================================================
    # SHUFFLE SLOTS (ANTI FRONT-LOADING)
    # =====================================================
    lesson_slots_copy = lesson_slots[:]
    shuffle(lesson_slots_copy)

    # =====================================================
    # SORT BLOCKS (DOUBLE FIRST)
    # =====================================================
    sorted_blocks = sorted(
        lesson_blocks,
        key=lambda b: b.block_size,
        reverse=True
    )

    # =====================================================
    # TRACK UNSCHEDULED
    # =====================================================
    unscheduled_blocks = []

    # =====================================================
    # FIRST PASS
    # =====================================================
    for block in sorted_blocks:

        scheduled = False

        # =================================================
        # 🔥 NEW: DYNAMIC SLOT SORTING (CRITICAL FIX)
        # =================================================
        # Re-sort every time based on CURRENT day load
        # This ensures real balancing during scheduling
        # =================================================
        lesson_slots_dynamic = sorted(
            lesson_slots_copy,
            key=lambda s: day_load[s.day]
        )

        # =================================================
        # SINGLE LESSON
        # =================================================
        if block.block_size == 1:

            for slot in lesson_slots_dynamic:

                if slot.id in occupied_slots:
                    continue

                current_count = subject_daily_count[slot.day][block.subject]

                if current_count >= MAX_PER_SUBJECT_PER_DAY:
                    continue

                teacher = find_available_teacher(block, [slot.id], teachers)

                if teacher:
                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)

                    # UPDATE TRACKERS
                    subject_daily_count[slot.day][block.subject] += 1
                    day_load[slot.day] += 1  # 🔥 USED FOR BALANCING

                    block.assign_teacher(teacher)
                    block.assign_slot(slot.id)

                    teacher.assign_slot(slot.id)
                    teacher.assign_lesson(block)

                    scheduled = True
                    break

        # =================================================
        # DOUBLE LESSON
        # =================================================
        elif block.block_size == 2:

            for i in range(len(lesson_slots_dynamic) - 1):

                slot1 = lesson_slots_dynamic[i]
                slot2 = lesson_slots_dynamic[i + 1]

                if (
                    slot1.day == slot2.day and
                    slot2.period == slot1.period + 1 and
                    slot1.id not in occupied_slots and
                    slot2.id not in occupied_slots
                ):

                    if double_lessons_per_day[slot1.day] >= MAX_DOUBLE_PER_DAY:
                        continue

                    current_count = subject_daily_count[slot1.day][block.subject]

                    if current_count >= MAX_PER_SUBJECT_PER_DAY:
                        continue

                    slot_ids = [slot1.id, slot2.id]

                    teacher = find_available_teacher(block, slot_ids, teachers)

                    if teacher:
                        timetable[slot1.id] = block
                        timetable[slot2.id] = block

                        occupied_slots.add(slot1.id)
                        occupied_slots.add(slot2.id)

                        # UPDATE TRACKERS
                        subject_daily_count[slot1.day][block.subject] += 2
                        double_lessons_per_day[slot1.day] += 1
                        day_load[slot1.day] += 2  # 🔥 BALANCING FIX

                        block.assign_teacher(teacher)
                        block.assign_slot(slot1.id)
                        block.assign_slot(slot2.id)

                        teacher.assign_slot(slot1.id)
                        teacher.assign_slot(slot2.id)
                        teacher.assign_lesson(block)

                        scheduled = True
                        break

        if not scheduled:
            unscheduled_blocks.append(block)

    # =====================================================
    # SECOND PASS (RELAXED)
    # =====================================================
    for block in unscheduled_blocks:

        if block.block_size == 1:

            for slot in lesson_slots:

                if slot.id in occupied_slots:
                    continue

                teacher = find_available_teacher(block, [slot.id], teachers)

                if teacher:
                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)

                    block.assign_teacher(teacher)
                    block.assign_slot(slot.id)

                    teacher.assign_slot(slot.id)
                    teacher.assign_lesson(block)
                    break

        elif block.block_size == 2:

            for i in range(len(lesson_slots) - 1):

                slot1 = lesson_slots[i]
                slot2 = lesson_slots[i + 1]

                if (
                    slot1.day == slot2.day and
                    slot2.period == slot1.period + 1 and
                    slot1.id not in occupied_slots and
                    slot2.id not in occupied_slots
                ):

                    slot_ids = [slot1.id, slot2.id]

                    teacher = find_available_teacher(block, slot_ids, teachers)

                    if teacher:
                        timetable[slot1.id] = block
                        timetable[slot2.id] = block

                        occupied_slots.add(slot1.id)
                        occupied_slots.add(slot2.id)

                        block.assign_teacher(teacher)
                        block.assign_slot(slot1.id)
                        block.assign_slot(slot2.id)

                        teacher.assign_slot(slot1.id)
                        teacher.assign_slot(slot2.id)
                        teacher.assign_lesson(block)
                        break

    return timetable