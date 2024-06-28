class Member:
    def __init__(self, *args):
        self.enabled = None
        self.name = None
        self.family_id = None
        self.age = None
        self.exceptions = None

        self.__set_values(args)

    def __repr__(self):
        return f'Member({self.name})'

    def __set_values(self, *args):
        """Sets the input data into the instance attributes"""

        params = vars(self)
        for i, param in enumerate(params):
            try:
                setattr(self, param, args[0][i])
            except :
                pass
