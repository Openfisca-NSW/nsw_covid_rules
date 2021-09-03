from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Person

import numpy as np

# Variables relating to the maximum number of people allowed on a premises, as detailed
# in


class maximum_number_of_persons_general_area(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' the general area?'
    # clause 2.2 (1)

    def formula(persons, period, parameters):
        type_of_premises = persons('type_of_premises', period)
        in_greater_sydney = persons('in_Greater_Sydney', period)
        exempted_gathering = persons('exempted_gathering', period)
        ExemptedGathering = (exempted_gathering.possible_values)
        is_place_of_residence = (type_of_premises == TypeOfPremises.place_of_residence)
        is_holiday_home_or_short_term_rental = ((type_of_premises == TypeOfPremises.holiday_home)
                                               + (type_of_premises == TypeOfPremises.short_term_rental))
        is_entertainment_facility = (type_of_premises == TypeOfPremises.entertainment_facility)
        is_major_recreation_facility = (type_of_premises == TypeOfPremises.major_recreation_facility)
        is_group_gym_or_dance_class = (type_of_premises == TypeOfPremises.indoor_recreation_facility)
# need to add requirement that activity is a gym or group dance class
# it doesn't fit in with type of premises, not with exempt activities
        is_commercial_vessel = ((type_of_premises == TypeOfPremises.commercial_scuba_diving_vessel)
                                + (type_of_premises == TypeOfPremises.commercial_snorkelling_vessel)
                                + (type_of_premises == TypeOfPremises.commercial_marine_animal_watching_vessel))
        is_caravan_park_or_camping_ground = ((type_of_premises == TypeOfPremises.caravan_park)
                                             + (type_of_premises == TypeOfPremises.camping_ground))
        is_exempt_gathering = np.logical_not(exempted_gathering == ExemptedGathering.not_exempt)  # checks if
        is_Greater_Sydney_construction_site = ((type_of_premises == TypeOfPremises.construction_site)
                                               * in_greater_sydney)
# need to code in condition for Schedule 3 gatherings
        return np.select([is_place_of_residence,
                          is_holiday_home_or_short_term_rental,
                          is_entertainment_facility,
                          is_major_recreation_facility,
                          is_group_gym_or_dance_class,
                          is_caravan_park_or_camping_ground,
                          is_commercial_vessel,
                          is_exempt_gathering,
                          is_Greater_Sydney_construction_site,
                          np.logical_not
                          (is_place_of_residence
                          + is_holiday_home_or_short_term_rental
                          + is_entertainment_facility
                          + is_major_recreation_facility
                          + is_group_gym_or_dance_class
                          + is_caravan_park_or_camping_ground
                          + is_commercial_vessel
                          + is_exempt_gathering
                          + is_Greater_Sydney_construction_site,
                           )
                          ],
                         [persons('maximum_number_of_persons_in_general_area_residence', period),
                          persons('maximum_number_of_persons_in_holiday_home_or_short_term_rental_general_area', period),
                          persons('maximum_number_of_persons_in_general_area_entertainment_facilities', period),
                          persons('maximum_number_of_persons_in_general_area_major_recreation_facility', period),
                          persons('maximum_number_of_persons_in_gym_group_class', period),
                          1000,  # note there's no clause for caravan parks or campsite
                          1000,  # note there's no clause for caravan parks or campsite
                          0,  # need to figure out distinction between no people allowed and no restriction on
                          10000,  # need to replace w. condition in 5.7
                          persons('maximum_number_of_persons_on_general_area_general_premises', period)
                          ]
                         )


class maximum_number_of_persons_on_general_area_general_premises(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' the general area?' \
            ' This does not apply to places of residence, holiday homes, short-term rentals,' \
            ' entertainment facilities, major recreation facilities,' \
            ' group gym classes, group dance classes at indoor recreation facilities, '
    # clause 2.2 (1)

    def formula(persons, period, parameters):
        size_of_premises = persons('size_of_premises', period)
        minimum_number_of_square_meters = parameters(period).maximum_number_of_allowable_persons.square_meters_per_person_in_general_area  # update this when you go to 1 person per 2 m2
        return np.where(size_of_premises / minimum_number_of_square_meters < 25,
                        25,
                        size_of_premises / minimum_number_of_square_meters)


class TypeOfPremises(Enum):
    general_premises = 'Premises are not one of the categories below.'
    place_of_residence = 'Premises is a place of residence, including temporary accomodation.'
    holiday_home = 'Premises is a holiday home.'
    short_term_rental = 'Premises is a short term rental.'
    entertainment_facility = 'Premises is an entertainment facility, including' \
                             ' a theatre, cinema, music hall, concert hall,' \
                             ' dance hall or the like. This does not include' \
                             ' pubs or registered clubs.'
    major_recreation_facility = 'Premises is a major recreation facility - meaning' \
                                ' a place regularly for large scale sporting' \
                                ' or recreation activities, including theme parks,' \
                                ' sports stadiums, showgrounds, racecourses and motor racing parks.'
    indoor_recreation_facility = 'Premises is a place used predominantly for' \
                                 ' indoor recreation, including a squash court,' \
                                 ' indoor swimming pool, gymnasium, table tennis centre,' \
                                 ' health studio, bowling alley, ice rink, or' \
                                 ' other persons used for indoor recreation. This' \
                                 ' does not include an entertainment facility,' \
                                 ' recreation facility or registered club.'
    commercial_scuba_diving_vessel = 'Premises is a commercial scuba diving vessel.'
    commercial_snorkelling_vessel = 'Premises is a commercial snorkelling vessel.'
    commercial_marine_animal_watching_vessel = 'Premises is a commercial marine animal watching vessel.'
    caravan_park = 'Premises is a caravan park.'
    camping_ground = 'Premises is a camping ground.'
    gathering = 'Premises are not one of the categories below.'  # need to check this in relation to Part 3
    construction_site = 'Premises is a construction site.'
    amusement_centre = 'Premises is an amusement centre.'
    hairdresser = 'Premises is a hairdresser.'
    spa = 'Premises is a spa.'
    nail_salon = 'Premises is a nail salon.'
    beauty_salon = 'Premises is a beauty salon.'
    waxing_salon = 'Premises is a waxing salon.'
    tanning_salon = 'Premises is a tanning salon.'
    tattoo_parlour = 'Premises is a tattoo parlour.'
    massage_parlour = 'Premises is a massage parlour.'
    auction_house = 'Premises is an auction house.'
    betting_agency = 'Premises is a betting agency.'
    gaming_lounge = 'Premises is a gaming lounge.'
    non_food_market = 'Premises is a market that does not predominantly sell food.'
    nightclub = 'Premises is a nightclub.'
    non_natural_public_swimming_pool = 'Premises is a non-natural, public swimming pool.'
    national_trust = 'Premises is operated by the National Trust.'
    historic_houses_trust = 'Premises is operated by the Historic Houses Trust.'
    sex_services = 'Premises is a sex services premise.'
    sex_on_premises = 'Premises is a sex on premises venue.'
    strip_club = 'Premises is a strip club.'


class type_of_premises(Variable):
    value_type = Enum
    possible_values = TypeOfPremises
    default_value = TypeOfPremises.place_of_residence
    entity = Person
    definition_period = ETERNITY
    label = 'What is the type of persons the person is in?'


class maximum_number_of_persons_in_general_area_residence(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' a residence within the general area?'

    def formula(persons, period, parameters):
        place_of_residence_maximum = parameters(period).maximum_number_of_allowable_persons.maximum_people_in_place_of_residence
        return place_of_residence_maximum
        # the legislation here isn't particularly clear - is it saying "only 5 people in the household" or \
        # 5 people per adult living at the residence?
        # clause 2.4 (1)


class maximum_number_of_persons_in_holiday_home_or_short_term_rental_general_area(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' a holiday home or short term rental?' \
            ' This does not apply to places of residence, holiday homes, short-term rentals,' \
            ' entertainment facilities, major recreation facilities,' \
            ' group gym classes, group dance classes at indoor recreation facilities, '

    def formula(persons, period, parameters):
        short_term_residence_maximum = parameters(period).maximum_number_of_allowable_persons.maximum_people_in_short_term_residence
        return short_term_residence_maximum
        # need to code in condition for if all people are from the same residence
        # clause 2.3


class maximum_number_of_persons_in_general_area_entertainment_facilities(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' an entertainment or major recreation facilities?'

    def formula(persons, period, parameters):
        size_of_premises = persons('size_of_premises', period)
        minimum_number_of_square_meters = parameters(period).maximum_number_of_allowable_persons.square_meters_per_person_in_entertainment  # update this when you go to 1 person per 2 m2
        return np.where(size_of_premises / minimum_number_of_square_meters < 25,
                        25,
                        size_of_premises / minimum_number_of_square_meters)
        # note that unlike 2.2 (1) b, it doesn't articulate that one of these conditions supersedes
        # the other. is the intent to keep this number low or high?
        # note that 2.5 (2) explicitly says the greater of these two values, but 2.3 (3)
        # we'll need to code in the ability to pick "or" and include a variable on
        # 50% of seating capacity


class maximum_number_of_persons_in_general_area_major_recreation_facility(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' a major recreation facility?'

    def formula(persons, period, parameters):
        size_of_premises = persons('size_of_premises', period)
        allowable_fixed_seating_capacity = persons('fixed_seating_capacity', period) / 2  # to get 50% of capacity
        unfixed_seating_area = persons('size_of_unfixed_seating_area', period)
        total_capacity = (allowable_fixed_seating_capacity + unfixed_seating_area)
        # we need to get clarity on how they measure these. note the PHO doesn't \
        # define how they measure either
        minimum_number_of_square_meters = parameters(period).maximum_number_of_allowable_persons.square_meters_per_person_in_entertainment  # update this when you go to 1 person per 2 m2
        return np.select([(total_capacity > size_of_premises / minimum_number_of_square_meters),
                          (total_capacity < size_of_premises / minimum_number_of_square_meters),
                          (total_capacity == size_of_premises / minimum_number_of_square_meters)],
                         [total_capacity,
                          size_of_premises / minimum_number_of_square_meters,
                          total_capacity
                          ]
                         )
        # note that the PHO specifies "which is greater of the following 2 options" -
        # there's no clarity on what happens when they're identical -
        # this may be inconsequential?


class maximum_number_of_persons_in_gym_group_class(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' a gym group class?'

    def formula(persons, period, parameters):
        gym_group_class_maximum = parameters(period).maximum_number_of_allowable_persons.maximum_people_in_gym_class
        return gym_group_class_maximum


class maximum_number_of_persons_stay_at_home_area(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' the stay at home area?'
    # clause 3.8

    def formula(persons, period, parameters):
        type_of_premises = persons('type_of_premises', period)
        in_greater_sydney = persons('in_Greater_Sydney', period)
        is_place_of_residence = (type_of_premises == TypeOfPremises.place_of_residence)
        is_holiday_home_or_short_term_rental = ((type_of_premises == TypeOfPremises.holiday_home)
                                                + (type_of_premises == TypeOfPremises.short_term_rental))
        is_caravan_park_or_camping_ground = ((type_of_premises == TypeOfPremises.caravan_park)
                                          + (type_of_premises == TypeOfPremises.caravan_park))
        is_commercial_vessel = ((type_of_premises == TypeOfPremises.commercial_scuba_diving_vessel)
                               + (type_of_premises == TypeOfPremises.commercial_snorkelling_vessel)
                               + (type_of_premises == TypeOfPremises.commercial_marine_animal_watching_vessel))
        is_Greater_Sydney_construction_site = ((type_of_premises == TypeOfPremises.construction_site)
                                              * in_greater_sydney)
        return np.select(
            [is_place_of_residence,
             is_holiday_home_or_short_term_rental,
             is_caravan_park_or_camping_ground,
             is_commercial_vessel,
             is_Greater_Sydney_construction_site,
             np.logical_not(is_place_of_residence
                            + is_holiday_home_or_short_term_rental
                            + is_caravan_park_or_camping_ground
                            + is_commercial_vessel
                            + is_Greater_Sydney_construction_site)
             ],
            [persons('maximum_number_of_persons_in_general_area_residence', period),
             persons('maximum_number_of_persons_in_holiday_home_or_short_term_rental_general_area', period),
             1000,  # note there's no clause for caravan parks or campsite
             1000,  # note there's no clause for caravan parks or campsite
             0,  # need to figure out distinction between no people allowed and no restriction on
             10000,  # need to replace w. condition in 5.7
             persons('maximum_number_of_persons_on_general_area_general_premises', period)
             ])


class maximum_number_of_persons_on_stay_at_home_area_general_premises(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the maximum number of people allowed on the premises, in' \
            ' the stay at home area?' \
            ' This does not apply to places of residence, holiday homes, short-term rentals.'
# clause 3.8 (1)

    def formula(persons, period, parameters):
        size_of_premises = persons('size_of_premises', period)
        minimum_number_of_square_meters = parameters(period).maximum_number_of_allowable_persons.square_meters_per_person_in_stay_at_home_area  # update this when you go to 1 person per 2 m2
        return np.where(size_of_premises / minimum_number_of_square_meters < 25,
                        25,
                        size_of_premises / minimum_number_of_square_meters)


class size_of_premises(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the size of the premises, in m2?'
# is this measured to the nearest m2, or for your purposes do you have .1 of m2?
# this variable assumes to the nearest m2.


class fixed_seating_capacity(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the fixed seating capacity of the premises, in number of chairs?'
# totally guessing that's how it's measured, we should confirm


class size_of_unfixed_seating_area(Variable):
    value_type = int
    entity = Person
    definition_period = ETERNITY
    label = 'What is the size of the unfixed seating area of the premises, in m2?'
# is this measured to the nearest m2, or for your purposes do you have .1 of m2?
# this variable assumes to the nearest m2.
