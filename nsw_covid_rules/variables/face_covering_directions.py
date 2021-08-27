from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

# details whether you need to wear a face covering, as detailed in Part 2, Division 3;
# Part 3, Division 5; Part 4, Division 5.

class NSW_COVID_19_must_wear_face_covering_general_area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is a person required to wear a fitted face covering, covering both' \
             ' the nose and mouth, within the general area?'

    def formula(buildings, period, parameters):
        person_is_over_12_yo = buildings('person_is_over_12_years_of_age', period)
        person_is_in_non_residential_indoor_area = buildings('person_is_in_non_residential_indoor_area', period)
        person_is_in_public_transport_waiting_area = buildings('person_is_in_public_transport_waiting_area', period)
        person_is_in_public_transport_vehicle = buildings('person_is_in_public_transport_vehicle', period)
        person_is_in_major_recreation_facility = buildings('person_is_in_major_recreation_facility', period)
        person_is_attending_COVID_19_safe_outdoor_gathering = buildings('person_is_attending_COVID_19_safe_outdoor_gathering', period)
        person_is_attending_controlled_outdoor_gathering = buildings('person_is_attending_controlled_outdoor_gathering', period)
        person_is_working_at_hospitality_venue_and_dealing_with_public = buildings('person_is_working_at_hospitality_venue_and_dealing_with_public', period)
        return (
                person_is_over_12_yo *
                ((person_is_in_non_residential_indoor_area) +
                 (person_is_in_public_transport_waiting_area) +
                 (person_is_in_public_transport_vehicle) +
                 (person_is_in_major_recreation_facility) +
                 (person_is_attending_COVID_19_safe_outdoor_gathering) +
                 (person_is_attending_controlled_outdoor_gathering) +
                 (person_is_working_at_hospitality_venue_and_dealing_with_public))
                )


class NSW_COVID_19_must_wear_face_covering_stay_at_home_area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is a person required to wear a fitted face covering, covering both' \
             ' the nose and mouth, within the stay at home area?'

    def formula(buildings, period, parameters):
        person_is_over_12_yo = buildings('person_is_over_12_years_of_age', period)
        person_is_in_non_residential_indoor_area = buildings('person_is_in_non_residential_indoor_area', period)
        person_is_in_non_residential_outdoor_area = buildings('person_is_in_non_residential_outdoor_area', period)
        person_is_in_residential_common_area = buildings('person_is_in_residential_common_area', period)
        person_is_in_public_transport_waiting_area = buildings('person_is_in_public_transport_waiting_area', period)
        person_is_in_public_transport_vehicle = buildings('person_is_in_public_transport_vehicle', period)
        return(
                person_is_over_12_yo *
                (
                (person_is_in_non_residential_indoor_area) +
                (person_is_in_non_residential_outdoor_area) +
                (person_is_in_residential_common_area) +
                (person_is_in_public_transport_waiting_area) +
                (person_is_in_public_transport_vehicle)
                )
            )
            # note there are some reasons which are contained in the general area
            # order which aren't contained in this definition - is this intentional?


