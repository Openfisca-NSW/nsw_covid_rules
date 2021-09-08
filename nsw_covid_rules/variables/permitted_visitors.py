from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable


# Main variable for outputing result i.e. if visitors are allowed at premises or not.
class are_visitors_permitted(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are visitors permitted to visit my place of residence?'

    def formula(persons, period, parameters):
        category_of_area = persons('category_of_area', period)
        AREA = category_of_area.possible_values
        in_area_of_concern = (category_of_area == AREA.area_of_concern)
        in_stay_at_home_area = (category_of_area == AREA.stay_at_home_area)
        in_general_area = (category_of_area == AREA.general_area)
        return select(
            [in_area_of_concern,
             in_stay_at_home_area,
             in_general_area],
            [persons('visitors_permitted_for_area_of_concern', period),
             persons('visitors_permitted_for_stay_at_home_area', period),
             persons('visitors_permitted_for_general_area', period)])


# GENERAL AREA
class visitors_permitted_for_general_area(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person is authorised to visit a place of residence in a general'\
            'area?'

    def formula(persons, period, parameters):
        return ((not_(persons('maximum_permitted_number_of_visitors_general_area_present', period)))
        + persons('visiting_for_move_assistance', period)
        + persons('visiting_for_childcare', period)
        + persons('visiting_for_carer_responsibilities', period)
        + persons('visiting_for_compassionate_reasons', period)
        + persons('visiting_for_family_contact_arrangements', period)
        + persons('visiting_for_significant_event', period)
        + persons('visiting_to_inspect_residence', period))


class maximum_permitted_number_of_visitors_general_area_present(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'Will there be more than 5 visitors at your place of residence'\
            'at any one time?'


# STAY AT HOME AREA
class visitors_permitted_for_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person is authorised to visit a place of residence in an area'\
            'of concern? (Prescribed work that is necessary OR Unprescribed work'\
            'have no limits to number of workers, but prescribed work has as limit'\
            'on the number of workers)'

    def formula(persons, period, parameters):
        return select(
            [persons('visiting_person_is_worker', period),
            persons('visiting_for_non_work_activities', period)],
            [persons('worker_permitted_stay_at_home_area', period),
             persons('permitted_for_non_work_activities_in_stay_at_home_area', period)])


class worker_permitted_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'For non-prescribed workers, will the number of workers within indoor'\
            'or outdoor workers in a stay at home area be within the permitted threshold?'

    def formula(persons, period, parameters):
        visitor_is_worker = persons('visiting_person_is_worker', period)
        is_prescribed_work = persons('is_prescribed_work', period)
        is_necessary_prescribed_work = persons('is_prescribed_work_necessary', period)
        is_indoor_work = persons('work_conducted_in_indoor_area', period)
        is_outdoor_work = persons('work_conducted_in_outdoor_area', period)
        exceeds_indoor_workers_limit = persons('indoor_workers_exceed_limit_stay_at_home_area', period)
        exceeds_outdoor_workers_limit = persons('outdoor_workers_exceed_limit_stay_at_home_area', period)
        indoor_non_workers_are_present = persons('indoor_non_workers_are_present_at_indoor_work_site', period)
        is_non_necessary_eligible_indoors_work = (is_indoor_work
                                                  * (not(exceeds_indoor_workers_limit))
                                                  * (not(indoor_non_workers_are_present)))
        is_non_necessary_eligible_outdoors_work = (is_outdoor_work
                                                   * (not(exceeds_outdoor_workers_limit)))
        return (visitor_is_worker
                * ((is_prescribed_work
                    * (is_necessary_prescribed_work
                    + (is_non_necessary_eligible_indoors_work
                       + is_non_necessary_eligible_outdoors_work))
                + not_(is_prescribed_work)))
                )


class indoor_workers_exceed_limit_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    default_value = False
    definition_period = ETERNITY
    label = 'Will there be more than two workers in an indoor area'\
            'of the place of residence?'


class indoor_non_workers_are_present_at_indoor_work_site(Variable):
    value_type = bool
    entity = Person
    default_value = False
    definition_period = ETERNITY
    label = 'Is a person who is not a worker in the same room as the worker(s),' \
            ' when the worker(s) carries out prescribed work?'


class outdoor_workers_exceed_limit_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    default_value = False
    definition_period = ETERNITY
    label = 'Will there be more than five workers in an outdoor area'\
            'of the place of residence?'


class permitted_for_non_work_activities_in_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    default_value = False
    definition_period = ETERNITY
    label = 'Is  person permitted to visit for non-work activities?'

    def formula(persons, period, parameters):
        visiting_for_move_assistance = persons('visiting_for_move_assistance', period)
        visiting_for_childcare = persons('visiting_for_childcare', period)
        visiting_for_family_contact_arrangements = persons('visiting_for_family_contact_arrangements', period)
        visiting_for_emergency = persons('visiting_for_emergency', period)
        visiting_to_avoid_injury_or_harm = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_to_inspect_residence = persons('visiting_to_inspect_residence', period)
        visiting_for_carer_responsibilities = persons('visiting_for_carer_responsibilities', period)
        visiting_for_compassionate_reasons = persons('visiting_for_compassionate_reasons', period)
        eligible_to_provide_care_or_compassionate_visit = (visiting_for_carer_responsibilities
                                                           + visiting_for_compassionate_reasons
                                                           * persons('eligible_to_provide_care_or_compassionate_visit', period))
        is_nominated_person = persons('is_nominated_person', period)
        only_one_adult_resides_at_premises = persons('only_one_adult_resides_at_premises', period)
        nominated_individual_resides_in_stay_at_home_area = persons('nominated_individual_resides_in_stay_at_home_area', period)
        return (visiting_for_move_assistance + visiting_for_childcare
        + visiting_for_family_contact_arrangements + visiting_for_emergency
        + visiting_to_avoid_injury_or_harm + visiting_to_inspect_residence
        + eligible_to_provide_care_or_compassionate_visit
        + (is_nominated_person * only_one_adult_resides_at_premises
        * nominated_individual_resides_in_stay_at_home_area))


# AREA OF CONCERN
class visitors_permitted_for_area_of_concern(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person is authorised to visit a place of residence in an area'\
            'of concern?'

    def formula(persons, period, parameters):
        return select(
            [persons('visiting_person_is_worker', period),
            persons('visiting_for_non_work_activities', period)],
            [persons('worker_permitted_area_of_concern', period),
             persons('permitted_for_non_work_activities_in_area_of_concern', period)])


class outdoor_workers_exceeds_limit_area_of_concern(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Will there be more than five workers in an outdoor area'\
            'of the place of residence?'


class worker_permitted_area_of_concern(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'For non-prescribed workers in an area of concern, will the number of'\
            'workers within indoor or outdoor workers in a stay at home area be within'\
            'the permitted threshold?'

    def formula(persons, period, parameters):
        visitor_is_worker = persons('visiting_person_is_worker', period)
        is_prescribed_work = persons('is_prescribed_work', period)
        is_necessary_prescribed_work = persons('is_prescribed_work_necessary', period)
        is_outdoor_work = persons('work_conducted_in_outdoor_area', period)
        exceeds_outdoor_workers_limit = persons('outdoor_workers_exceeds_limit_area_of_concern', period)
        is_eligible_outdoors_work = (is_outdoor_work * (not(exceeds_outdoor_workers_limit)))
        return (visitor_is_worker
                * (is_prescribed_work * (is_necessary_prescribed_work + is_eligible_outdoors_work))
                + not_(is_prescribed_work)
                )


class permitted_for_non_work_activities_in_area_of_concern(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person authorised to visit a place of residence in a stay'\
            'at home area?'

    def formula(persons, period, parameters):
        visiting_for_move_assistance = persons('visiting_for_move_assistance', period)
        visiting_for_childcare = persons('visiting_for_childcare', period)
        visiting_for_family_contact_arrangements = persons('visiting_for_family_contact_arrangements', period)
        visiting_for_emergency = persons('visiting_for_emergency', period)
        visiting_to_avoid_injury_or_harm = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_to_inspect_residence = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_for_carer_responsibilities = persons('visiting_for_carer_responsibilities', period)
        visiting_for_compassionate_reasons = persons('visiting_for_compassionate_reasons', period)
        eligible_to_provide_care_or_compassionate_visit = (visiting_for_carer_responsibilities
                                                           + visiting_for_compassionate_reasons
                                                           * persons('eligible_to_provide_care_or_compassionate_visit', period))
        is_nominated_person = persons('is_nominated_person', period)
        only_one_adult_resides_at_premises = persons('only_one_adult_resides_at_premises', period)
        return (visiting_for_move_assistance + visiting_for_childcare
        + visiting_for_family_contact_arrangements + visiting_for_emergency
        + visiting_to_avoid_injury_or_harm + visiting_to_inspect_residence
        + eligible_to_provide_care_or_compassionate_visit
        + (is_nominated_person * only_one_adult_resides_at_premises))


# COMMON CONDITIONS
class visiting_person_is_worker(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the visiting person a worker?'


class visiting_for_non_work_activities(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  the person visiting for non-work related (other) activities?'


class nominated_individual_resides_in_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  the nominated visitor the individual residing in a stay at home'\
            'area but not in an area of concern?'


class only_one_adult_resides_at_premises(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Does only one person reside in the place of' \
            'residence?'


class is_prescribed_work(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work relating to (a) cleaning, (b) repairs and maintenance'\
            '(c) alterations and additions to buildings'\
            '(d) work carried out as part of a trade, including electrical'\
            'work or plumbing'


class is_prescribed_work_necessary(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Is the prescribed work necessary to be carried out?'

    # def formula(persons, period, parameters):
    #     is_prescribed_work = persons('is_prescribed_work', period)
    #     work_required_for_health_and_safety = persons('work_required_for_health_and_safety', period)
    #     work_required_for_emergency = persons('work_required_for_emergency', period)
    #     work_required_for_essential_utility = persons('work_required_for_essential_utility', period)
    #     work_required_for_fire_protection = persons('work_required_for_fire_protection', period)
    #     work_required_for_cleaning_or_repairs = persons('work_required_for_cleaning_or_repairs', period)
    #     work_required_for_sale_and_lease = persons('work_required_for_sale_and_lease', period)
    #     return is_prescribed_work * (work_required_for_health_and_safety
    #     + work_required_for_emergency + work_required_for_essential_utility
    #     + work_required_for_fire_protection + work_required_for_cleaning_or_repairs
    #     + work_required_for_sale_and_lease)


# class work_required_for_health_and_safety(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = ETERNITY
#     label = 'Is the work urgently required to be carried out to ensure the'\
#             'health, safety or security of the place of residence'\
#             'or persons residing at the place of residence'
#
#
# class work_required_for_emergency(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = ETERNITY
#     label = 'Is the work urgently required to be carried out because of an'\
#             'emergency?'
#
#
# class work_required_for_essential_utility(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = ETERNITY
#     label = 'Is the work required for the installation, maintenance or repair of'\
#             'an essential utility?'
#
#
# class work_required_for_fire_protection(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = ETERNITY
#     label = 'Is the work required for fire protection and safety?'
#
#
# class work_required_for_cleaning_or_repairs(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = ETERNITY
#     label = 'Is the prescribed work (cleaning or repairs and maintenance)'\
#             'at a place of residence that is unoccupied when the work is being'\
#             'carried out?'
#
#
# class work_required_for_sale_and_lease(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = ETERNITY
#     label = 'Is the prescribed work (cleaning or repairs and maintenance)'\
#             'because it is necessary for the sale or lease of the place of'\
#             'residence carried out'


class work_conducted_in_indoor_area(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Will there the work be conducted in an indoor area?'


class work_conducted_in_outdoor_area(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Will there the work be conducted in an outdoor area?'


class visiting_for_move_assistance(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting to assist another person moving to or from the place of residence'


class visiting_for_childcare(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting for childcare'


class visiting_for_family_contact_arrangements(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting for family contact arrangements'


class visiting_for_emergency(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting for emergency'


class visiting_for_significant_event(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting to attend a significant event'


class visiting_to_avoid_injury_or_harm(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting to avoid an injury, illness or risk of harm'


class visiting_to_inspect_residence(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting to inspect the place of residence for sale or '\
            'lease or to participate in an auction of the place of residence'


class visiting_for_carer_responsibilities(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting for carer’s responsibilities, to provide care or'\
            'assistance to a vulnerable person'


class visiting_for_compassionate_reasons(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Person visiting for compassionate reasons'


class eligible_to_provide_care_or_compassionate_visit(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person eligible to provide care in the place of residence,' \
            ' or visit for compassionate reasons?'

    def formula(persons, period, parameters):
        visiting_for_care = persons('visiting_for_carer_responsibilities', period)
        visiting_for_compassionate_reasons = persons('visiting_for_compassionate_reasons', period)
        another_person_currently_visiting = persons('another_person_currently_visiting_for_care_or_compassionate_reasons', period)
        two_people_required_to_provide_care = persons('two_people_required_to_provide_care', period)
        eligible_to_provide_care = (visiting_for_care
                                    * (not_(another_person_currently_visiting)
                                        + two_people_required_to_provide_care))
        eligible_to_provide_compassionate_visit = (visiting_for_compassionate_reasons
                                                   * (not_(another_person_currently_visiting)))
        return (eligible_to_provide_care + eligible_to_provide_compassionate_visit)


class another_person_currently_visiting_for_care_or_compassionate_reasons(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is another person already visiting to provide care, or for compassionate reasons?'


class two_people_required_to_provide_care(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are two people required to provide care safely?'
