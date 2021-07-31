from enum import Enum


class RStatus(Enum):
    """
    represents all status of a job application.
    Note: Originally represents all the request status, but Request table is no longer
    being used.
    the lifecycle of an application is:
                                  -> ACCEPTED
                         -> OFFER -
            -> INTERVIEW -        -> DECLINED
    APPLIED -            -> REJECTED (candidate did not pass the interview)
                         -> DECLINED (candidate declined interview request)
            -> REJECTED (candidate did not pass initial screening)
    """
    APPLIED = 1
    INTERVIEW = 2
    OFFER = 3
    ACCEPTED = 4
    DECLINED = 5
    REJECTED = 6

    def __str__(self):
        """ Overloads str method. """
        return 'RStatus(sid = ' + str(self.value) + ', name = ' + self.name + ')'