class NSW_COVID_19_must_wear_face_covering_area_of_concern(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is a person required to wear a fitted face covering, covering both' \
             ' the nose and mouth, within the area of concern?'

    def formula(buildings, period, parameters):
        person_is_over_12_yo = buildings('person_is_over_12_years_of_age', period)
        person_is_in_non_residential_indoor_area = buildings('person_is_in_non_residential_indoor_area', period)
        person_is_in_non_residential_outdoor_area = buildings('person_is_in_non_residential_outdoor_area', period)
        person_is_in_residential_common_area = buildings('person_is_in_residential_common_area', period)
        person_is_in_public_transport_waiting_area = buildings('person_is_in_public_transport_waiting_area', period)
        person_is_in_public_transport_vehicle = buildings('person_is_in_public_transport_vehicle', period)
        return(
                person_is_over_12_yo *
                (
                (person_is_in_non_residential_indoor_area) +
                (person_is_in_non_residential_outdoor_area) +
                (person_is_in_residential_common_area) +
                (person_is_in_public_transport_waiting_area) +
                (person_is_in_public_transport_vehicle)
                )
            )


class person_is_over_12_years_of_age(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person over 12 years of age?'


class person_is_in_non_residential_indoor_area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person in a non residential indoor area?'


class person_is_in_residential_common_area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person in a residential indoor common area?'


class person_is_in_non_residential_outdoor_area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person in a non residential outdoor area?'


class person_is_in_public_transport_waiting_area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person in a public transport waiting area?'


class person_is_in_public_transport_vehicle(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person in a public transport vehicle?'


class person_is_in_major_recreation_facility(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person at a major recreation facility?'


class person_is_attending_COVID_19_safe_outdoor_gathering(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person attending a COVID-19 Safe outdoor gathering?'


class person_is_attending_controlled_outdoor_gathering(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person attending a controlled outdoor gathering?'


class person_is_working_at_hospitality_venue_and_dealing_with_public(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person working at a hospitality venue and dealing with the public?'


class person_is_medically_exempt_from_wearing_face_covering(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person medically exempty from wearing a face covering, and' \
            ' do they have evidence to support this?'

    def formula(buildings, period, parameters):
        person_has_physical_illness_or_condition = buildings('person_has_physical_illness_or_condition', period)
        person_has_mental_illness_or_condition = buildings('person_has_physical_illness_or_condition', period)
        person_has_evidence_of_facemask_unsuitability = buildings('person_has_evidence_of_facemask_unsuitability', period)
        return (
                (person_has_physical_illness_or_condition + person_has_mental_illness_or_condition) *
                person_has_evidence_of_facemask_unsuitability
                )


class person_has_physical_illness_or_condition(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the person have a physical condition that makes wearing a' \
            ' fitted face covering unsuitable, such as but not limited to' \
            ' ...?'
    # note they took the possible conditions (i.e. asthma, autism) for not \
    # wearing a facemask out of the PHO on 21 Aug. Do we want to simply say \
    # "if you have evidence (which is defined in the PHO) of your condition \
    # being suitable for not wearing a facemask, you don't have to?



class person_is_conducting_exempt_activity(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the person conducting an activity which exempts them from' \
            ' wearing a face mask?'

    def formula(buildings, period, parameters):
        current_exempt_activity = buildings('current_exempt_activity', period)
        is_not_exempt = (current_exempt_activity == CurrentExemptActivity.is_not_exempt)
        return np.logical_not(is_not_exempt)


class CurrentExemptActivity(Enum):
    is_eating = 'Person is eating.'
    is_drinking = 'Person is drinking.'
    is_strenously_exercising = 'Person is engaging in strenous exercise, except' \
                               ' in an indoor area as part of a gym class or dance class.'
    communicating_with_deaf = 'Person is communicating with a person who is deaf' \
                              ' or hard of hearing.'
    covering_is_risk_to_safety = 'Person is engaging in work where wearing a' \
                                 ' covering is a risk to their, or another person\'s safety.'
    enunciation_of_mouth_is_essential = 'Person is engaging in an activity where' \
                                        ' enunciation of their mouth is essential.'
    visibility_of_mouth_is_essential = 'Person is engaging in an activity where' \
                                       ' visibility of their mouth is essential.'
    work_in_indoor_area_alone = 'Person is working in an indoor area and no' \
                                ' other person is in the area.'
    working_in_school = 'Person is working in a school.'
    requested_for_identity_check = 'Person is requested to remove their mask as' \
                                   ' part of an identity check.'
    for_emergency = 'Person is required to remove facemask in case of an emergency.'
    provision_of_goods_or_service = 'Person is required to remove facemask for' \
                                    ' proper provision of goods or service.'
    in_vehicle_alone = 'Person is in a vehicle, alone.'
    in_vehicle_with_household_member = 'Person is in a vehicle, and all other' \
                                       ' people are members of the person\'s household.'
    in_vehicle_with_nominated_visitor = 'Person is in a vehicle, and the other' \
                                        ' person is the person\'s nominated visitor.'
    in_motel = 'Person is in a motel or hotel, and is in their own room.'
    is_student_at_school = 'Person is a student currently in a school.'
    is_patient_at_health_facility = 'Person is a patient at a public hospital,' \
                                    ' or at a private health facility.'
    is_resident_at_aged_care_facility= 'Person is a resident at a residential' \
                                       ' aged care facility.'
    in_correctional_centre = 'Person is in a correctional centre, or other place of custody.'
    is_getting_married = 'Person is in the process of getting married.'
    is_not_exempt = 'Person is not conducting any exempt activities.'


class current_exempt_activity(Variable):
    value_type = Enum
    entity = Building
    possible_values = CurrentExemptActivity
    default_value = CurrentExemptActivity.is_not_exempt
    definition_period = ETERNITY
    label = 'What activity is the person conducting, which makes them exempt' \
            ' from wearing a facemask?'
