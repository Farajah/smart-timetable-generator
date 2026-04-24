# Represents a schedulable unit (single or double lesson)

# models/lesson_block.py

class LessonBlock:
    def __init__(self, id, subject, class_id, block_size, is_double=False, requires_lab=False):
        
        # Unique identifier for the block
        self.id = id
        
        # Subject name (e.g. Math, English)
        self.subject = subject
        
        # Class this lesson belongs to (e.g. 7A)
        self.class_id = class_id
        
        # Number of slots required:
        # 1 = single lesson
        # 2 = double lesson
        self.block_size = block_size
        
        # Boolean flag for double lessons
        self.is_double = is_double

        # Tracks which slots this lesson has been assigned to
        self.scheduled_slot_ids = []

        # Whether this specific block may require a lab
        self.requires_lab = requires_lab

        # assigned teacher (initially None)
        self.teacher = None

    # Assign a teacher to this lesson
    def assign_teacher(self, teacher):
        self.teacher = teacher

    # Record that a slot has been assigned
    def assign_slot(self, slot_id):
        self.scheduled_slot_ids.append(slot_id)

    # Check if lesson is fully scheduled
    def is_scheduled(self):
        return len(self.scheduled_slot_ids) == self.block_size

        