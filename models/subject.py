# Represents a subject and its academic requirements

class Subject:
    def __init__(self, id, name, lessons_per_week, difficulty_score, preferred_double_lessons, requires_lab=False):
        self.id = id
        self.name = name

        # Total number of periods this subject must appear in a week
        self.lessons_per_week = lessons_per_week

        # Difficulty score (used later for scheduling optimization)
        # Higher = harder subject (e.g Math = 9, Art = 3)
        self.difficulty_score = difficulty_score

        # Preferred number of double lessons (soft constraint)
        # Example: 1 means 1 double block (2 consecutive periods)
        self.preferred_double_lessons = preferred_double_lessons

        # Whether this subject sometimes requires a lab
        # (used later for room constraints)
        self.requires_lab = requires_lab