from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Person

import numpy as np

# deals with application of "general area", "stay at home" and "area of concern"
# designations, as detailed in Clause 2.1, Clause 3.1, Clause 4.1, and primarily
# Schedule 1.


class person_state_of_residence(Variable):
    value_type = str
    entity = Person
    default_value = "NSW"
    definition_period = ETERNITY
    label = 'What state is the person residing in?'


class person_suburb_of_residence(Variable):
    value_type = str
    entity = Person
    definition_period = ETERNITY
    label = 'What suburb is the person residing in?'


class lgaShortName(Variable):
    value_type = str
    entity = Person
    definition_period = ETERNITY
    label = 'What LGA is the person residing in?'


class LGAResidence(Enum):
    city_of_albury = 'Person resides in the City of Albury LGA.'
    armidale = 'Person resides in the Armidale LGA.'
    ballina = 'Person resides in the Ballina LGA.'
    bayside_council = 'Person resides in the Bayside Council LGA.'
    city_of_blacktown = 'Person resides in the City of Blacktown LGA.'
    burwood = 'Person resides in the Burwood LGA.'
    city_of_campbelltown = 'Person resides in the City of Campbelltown LGA.'
    canterbury_bankstown = 'Person resides in the Canterbury-Bankstown LGA.'
    cumberland = 'Person resides in the Cumberland LGA.'
    city_of_fairfield = 'Person resides in the City of Fairfield LGA.'
    georges_river = 'Person resides in the Georges River LGA.'
    inner_west = 'Person resides in the Inner West LGA.'
    city_of_liverpool = 'Person resides in the City of Liverpool LGA.'
    city_of_parramatta = 'Person resides in the City of Parramatta LGA.'
    strathfield = 'Person resides in the Strathfield LGA.'
    city_of_penrith = 'Person resides in the City of Penrith LGA.'
    city_of_sydney = 'Person resides in the City of Sydney LGA.'


class person_LGA_of_residence(Variable):
    value_type = Enum
    possible_values = LGAResidence
    default_value = LGAResidence.city_of_sydney
    entity = Person
    definition_period = ETERNITY
    label = 'What suburb is the person in?'

    def formula(persons, period, parameters):
        suburb = persons('person_suburb_of_residence', period)
        return np.select([
                         suburb == "Blacktown",
                         suburb == "Enmore",
                         suburb == "Surry Hills",
                         ],
                         [
                         LGAResidence.city_of_blacktown,
                         LGAResidence.inner_west,
                         LGAResidence.city_of_sydney,
                         ]
                         )


class CategoryOfArea(Enum):
    general_area = 'Person is in the general area.'
    stay_at_home_area = 'Person is in a stay at home area.'
    area_of_concern = 'Person is in an area of concern.'


class category_of_area(Variable):
    value_type = Enum
    possible_values = CategoryOfArea
    default_value = CategoryOfArea.general_area
    entity = Person
    definition_period = ETERNITY
    label = 'What suburb is the person in?'

    def formula(persons, period, parameters):
        suburb = persons('person_suburb_of_residence', period)
        LGA = persons('person_LGA_of_residence', period)
        is_in_area_of_concern = ((LGA == LGAResidence.bayside_council)
                                 + (LGA == LGAResidence.city_of_blacktown)
                                 + (LGA == LGAResidence.burwood)
                                 + (LGA == LGAResidence.city_of_campbelltown)
                                 + (LGA == LGAResidence.canterbury_bankstown)
                                 + (LGA == LGAResidence.cumberland)
                                 + (LGA == LGAResidence.city_of_fairfield)
                                 + (LGA == LGAResidence.georges_river)
                                 + (LGA == LGAResidence.city_of_liverpool)
                                 + (LGA == LGAResidence.city_of_parramatta)
                                 + (LGA == LGAResidence.strathfield)
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Caddens'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Claremont Meadows'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Colyton'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Erskine Park'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Kemps Creek'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Kingswood'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'North St Marys'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Mount Vernon'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Orchard Hills'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'Oxley Park'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'St Clair'))
                                 + ((LGA == LGAResidence.city_of_penrith) * (suburb == 'St Marys'))
                                 )
        return np.where(is_in_area_of_concern,
                        CategoryOfArea.area_of_concern,
                        CategoryOfArea.stay_at_home_area)
    # note that Schedule 1, Part 2 currently defines the whole state as being in
    # either a stay at home area or an area of concern - there is no part of NSW
    # currently in "the general area"


class LGA_category_of_area(Variable):
    value_type = Enum
    possible_values = CategoryOfArea
    default_value = CategoryOfArea.general_area
    entity = Person
    definition_period = ETERNITY
    label = 'Based on suburb and LGA, which category of area does the person live in?'

    def formula(persons, period, parameters):
        suburb = persons('person_suburb_of_residence', period)
        lgaShortName = persons('lgaShortName', period)
        state = persons('person_state_of_residence', period)
        area_of_concern = ((state == 'NSW')
            * ((lgaShortName == 'BAYSIDE')
            + (lgaShortName == 'BLACKTOWN')
            + (lgaShortName == 'BURWOOD')
            + (lgaShortName == 'CAMPBELLTOWN')
            + (lgaShortName == 'CANTERBURY-BANKSTOWN')
            + (lgaShortName == 'CUMBERLAND')
            + (lgaShortName == 'FAIRFIELD')
            + (lgaShortName == 'GEORGES RIVER')
            + (lgaShortName == 'LIVERPOOL')
            + (lgaShortName == 'PARRAMATTA')
            + (lgaShortName == 'STRATHFIELD')
            + ((lgaShortName == 'PENRITH')
                * ((suburb == 'CADDENS')
                    + (suburb == 'CLAREMONT MEADOWS')
                    + (suburb == 'COLYTON')
                    + (suburb == 'ERSKINE PARK')
                    + (suburb == 'KEMPS CREEK')
                    + (suburb == 'KINGSWOOD')
                    + (suburb == 'NORTH ST MARYS')
                    + (suburb == 'MOUNT VERNON')
                    + (suburb == 'ORCHARD HILLS')
                    + (suburb == 'OXLEY PARK')
                    + (suburb == 'ST CLAIR')
                    + (suburb == 'ST MARYS')))))
        general_area = ((state == 'NSW')
            * ((lgaShortName == 'BEGA VALLEY')
            + (lgaShortName == 'BLAYNEY')
            + (lgaShortName == 'BOGAN')
            + (lgaShortName == 'CABONNE')
            + (lgaShortName == 'DUNGOG')
            + (lgaShortName == 'FORBES')
            + (lgaShortName == 'MUSWELLBROOK')
            + (lgaShortName == 'NARRABRI')
            + (lgaShortName == 'PARKES')
            + (lgaShortName == 'SINGLETON')
            + (lgaShortName == 'SNOWY MONARO REGIONAL')
            + (lgaShortName == 'UPPER HUNTER')))
        stay_at_home_area = state == 'NSW'
        return np.select([
            area_of_concern,
            general_area,
            stay_at_home_area,
            ],
            [
            CategoryOfArea.area_of_concern,
            CategoryOfArea.general_area,
            CategoryOfArea.stay_at_home_area,
            ])
