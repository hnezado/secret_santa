class Member:
    def __init__(self, name, f_id, age, exceptions=None):
        self.name = name
        self.family_id = f_id
        self.age = age
        self.exceptions = exceptions

    def __repr__(self):
        return f'Member({self.name})'
