from openfisca_core.indexed_enums import Enum
from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable

import numpy as np

# details 1. eligibility and reasons to get a permit to leave Greater Sydney,
# 2. requirements to get such permit,
# 3. eligibility and reasons to get a permit to be a nominated visitor,
# 4. when gazetted, eligibility and reasons to get a permit to leave the area of concern.

# below section deals with whether a person requires a permit to go to work,
# under Clause 4.3 and Clause 4.3A.


class person_requires_permit_for_work(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person required to acquire a permit from Service NSW to go to work?'

    def formula(persons, period, parameters):
        category_of_area = persons('person_category_of_area', period)
        CategoryOfArea = (category_of_area.possible_values)
        in_area_of_concern = (category_of_area == CategoryOfArea.area_of_concern)
        is_authorised_worker = persons('is_authorised_worker', period)
        leaving_area_of_concern = persons('is_leaving_area_of_concern', period)
        is_entering_area_of_concern = persons('is_entering_area_of_concern', period)
        is_providing_emergency_services = persons('is_providing_emergency_services', period)
        return ((in_area_of_concern * is_authorised_worker * leaving_area_of_concern * np.logical_not(is_providing_emergency_services))
                + (is_entering_area_of_concern * np.logical_not(is_providing_emergency_services)))


class is_authorised_worker(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person an authorised worker?'


class is_leaving_area_of_concern(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person leaving an area of concern?'


class is_entering_area_of_concern(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person leaving an area of concern?'


class is_providing_emergency_services(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person providing emergency services?'


# code related to being nominated as a visitor, within section 4.13 (3)

class is_eligible_to_be_nominated_person(Variable):
    value_type = bool
    default_value = False
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

# code relating to permit requirements for entering and leaving Greater Sydney,
# within Clause 5.4


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
    carrying_out_work_less_than_50kms_from_Sydney = 'Person is carrying out work less than 50 kilometres' \
                                                    'from Greater Sydney.'  # 5.4(1)(b)
    carrying_out_work_more_than_50kms_from_Sydney = 'Person is carrying out work more than 50 kilometres' \
                                                    'from Greater Sydney.'  # 5.4(1)(b)
    carrying_out_emergency_work = 'Person is carrying out work involving the provision of an emergency service.'
    no_valid_reason = 'Person does not have a valid reason to leave Greater Sydney.'


class greater_sydney_permit_reasons(Variable):
    value_type = Enum
    entity = Person
    definition_period = ETERNITY
    possible_values = PermitReasonsGreaterSydney
    default_value = PermitReasonsGreaterSydney.no_valid_reason
    label = 'Permitted reasons for leaving Greater Sydney'


class person_requires_permit_to_leave_Greater_Sydney(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    default_value = True
    label = 'Does the person require a permit to leave Greater Sydney?'

    def formula(persons, period, parameters):
        permit_reasons = persons('greater_sydney_permit_reasons', period)
        PermitReasonsGreaterSydney = (permit_reasons.possible_values)
        working_less_than_50kms_from_Sydney = (permit_reasons == PermitReasonsGreaterSydney.carrying_out_work_less_than_50kms_from_Sydney)
        carrying_out_emergency_work = (permit_reasons == PermitReasonsGreaterSydney.carrying_out_emergency_work)
        no_valid_reason = (permit_reasons == PermitReasonsGreaterSydney.no_valid_reason)
        return np.logical_not(working_less_than_50kms_from_Sydney
                              + carrying_out_emergency_work
                              + no_valid_reason)


class person_is_allowed_to_leave_Greater_Sydney(Variable):
    value_type = bool
    entity = Person
    definition_period = DAY
    default_value = False
    label = 'Is the person allowed to leave Greater Sydney?'

    def formula(persons, period, parameters):
        permit_reasons = persons('greater_sydney_permit_reasons', period)
        PermitReasonsGreaterSydney = (permit_reasons.possible_values)
        relocating_to_new_place_of_residence = (permit_reasons == PermitReasonsGreaterSydney.relocating_new_place_of_residence)
        move_between_place_of_residence_for_work = (permit_reasons == PermitReasonsGreaterSydney.move_between_place_of_residence_for_work)
        move_between_place_of_residence_for_repairs = (permit_reasons == PermitReasonsGreaterSydney.move_between_place_of_residence_for_repairs)
        move_between_place_of_residence_for_animal_welfare = (permit_reasons == PermitReasonsGreaterSydney.inspect_new_place_of_residence)
        working_less_than_50kms_from_Sydney = (permit_reasons == PermitReasonsGreaterSydney.carrying_out_work_less_than_50kms_from_Sydney)
        working_more_than_50kms_from_Sydney = (permit_reasons == PermitReasonsGreaterSydney.carrying_out_work_more_than_50kms_from_Sydney)
        carrying_out_emergency_work = (permit_reasons == PermitReasonsGreaterSydney.carrying_out_emergency_work)
        return (relocating_to_new_place_of_residence
                + move_between_place_of_residence_for_work
                + move_between_place_of_residence_for_repairs
                + move_between_place_of_residence_for_animal_welfare
                + working_less_than_50kms_from_Sydney
                + working_more_than_50kms_from_Sydney
                + carrying_out_emergency_work)
