class ObjectExistsError(Exception):
    """Exception raised for errors in object already exist in database.

    Attributes:
        obj -- object name that is causing the error
        message -- explanation of the error
    """

    def __init__(self, obj, message=" already exists."):
        self.obj = obj
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.obj + self.message
