from nsw_covid_rules.regulation_reference.regulation_reference import Regulation, PartType as PT


PHO_2021 = Regulation(
    "ESS 2021", "Public Health (COVID-19 Additional Restrictions for Delta Outbreak) Order", "21 August 2021")

# Identify Common Variables---------------

#  Variables Specific to Clauses ---------------

division_1 = PHO_2021.add_part("1", PT.CLAUSE, "Introduction")
division_1.add_parts([("1.1", PT.CLAUSE, 'Name of Order'),
                    ("1.2", PT.CLAUSE, 'Commencement')])
