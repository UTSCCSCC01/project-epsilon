from enum import Enum


class RStatus(Enum):
    ACCEPTED = 1
    REJECTED = 2
    PENDING = 3

    def __str__(self):
        """ Overloads str method. """
        return 'RStatus(sid = ' + str(self.value) + ', name = ' + self.name + ')'
