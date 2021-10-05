from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Person
import numpy as np


class mask_requirements(Variable):
    value_type = str
    entity = Person
    definition_period = ETERNITY
    label = 'What are the mask requirements for this LGA and suburb in NSW?'
    reference = "variable-type: output"

    def formula(persons, period, parameters):
        category_of_area = persons('LGA_category_of_area', period)
        AREA = category_of_area.possible_values
        in_stay_at_home_area = (category_of_area == AREA.stay_at_home_area)
        in_general_area = (category_of_area == AREA.general_area)
        return np.select(
            [in_stay_at_home_area,
             in_general_area],
            ["Indoor, public transport",
             persons('permitted_for_visiting_general_area', period)])
