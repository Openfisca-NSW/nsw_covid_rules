from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Person

import numpy as np
# Variables relating to gathering exempted from stay at home requirements, as
# detailed in Schedule 3 of the PHO.


class ExemptedGatherings(Enum):
    not_exempt = 'Gathering is not one of the gatherings listed above.'


class exempted_gathering(Variable):
    value_type = Enum
    possible_values = ExemptedGatherings
    default_value = ExemptedGatherings.not_exempt
    entity = Person
    definition_period = ETERNITY
    label = 'Is your gathering a type of gathering exempt from restrictions on' \
            ' maximum number of people allowed on a premises?'


# code relating to vehicles in stay at home areas - clause 3.14

class ReasonForVehicleUse(Enum):
    carry_out_work = 'Vehicle is being used to carry out work.'
    public_transport = 'Vehicle is being used to provide public transport service.'
    provide_care_or_assistance = 'Vehicle is being used to provide care or' \
                                 ' assistance to a vulnerable person.'
    emergency = 'Vehicle is being used in an emergency.'
    compassionate_reasons = 'Vehicle is being used for compassionate reasons.'
    other_reason = 'Vehicle is being used for a reason other than those listed above.'
# list of reasons that are excluded from restrictions on sharing a vehicle, as detailed in clause 3.14 (3).


class reason_for_vehicle_use(Variable):
    value_type = Enum
    possible_values = ReasonForVehicleUse
    default_value = ReasonForVehicleUse.other_reason
    entity = Person
    definition_period = ETERNITY
    label = 'What is your reason for using your vehicle?'


class PassengerRelation(Enum):
    member_of_household = 'Person is only in the vehicle with a member of their household.'
    nominated_visitor = 'Person is only in the vehicle with their nominated visitor.'
    no_person = 'Person is in a vehicle by themselves.'
    other_persons = 'Person is in a vehicle with any person other than those listed above.'
# list of relationships to passengers which are excluded from restrictions on sharing a vehicle,
# as detailed in clause 3.14 (1).


class passenger_relation(Variable):
    value_type = Enum
    possible_values = PassengerRelation
    default_value = PassengerRelation.no_person
    entity = Person
    definition_period = ETERNITY
    label = 'Who are you in the vehicle with?'


class allowed_to_share_vehicle_stay_at_home_area(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Are you allowed to share the vehicle with another person, in a' \
            ' stay at home area?'

    def formula(persons, period, parameters):
        reason_for_vehicle_use = persons('reason_for_vehicle_use', period)
        passenger_relationship = persons('passenger_relation', period)
        not_valid_reason = (reason_for_vehicle_use == ReasonForVehicleUse.other_reason)
        not_valid_relationship = (passenger_relationship == PassengerRelation.other_persons)
        return np.logical_not(not_valid_reason * not_valid_relationship)
# formula for determining whether you can share a vehicle in a stay at home arem,
# as defined in the overall clause 3.14.


class allowed_to_share_vehicle_area_of_concern(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Are you allowed to share the vehicle with another person, in an' \
            ' area of concern?'

    def formula(persons, period, parameters):
        reason_for_vehicle_use = persons('reason_for_vehicle_use', period)
        passenger_relationship = persons('passenger_relation', period)
        not_valid_reason = (reason_for_vehicle_use == ReasonForVehicleUse.other_reason)
        not_valid_relationship = (passenger_relationship == PassengerRelation.other_persons)
        return np.logical_not(not_valid_reason * not_valid_relationship)

# formula for determining whether you can share a vehicle in an area of concern,
# as defined in the overall clause 4.15.
# note this is identical to formula in stay at home area, but is coded as separate variables
# in case this changes and they deviate.


class allowed_to_share_vehicle(Variable):
    value_type = bool
    default_value = False
    entity = Person
    definition_period = ETERNITY
    label = 'Are you allowed to share the vehicle with another person?'
# overall variable integrating the above

    def formula(persons, period, parameters):
        category_of_area = persons('category_of_area', period)
        CategoryOfArea = (category_of_area.possible_values)
        return np.select([category_of_area == (CategoryOfArea.general_area),
                          category_of_area == (CategoryOfArea.stay_at_home_area),
                          category_of_area == (CategoryOfArea.area_of_concern)],
                         [True,
                          persons('allowed_to_share_vehicle_stay_at_home_area', period),
                          persons('allowed_to_share_vehicle_area_of_concern', period)]
                         )

# note that 1. there are currently no restrictions on sharing a vehicle in the general area,
# and 2. there is currently nobody in the general area
