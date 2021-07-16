class InputInvalidError(Exception):
    """Exception raised for invalid input type.

    Attributes:
        obj -- object name that is causing the error
        message -- explanation of the error
    """

    def __init__(self, obj, message="Invalid input: "):
        self.obj = obj
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message + self.obj
