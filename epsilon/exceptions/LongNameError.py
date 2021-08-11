class LongNameError(Exception):
    """Exception raised for when Name is longer than 6 letters

    Attributes:
        obj -- object name that is causing the error
        message -- explanation of the error
    """

    def __init__(self, message="Please make sure name is not more than 6 letters "):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
