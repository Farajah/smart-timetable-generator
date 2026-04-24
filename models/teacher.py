# Represents a teacher and their teaching capabilities

class Teacher:
    def __init__(self, id, name, subjects, classes, max_lessons_per_week, absolute_max_lessons_per_week):
        self.id = id
        self.name = name

        # List of subject names the teacher can teach
        # e.g ["Math", "Physics"]
        self.subjects = subjects  

        # List of grades the teacher is allowed to teach
        # e.g [1,2,3] for lower primary or [6,7,8] for upper primary
        self.classes = classes 

        # -------------------------------
        # WORKLOAD CONSTRAINTS
        # -------------------------------

        # Preferred workload (ideal limit)
        self.max_lessons_per_week = max_lessons_per_week

        # Absolute limit (safety cap)
        self.absolute_max_lessons_per_week = absolute_max_lessons_per_week

        # -------------------------------
        # RUNTIME TRACKING
        # -------------------------------

        # List of LessonBlocks assigned
        self.assigned_lessons = []

        # Tracks which time slots teacher is already booked in
        self.occupied_slots = set()

        # ---------------------------------------------------------
    # BASIC CHECKS
    # ---------------------------------------------------------

    def can_teach(self, subject):
        """
        Check if teacher is qualified to teach the subject
        """
        return subject in self.subjects

    def is_available(self, slot_id):
        """
        Check if teacher is free at a given slot
        """
        return slot_id not in self.occupied_slots

    # ---------------------------------------------------------
    # WORKLOAD LOGIC
    # ---------------------------------------------------------

    def workload(self):
        """
        Current number of assigned lessons
        """
        return len(self.assigned_lessons)

    def within_normal_load(self):
        """
        ✔ Preferred zone
        Teacher is still under ideal workload
        """
        return self.workload() < self.max_lessons_per_week

    def within_absolute_limit(self):
        """
        ⚠ Overload zone (allowed but not ideal)
        Teacher can still be used if necessary
        """
        return self.workload() < self.absolute_max_lessons_per_week

    def is_overloaded(self):
        """
        Detect if teacher is beyond preferred workload
        Useful for analytics later
        """
        return self.workload() > self.max_lessons_per_week

    # ---------------------------------------------------------
    # ASSIGNMENT METHODS
    # ---------------------------------------------------------

    def assign_slot(self, slot_id):
        """
        Mark a slot as occupied by the teacher
        Prevents double booking
        """
        self.occupied_slots.add(slot_id)

    def assign_lesson(self, lesson_block):
        """
        Assign a lesson block to teacher
        """
        self.assigned_lessons.append(lesson_block)