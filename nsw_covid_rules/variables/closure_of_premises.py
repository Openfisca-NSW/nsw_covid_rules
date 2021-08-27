from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Person

# Details situations in where premises must be closed, open with restrictions or
# exceptions to these restrictions, as detailed in Part 3, Division 3;
# Part 4, Division 3.


class premises_must_be_closed(Variable):
    value_type = bool
    entity = Person
    definition_period = ETERNITY
    label = 'Are your premises required to be closed?'

    def formula(buildings, period, parameters):
        type_of_premises = buildings('type_of_premises', period)
        TypeOfPremises = type_of_premises.possible_values
        is_amusement_centre = (type_of_premises == TypeOfPremises.amusement_centre)
        is_hairdresser = (type_of_premises == TypeOfPremises.hairdresser)
        is_spa = (type_of_premises == TypeOfPremises.spa)
        is_nail_salon = (type_of_premises == TypeOfPremises.nail_salon)
        is_beauty_salon = (type_of_premises == TypeOfPremises.beauty_salon)
        is_waxing_salon = (type_of_premises == TypeOfPremises.waxing_salon)
        is_tanning_salon = (type_of_premises == TypeOfPremises.tanning_salon)
        is_tattoo_parlour = (type_of_premises == TypeOfPremises.tattoo_parlour)
        is_massage_parlour = (type_of_premises == TypeOfPremises.massage_parlour)
        is_auction_house = (type_of_premises == TypeOfPremises.auction_house)
        is_betting_agency = (type_of_premises == TypeOfPremises.betting_agency)
        is_gaming_lounge = (type_of_premises == TypeOfPremises.gaming_lounge)
        is_non_food_market = (type_of_premises == TypeOfPremises.non_food_market)
        is_nightclub = (type_of_premises == TypeOfPremises.nightclub)
        is_non_natural_public_swimming_pool = (type_of_premises == TypeOfPremises.non_natural_public_swimming_pool)
        is_operated_by_the_national_trust = (type_of_premises == TypeOfPremises.national_trust)
        is_operated_by_the_historic_houses_trust = (type_of_premises == TypeOfPremises.historic_houses_trust)
        is_sex_services_premises = (type_of_premises == TypeOfPremises.sex_services)
        is_sex_on_premises_venue = (type_of_premises == TypeOfPremises.sex_on_premises)
        is_strip_club = (type_of_premises == TypeOfPremises.strip_club)
        return(is_amusement_centre
               + is_hairdresser
               + is_spa
               + is_nail_salon
               + is_beauty_salon
               + is_waxing_salon
               + is_tanning_salon
               + is_tattoo_parlour
               + is_massage_parlour
               + is_auction_house
               + is_betting_agency
               + is_gaming_lounge
               + is_non_food_market
               + is_nightclub
               + is_non_natural_public_swimming_pool
               + is_operated_by_the_national_trust
               + is_operated_by_the_historic_houses_trust
               + is_sex_services_premises
               + is_sex_on_premises_venue
               + is_strip_club
               )
