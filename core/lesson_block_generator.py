# =========================================================
# LESSON BLOCK GENERATOR
# =========================================================
# Purpose:
# Converts subject weekly requirements into schedulable units
# ("lesson blocks") that the scheduler can place into timetables.
#
# Each lesson block represents either:
# - A single lesson (1 period)
# - A double lesson (2 consecutive periods)
# =========================================================


from models.lesson_block import LessonBlock


# =========================================================
# MAIN FUNCTION: GENERATE LESSON BLOCKS
# =========================================================

def generate_lesson_blocks(class_obj):
    """
    Transforms subject requirements into atomic scheduling units.

    Example:
    Math (6 lessons/week, 2 double lessons)
    → 2 blocks of size 2 + 2 blocks of size 1
    """

    lesson_blocks = []
    block_id = 1

    # =====================================================
    # LOOP THROUGH ALL SUBJECTS IN CLASS
    # =====================================================

    for subject in class_obj.subjects:

        total_lessons = subject.lessons_per_week
        double_lessons = subject.preferred_double_lessons

        # -------------------------------------------------
        # VALIDATION: DOUBLE LESSON CONSTRAINT
        # -------------------------------------------------
        # Ensures we do not allocate more double lessons
        # than available teaching time allows
        # -------------------------------------------------

        if double_lessons * 2 > total_lessons:
            raise ValueError(
                f"Invalid configuration for {subject.name}: "
                f"double lessons exceed total weekly lessons"
            )

        # =================================================
        # STEP 1: CREATE DOUBLE LESSON BLOCKS
        # =================================================
        # Each block represents 2 consecutive periods
        # =================================================

        for _ in range(double_lessons):

            lesson_blocks.append(
                LessonBlock(
                    id=block_id,
                    subject=subject.name,
                    class_id=class_obj.name,
                    block_size=2,

                    # 🔥 Derived flag for easier logic downstream
                    is_double=True,

                    requires_lab=subject.requires_lab
                )
            )

            block_id += 1

        # =================================================
        # STEP 2: CREATE SINGLE LESSON BLOCKS
        # =================================================
        # Remaining lessons after allocating double lessons
        # =================================================

        remaining = total_lessons - (double_lessons * 2)

        for _ in range(remaining):

            lesson_blocks.append(
                LessonBlock(
                    id=block_id,
                    subject=subject.name,
                    class_id=class_obj.name,
                    block_size=1,

                    # Single lesson flag
                    is_double=False,

                    requires_lab=subject.requires_lab
                )
            )

            block_id += 1

    return lesson_blocks