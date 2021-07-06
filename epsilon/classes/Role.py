from enum import Enum


class Role(Enum):
    TEAM_OWNER = 1
    TEAM_ADMIN = 2
    TEAM_MEMBER = 3

    def __str__(self):
        """ Overloads str method. """
        return 'Role(rid = ' + str(self.value) \
            + ', role_type = ' + self.name + ')'
