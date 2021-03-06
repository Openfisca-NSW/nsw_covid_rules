from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable


# Main variable for outputing result i.e. if visitors are allowed at premises or not.
class visitors_permitted(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are visitors permitted to visit my place of residence?'
    reference = "variable-type: output"

    def formula(persons, period, parameters):
        category_of_area = persons('LGA_category_of_area', period)
        AREA = category_of_area.possible_values
        in_area_of_concern = (category_of_area == AREA.area_of_concern)
        in_stay_at_home_area = (category_of_area == AREA.stay_at_home_area)
        in_general_area = (category_of_area == AREA.general_area)
        return select(
            [in_area_of_concern,
             in_stay_at_home_area,
             in_general_area],
            [False,
             persons('permitted_for_visiting_stay_at_home_area', period),
             persons('permitted_for_visiting_general_area', period)])


class ReasonsForVisitingGeneralArea(Enum):
    to_carry_out_work = 'to carry out work, including work done by a volunteer'\
                        'or charitable organisation'
    emergency_or_avoiding_illness = 'Because of an emergency or to avoid an'\
                                    'injury, illness or risk of harm'
    to_help_with_move = 'to help a person with moving to or from the place of residence'
    childcare_or_family = 'For childcare or family contact arrangements'
    inspect_property = 'To inspect a residence ahead of a lease, sale or attend'\
        'an auction of the residence.'
    provide_care_or_assistance = 'for carer’s responsibilities, or to provide'\
        'care or assistance to a vulnerable person'
    for_compassionate_reasons = 'for compassionate reasons; including where 2'\
                                'people in a relationship live apart'
    other = 'Social, recreational or other everyday activities'


class reasons_for_visiting_general_area(Variable):
    value_type = Enum
    possible_values = ReasonsForVisitingGeneralArea
    default_value = ReasonsForVisitingGeneralArea.other
    entity = Person
    definition_period = ETERNITY
    label = 'What is the reason for the visit?'
    reference = "variable-type: question"


class permitted_for_visiting_general_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the visitor permitted to visit general area?'
    reference = "variable-type: output"

    def formula(persons, period, parameters):
        reason_for_visiting_general_area = persons('reasons_for_visiting_general_area', period)
        Reason = reason_for_visiting_general_area.possible_values
        visitor_is_vaccinated = persons('visitor_is_vaccinated', period)
        household_vaccinated = persons('household_vaccinated', period)
        return select([reason_for_visiting_general_area == Reason.to_carry_out_work,
                    reason_for_visiting_general_area == Reason.to_help_with_move,
                    reason_for_visiting_general_area == Reason.childcare_or_family,
                    reason_for_visiting_general_area == Reason.emergency_or_avoiding_illness,
                    reason_for_visiting_general_area == Reason.inspect_property,
                    reason_for_visiting_general_area == Reason.for_compassionate_reasons,
                    reason_for_visiting_general_area == Reason.provide_care_or_assistance,
                    reason_for_visiting_general_area == Reason.other],
                     [True,
                     True,
                     True,
                     True,
                     True,
                     True,
                     True,
                     household_vaccinated * visitor_is_vaccinated])
