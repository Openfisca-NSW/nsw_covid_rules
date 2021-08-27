from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Person

# Details directions specific to the Greater Sydney area, detailed in Part 5.


class in_Greater_Sydney(Variable):
    value_type = bool
    entity = Person
    default_value = False
    definition_period = ETERNITY
    label = 'Is the address in Greater Sydney?'
