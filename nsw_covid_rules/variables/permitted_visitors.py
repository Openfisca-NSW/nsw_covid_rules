from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable


class is_prescribed_work(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work relating to (a) cleaning, (b) repairs and maintenance'\
            '(c) alterations and additions to persons'\
            '(d) work carried out as part of a trade, including electrical'\
            'work or plumbing'


class is_prescribed_work_permitted(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the prescribed work necessary to be carried out?'

    def formula(persons, period, parameters):
        is_prescribed_work = persons('is_prescribed_work', period)
        work_required_for_health_and_safety = persons('work_required_for_health_and_safety', period)
        work_required_for_emergency = persons('work_required_for_emergency', period)
        work_required_for_essential_utility = persons('work_required_for_essential_utility', period)
        work_required_for_fire_protection = persons('work_required_for_fire_protection', period)
        return is_prescribed_work and (work_required_for_health_and_safety
        or work_required_for_emergency or work_required_for_essential_utility
        or work_required_for_fire_protection or work_required_for_cleaning_or_repairs)


class work_required_for_health_and_safety(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work urgently required to be carried out to ensure the'\
            'health, safety or security of the place of residence'\
            'or persons residing at the place of residence'


class work_required_for_emergency(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work urgently required to be carried out because of an'\
            'emergency?'


class work_required_for_essential_utility(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work required for the installation, maintenance or repair of'\
            'an essential utility?'


class work_required_for_fire_protection(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work required for fire protection and safety?'


class work_required_for_cleaning_or_repairs(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'for prescribed work that is cleaning or repairs and maintenance'\
            'at a place of residence that is unoccupied when the work is being'\
            'carried out'


class work_required_for_sale_and_lease(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'for prescribed work that is cleaning or repairs and maintenance'\
            'because it is necessary for the sale or lease of the place of'\
            'residence carried out'
