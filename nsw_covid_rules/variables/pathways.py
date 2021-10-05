from openfisca_core.model_api import *
from openfisca_nsw_base.entities import *
from openfisca_core.variables import Variable


class pathway_1(Variable):
    value_type = str
    entity = Person
    definition_period = ETERNITY
    label = 'Pathway 1 UUIDs'
    reference = "variable-type: output"

    def formula(persons, period, parameters):
        return '02d19cfd-cf07-46ef-a6f8-f60f90ff23cf, 1d270ce3-b691-463f-99c4-07ee5e87b798'
