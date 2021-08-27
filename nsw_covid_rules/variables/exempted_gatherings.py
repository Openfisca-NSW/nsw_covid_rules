from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

# Variables relating to gathering exempted from stay at home requirements, as
# detailed in Schedule 3 of the PHO.

class ExemptedGatherings(Enum):
    not_exempt = 'Gathering is not one of the gatherings listed above.'


class exempted_gathering(Variable):
    value_type = Enum
    possible_values = ExemptedGatherings
    default_value = ExemptedGatherings.not_exempt
    entity = Building
    definition_period = ETERNITY
    label = 'Is your gathering a type of gathering exempt from restrictions on' \
            ' maximum number of people allowed on a premises?'
