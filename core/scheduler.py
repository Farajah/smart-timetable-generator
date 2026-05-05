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
    # WEEKLY SUBJECT TRACKER (NEW)
    # =====================================================
    subject_weekly_count = defaultdict(int)

    # Count required lessons per subject
    subject_required_count = defaultdict(int)
    for block in lesson_blocks:
        subject_required_count[block.subject] += block.block_size

    # =====================================================
    # DAY LOAD TRACKER
    # =====================================================
    day_load = defaultdict(int)

    # =====================================================
    # SUBJECT GAP TRACKER
    # =====================================================
    subject_last_period = defaultdict(lambda: defaultdict(lambda: -100))
    MIN_GAP = 1

    # =====================================================
    # SHUFFLE SLOTS (ANTI FRONT-LOADING)
    # =====================================================
    lesson_slots_copy = lesson_slots[:]
    shuffle(lesson_slots_copy)

    # =====================================================
    # SORT BLOCKS BY DEMAND (NEW)
    # =====================================================
    sorted_blocks = sorted(
        lesson_blocks,
        key=lambda b: (
            -b.block_size,                        # doubles first
            -subject_required_count[b.subject]    # high demand subjects first
        )
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
        #  DYNAMIC SLOT SORTING (CRITICAL FIX)
        # =================================================
        # Re-sort every time based on CURRENT day load
        # This ensures real balancing during scheduling
        # =================================================
        lesson_slots_dynamic = sorted(
            lesson_slots_copy,
            key=lambda s: (day_load[s.day], s.period)
        )


        # =================================================
        # SINGLE LESSON
        # =================================================
        if block.block_size == 1:

            for slot in lesson_slots_dynamic:

                if slot.id in occupied_slots:
                    continue

                # DAILY LIMIT
                if subject_daily_count[slot.day][block.subject] >= MAX_PER_SUBJECT_PER_DAY:
                    continue

                # GAP CONTROL
                last_period = subject_last_period[slot.day][block.subject]
                if slot.period - last_period < MIN_GAP:
                    continue

                # =================================================
                #  WEEKLY LIMIT CHECK (NEW)
                # =================================================
                if subject_weekly_count[block.subject] >= subject_required_count[block.subject]:
                    continue

                teacher = find_available_teacher(block, [slot.id], teachers)

                if teacher:
                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)

                    # UPDATE TRACKERS
                    subject_daily_count[slot.day][block.subject] += 1
                    subject_weekly_count[block.subject] += 1   # 🔥 NEW
                    day_load[slot.day] += 1

                    subject_last_period[slot.day][block.subject] = slot.period

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

                    if subject_daily_count[slot1.day][block.subject] >= MAX_PER_SUBJECT_PER_DAY:
                        continue

                    # GAP CONTROL
                    last_period = subject_last_period[slot1.day][block.subject]
                    if slot1.period - last_period < MIN_GAP:
                        continue

                    # =================================================
                    # PHASE 1: WEEKLY LIMIT CHECK (NEW)
                    # =================================================
                    if subject_weekly_count[block.subject] + 2 > subject_required_count[block.subject]:
                        continue

                    # =====================================================
                    # EARLY DOUBLE BIAS
                    # Avoid late-day double lessons
                    # =====================================================
                    if slot1.period > 6:
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
                        subject_weekly_count[block.subject] += 2  
                        double_lessons_per_day[slot1.day] += 1
                        day_load[slot1.day] += 2

                        subject_last_period[slot1.day][block.subject] = slot2.period

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

        # =================================================
        # SORTED SLOTS IN SECOND PASS
        # =================================================
        sorted_slots = sorted(
            lesson_slots,
            key=lambda s: (day_load[s.day], s.period)
        )

        if block.block_size == 1:

            for slot in sorted_slots:

                if slot.id in occupied_slots:
                    continue

                teacher = find_available_teacher(block, [slot.id], teachers)

                if teacher:
                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)

                    subject_weekly_count[block.subject] += 1

                    block.assign_teacher(teacher)
                    block.assign_slot(slot.id)

                    teacher.assign_slot(slot.id)
                    teacher.assign_lesson(block)
                    break

        elif block.block_size == 2:

            for i in range(len(sorted_slots) - 1):

                slot1 = sorted_slots[i]
                slot2 = sorted_slots[i + 1]

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

                        subject_weekly_count[block.subject] += 2

                        block.assign_teacher(teacher)
                        block.assign_slot(slot1.id)
                        block.assign_slot(slot2.id)

                        teacher.assign_slot(slot1.id)
                        teacher.assign_slot(slot2.id)
                        teacher.assign_lesson(block)
                        break

            # =====================================================
    # DEBUG: PHASE 1 WEEKLY TRACKING CHECK
    # =====================================================

    print("\n========== PHASE 1 DEBUG ==========")

    print("\n--- REQUIRED LESSONS PER SUBJECT ---")
    for subject, count in subject_required_count.items():
        print(f"{subject}: {count}")

    print("\n--- SCHEDULED LESSONS PER SUBJECT ---")
    for subject, count in subject_weekly_count.items():
        print(f"{subject}: {count}")

    print("\n--- DIFFERENCE (SHOULD BE ZERO) ---")
    for subject in subject_required_count:
        required = subject_required_count[subject]
        scheduled = subject_weekly_count.get(subject, 0)
        print(f"{subject}: {required - scheduled}")

    print("====================================\n")

    return timetable