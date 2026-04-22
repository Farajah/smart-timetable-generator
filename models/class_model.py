# Represents a class/stream (e.g., 7A, 7B)

class ClassModel:
    def __init__(self, id, name, grade, subjects):
        self.id = id
        self.name = name # identifies the class (7A, 7B)
        
        # Grade level (used to match with teacher allowed grades)
        self.grade = grade # defines its academic level (7)
        
         # List of Subject objects assigned to this class
        self.subjects = subjects  