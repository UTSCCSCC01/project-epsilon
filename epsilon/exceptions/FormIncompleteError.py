class FormIncompleteError(Exception):
    """Exception raised for errors in webpage form missing details.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Some required fields are missing a value. "
                 + "Please fill in all required fields."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
