""" Convenience // we expose the individual `Regulation` objects here so their import statements
    are simpler.

    Example::
        # in /variables/example_variable.py

        from openfisca_core.variables import Variable
        from openfisca_core.periods import ETERNITY
        ...

        from openfisca_nsw_covid_legislation.regulation_reference import ESS_2021
"""

from nsw_covid_rules.regulation_reference.ess_2021 import ESS_2021
from nsw_covid_rules.regulation_reference.pdrs_2022 import PDRS_2022
