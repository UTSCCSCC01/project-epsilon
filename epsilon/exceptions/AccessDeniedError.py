from flask_login import current_user
from collections import defaultdict

class AccessDeniedError(Exception):
    """Exception raised for errors in the current user doesn't
    have the the access right for a certain functionality.

    Attributes:
        curr_user_type -- user type
        functionality -- the functionality that the user has been
        denied access from.
    """

    def __init__(self, functionality=" this page.", role=""):

        self.role = role
        if current_user:
            self.curr_user_type = current_user.type_id
        else:
            self.curr_user_type = 0
        self.functionality = functionality
        user_type_val_to_rep = defaultdict(lambda: "a generic user")
        user_type_val_to_rep[1] = 'startup user'
        user_type_val_to_rep[2] = 'service provider'
        user_type_val_to_rep[3] = 'administrator'
        self.user_type_val_to_rep=user_type_val_to_rep
        super().__init__(self.functionality)

    def __str__(self):
        if len(self.role) != 0:
            return self.role + " does not have the access to " + self.functionality
        return self.user_type_val_to_rep[self.curr_user_type] +" does not have the access to " +self.functionality
