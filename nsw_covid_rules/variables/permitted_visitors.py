from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable
from nsw_covid_rules.variables.geographic_area import CategoryOfArea as Area


class visitors_permitted(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'What are the conditions for having visitors at places of residence?'

    def formula(persons, period, parameters):
        AREA = Area.possible_values
        return select(
            [(AREA.area_of_concern),
            (AREA.stay_at_home_area),
            (AREA.general_area)],
            [persons('visitors_permitted_for_area_of_concern', period),
            persons('visitors_permitted_for_stay_at_home_area', period),
            persons('visitors_permitted_for_general_area', period)])


class visitors_permitted_for_area_of_concern(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person is authorised to visit a place of residence in a stay'\
            'at home area'


class visitors_permitted_for_general_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person is authorised to visit a place of residence in a general'\
            'area'


class visitors_permitted_for_stay_at_home_area(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is  person is authorised to visit a place of residence in an area'\
            'of concern?'

    def formula(persons, period, parameters):
        visiting_for_move_assistance = persons('visiting_for_move_assistance', period)
        visiting_for_childcare = persons('visiting_for_childcare', period)
        visiting_for_family_contact_arrangements = persons('visiting_for_family_contact_arrangements', period)
        visiting_for_emergency = persons('visiting_for_emergency', period)
        visiting_to_avoid_injury_or_harm = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_to_inspect_residence = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_for_carer_responsibilities = persons('visiting_for_carer_responsibilities', period)
        is_nominated_person = persons('is_nominated_person', period)
        return (visiting_for_move_assistance + visiting_for_childcare
        + visiting_for_family_contact_arrangements + visiting_for_emergency
        + visiting_to_avoid_injury_or_harm + visiting_to_inspect_residence
        + visiting_for_carer_responsibilities + is_nominated_person)


class is_prescribed_work(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the work relating to (a) cleaning, (b) repairs and maintenance'\
            '(c) alterations and additions to buildings'\
            '(d) work carried out as part of a trade, including electrical'\
            'work or plumbing'


class is_prescribed_work_necessary(Variable):
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
        work_required_for_cleaning_or_repairs = persons('work_required_for_cleaning_or_repairs', period)
        work_required_for_sale_and_lease = persons('work_required_for_sale_and_lease', period)
        return is_prescribed_work * (work_required_for_health_and_safety
        + work_required_for_emergency + work_required_for_essential_utility
        + work_required_for_fire_protection + work_required_for_cleaning_or_repairs
        + work_required_for_sale_and_lease)


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
    label = 'Is the prescribed work (cleaning or repairs and maintenance)'\
            'at a place of residence that is unoccupied when the work is being'\
            'carried out?'


class work_required_for_sale_and_lease(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the prescribed work (cleaning or repairs and maintenance)'\
            'because it is necessary for the sale or lease of the place of'\
            'residence carried out'


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
            'assistance to a vulnerable person or for compassionate reasons'


class authorised_to_visit_place_of_residence(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Is the person authorised to visit place of residence?'

    def formula(persons, period, parameters):
        visiting_for_move_assistance = persons('visiting_for_move_assistance', period)
        visiting_for_childcare = persons('visiting_for_childcare', period)
        visiting_for_family_contact_arrangements = persons('visiting_for_family_contact_arrangements', period)
        visiting_for_emergency = persons('visiting_for_emergency', period)
        visiting_to_avoid_injury_or_harm = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_to_inspect_residence = persons('visiting_to_avoid_injury_or_harm', period)
        visiting_for_carer_responsibilities = persons('visiting_for_carer_responsibilities', period)
        return (visiting_for_move_assistance + visiting_for_childcare
        + visiting_for_family_contact_arrangements + visiting_for_emergency
        + visiting_to_avoid_injury_or_harm + visiting_to_inspect_residence
        + visiting_for_carer_responsibilities)
