
def schedule_lessons(lesson_blocks, lesson_slots):
    
    timetable = {}
    occupied_slots = set()

    for block in lesson_blocks:

        # -------------------------------
        # SINGLE LESSON
        # -------------------------------
        if block.block_size == 1:

            for slot in lesson_slots:
                if slot.id not in occupied_slots:

                    timetable[slot.id] = block
                    occupied_slots.add(slot.id)
                    break

        # -------------------------------
        # DOUBLE LESSON
        # -------------------------------
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
                    timetable[slot1.id] = block
                    timetable[slot2.id] = block

                    occupied_slots.add(slot1.id)
                    occupied_slots.add(slot2.id)
                    break

    return timetable