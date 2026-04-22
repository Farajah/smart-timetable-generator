from models.lesson_block import LessonBlock

# ---------------------------------------------------------
# Converts subject requirements into lesson blocks
# ---------------------------------------------------------
def generate_lesson_blocks(class_obj):
    lesson_blocks = []
    block_id = 1

    # Loop through each subject
    for subject in class_obj.subjects:
        total_lessons = subject.lessons_per_week
        double_lessons = subject.preferred_double_lessons

        # Validate double lessons
        if double_lessons * 2 > total_lessons:
            raise ValueError(f"Invalid double lessons for {subject.name}")

        # Create double lesson blocks
        for _ in range(double_lessons):
            lesson_blocks.append(
                LessonBlock(
                    id=block_id,
                    subject=subject.name,
                    class_id=class_obj.name,
                    block_size=2,
                    requires_lab=subject.requires_lab
                )
            )
            block_id += 1

        # Create remaining single lessons
        remaining = total_lessons - (double_lessons * 2)

        for _ in range(remaining):
            lesson_blocks.append(
                LessonBlock(
                    id=block_id,
                    subject=subject.name,
                    class_id=class_obj.name,
                    block_size=1,
                    requires_lab=subject.requires_lab
                )
            )
            block_id += 1

    return lesson_blocks