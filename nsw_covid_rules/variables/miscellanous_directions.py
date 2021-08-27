from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Person

# miscallenous directions as detailed in


class must_allow_employees_to_work_from_home(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are employers required to allow employees to work from home?'


class must_require_employees_to_work_from_home(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are employees required to work from home?'


class employee_place_of_residence_in_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are employers required to allow ?'
