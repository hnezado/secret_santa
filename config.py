class Member:
    def __init__(self, enabled, name, family_id, age, exceptions=None):
        self.enabled = enabled
        self.name = name
        self.family_id = family_id
        self.age = age
        self.exceptions = exceptions

    def __repr__(self):
        return f'Member({self.name})'
