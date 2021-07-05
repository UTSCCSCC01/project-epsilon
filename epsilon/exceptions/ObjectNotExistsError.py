class ObjectNotExistsError(Exception):
    """Exception raised for errors in object does not exist in database.

    Attributes:
        obj -- object name that is causing the error
        message -- explanation of the error
    """

    def __init__(self, obj, message=" does not exist."):
        self.obj = obj
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.obj + self.message
