# =========================================================
# SMART BLOCK ORDERING ENGINE
# =========================================================
# PURPOSE:
# Reorders lesson blocks BEFORE scheduling to:
#
# ✔ Prevent subject clustering (e.g. all Math on Monday)
# ✔ Spread subjects across the week
# ✔ Improve overall timetable quality
#
# STRATEGY:
# Round-robin distribution across subjects
# =========================================================

from collections import defaultdict


def smart_order_blocks(lesson_blocks):
    """
    Reorders lesson blocks using round-robin logic.

    INPUT:
        [Math, Math, Math, English, English, Science...]

    OUTPUT:
        [Math, English, Science, Math, English, Science...]
    """

    # -----------------------------------------------------
    # STEP 1: GROUP BLOCKS BY SUBJECT
    # -----------------------------------------------------
    subject_groups = defaultdict(list)

    for block in lesson_blocks:
        subject_groups[block.subject].append(block)

    # -----------------------------------------------------
    # STEP 2: ROUND-ROBIN EXTRACTION
    # -----------------------------------------------------
    # Take 1 block per subject at a time
    # until all blocks are exhausted
    # -----------------------------------------------------

    ordered_blocks = []

    while any(subject_groups.values()):
        for subject in list(subject_groups.keys()):
            if subject_groups[subject]:
                ordered_blocks.append(subject_groups[subject].pop(0))

    return ordered_blocks