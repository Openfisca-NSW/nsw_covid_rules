from openfisca_core.indexed_enums import Enum
from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable

# details 1. eligibility and reasons to get a permit to leave Greater Sydney,
# 2. requirements to get such permit,
# 3. eligibility and reasons to get a permit to be a nominated visitor,
# 4. when gazetted, eligibility and reasons to get a permit to leave the area of concern.


class PermitReasonsGreaterSydney(Enum):
    relocating_new_place_of_residence = 'Person is relocating to a new place' \
                                        'of residence outside Greater Sydney.'  # 5.4(1)(a)(i)
    move_between_place_of_residence_for_work = 'Person moves between places of' \
                                               ' residence for work, where only' \
                                               ' the person moves to the other place of residence.'  # 5.4(1)(a)(ii)
    move_between_place_of_residence_for_repairs = 'Person moves between places of' \
                                                  ' residence for urgent maintenance or repairs.'
    move_between_place_of_residence_for_animal_welfare = 'Person moves between places of' \
                                                         ' residence for animal welfare.'
    inspect_new_place_of_residence = 'Person is inspecting residential property' \
                                     ' as potential place of residence, with the ' \
                                     ' intent to reside outside Greater Sydney as soon' \
                                     ' as is practicable.'  # 5.4(1)(a)(iii)
    carrying_out_work = 'Person is carrying out work more than 50 kilometres' \
                        'from Greater Sydney.'  # 5.4(1)(b)
    carrying_out_emergency_work = 'Person is carrying out work involving the provision of an emergency service.'
    no_valid_reason = 'Person does not have a valid reason to leave Greater Sydney.'


class PermitReasonsGreaterSydney(Variable):
    value_type = Enum
    entity = Person
    definition_period = ETERNITY
    possible_values = PermitReasonsGreaterSydney
    default_value = PermitReasonsGreaterSydney.no_valid_reason
    label = 'Permitted reasons for leaving Greater Sydney'


class is_eligible_to_be_nominated_person(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person is eligible to be a nominated visitor for another person and' \
            'may apply for a Service NSW issued permit'

    def formula(persons, period, parameters):
        return (
            persons('noPersonNominated', period)
            and persons('notNomatedForAnotherPerson', period)
            and persons('livingWithinFiveKm', period)
            )


class noPersonNominated(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = 'No other individual has been a nominated visitor for the person'


class notNomatedForAnotherPerson(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = 'Individual has not been a nominated visitor for another person'


class livingWithinFiveKm(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = 'Nominated individual resides within 5km of the place of residence'


class is_nominated_person(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    label = 'The person has been issued a nominated person permit by Service NSW'
