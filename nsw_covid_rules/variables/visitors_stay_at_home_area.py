from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable


class ReasonsForVisitingStayAtHomeArea(Enum):
    to_carry_out_work = 'to carry out work, including work done by a volunteer or charitable organisation'
    to_help_with_move = 'To help with moving to or from a place of residence'
    childcare_or_family = 'For childcare or family contact arrangements'
    emergency_or_avoiding_illness = 'Because of an emergency or to avoid an'\
                                    'injury, illness or risk of harm'
    to_attend_a_significant_event = 'To attend a significant event, such as a'\
                                    'wedding, or a gathering following a funeral'\
                                    'or memorial service'
    for_a_friends_bubble = 'to participate in a nominated friends bubble'
    for_compassionate_reasons = 'For compassionate reasons; including where 2'\
        'people in a relationship live apart'
    as_nominated_visitor = 'As the nominated visitor'
    inspect_property = 'To inspect the property ahead of a lease, sale or attend'\
        'an auction of the residence.'
    provide_care_or_assistance = 'To provide care or assistance to a vulnerable person'
    other = 'Other'


class reasons_for_visiting_stay_at_home_area(Variable):
    value_type = Enum
    possible_values = ReasonsForVisitingStayAtHomeArea
    default_value = ReasonsForVisitingStayAtHomeArea.other
    entity = Person
    definition_period = ETERNITY
    label = 'What is the reason for the visit?'
    reference = "variable-type: question"


class permitted_for_visiting_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the visitor permitted to visit general area?'
    reference = "variable-type: output"

    def formula(persons, period, parameters):
        reason_for_visiting_stay_at_home_area = persons('reasons_for_visiting_stay_at_home_area', period)
        Reason = reason_for_visiting_stay_at_home_area.possible_values
        visitor_household_vaccinated = persons('visitor_household_vaccinated', period)
        member_of_another_nominated_friends_bubble = persons('member_of_another_nominated_friends_bubble', period)
        living_in_same_area_or_within_distance = persons('living_in_same_area_or_within_distance', period)
        return select([reason_for_visiting_stay_at_home_area == Reason.to_carry_out_work,
                    reason_for_visiting_stay_at_home_area == Reason.to_help_with_move,
                    reason_for_visiting_stay_at_home_area == Reason.childcare_or_family,
                    reason_for_visiting_stay_at_home_area == Reason.emergency_or_avoiding_illness,
                    reason_for_visiting_stay_at_home_area == Reason.to_attend_a_significant_event,
                    reason_for_visiting_stay_at_home_area == Reason.for_a_friends_bubble,
                    reason_for_visiting_stay_at_home_area == Reason.for_compassionate_reasons,
                    reason_for_visiting_stay_at_home_area == Reason.as_nominated_visitor,
                    reason_for_visiting_stay_at_home_area == Reason.inspect_property,
                    reason_for_visiting_stay_at_home_area == Reason.provide_care_or_assistance,
                    reason_for_visiting_stay_at_home_area == Reason.other],
                     [persons('worker_permitted_stay_at_home_area', period),
                     True,
                     True,
                     True,
                     True,
                     household_vaccinated * living_in_same_area_or_within_distance
                     * visitor_household_vaccinated
                     * member_of_another_nominated_frends_bubble
                     * not_(member_of_another_nominated_friends_bubble),
                     True,
                     True,
                     True,
                     True])
