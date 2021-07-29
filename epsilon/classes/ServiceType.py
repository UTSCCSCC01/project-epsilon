from enum import Enum


class ServiceType(Enum):
    PRODUCT_DEVELOPMENT = 1
    ACCOUNTING_AND_BOOKKEEPING = 2
    LEGAL = 3
    MARKETING = 4
    SALES_AND_CRM = 5

    def __str__(self):
        """ Overloads str method. """
        return 'ServiceType(ser_type_id = ' + str(self.value) \
            + ', service_type = ' + self.name + ')'
