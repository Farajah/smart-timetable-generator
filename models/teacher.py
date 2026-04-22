# Represents a teacher and their teaching capabilities

class Teacher:
    def __init__(self, id, name, subjects, allowed_grades, preferred_max_load, absolute_max_load):
        self.id = id
        self.name = name

        # List of subject names the teacher can teach
        # e.g ["Math", "Physics"]
        self.subjects = subjects  

        # List of grades the teacher is allowed to teach
        # e.g [1,2,3] for lower primary or [6,7,8] for upper primary
        self.allowed_grades = allowed_grades 

        # Preferred maximum number of lessons per week (soft constraint)
        self.preferred_max_load = preferred_max_load

        # Absolute maximum lessons (hard limit - should not be exceeded)
        self.absolute_max_load = absolute_max_load