from enum import Enum


class Type(Enum):
    STARTUP_USER = 1
    SERVICE_PROVIDER = 2
    ADMIN = 3

    def __str__(self):
        """ Overloads str method. """
        return 'Type(type_id = ' + str(self.value) \
            + ', user_type = ' + self.name + ')'
