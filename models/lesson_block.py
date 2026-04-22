# Represents a schedulable unit (single or double lesson)

class LessonBlock:
    def __init__(self, id, subject, class_id, block_size, requires_lab=False):
        self.id = id

        # Subject name (e.g "Math")
        self.subject = subject

        # Class this lesson belongs to (e.g "7A")
        self.class_id = class_id

        # Size of block:
        # 1 = single lesson
        # 2 = double lesson (must occupy 2 consecutive periods)
        self.block_size = block_size

        # Whether this specific block may require a lab
        self.requires_lab = requires_lab