from openfisca_core.indexed_enums import Enum

# Reasonble excuses as detailed in Schedule 2 of the PHO.


class ReasonableExcuses(Enum):
    work = 'Person can leave place of residence to work, if it is not' \
           ' reasonably practicable to work at the place of residence.'
    attending_childcare = 'Person can leave place of residence to attend childcare.'
    pick_up_from_childcare = 'Person can leave place of residence to pick up' \
                             ' a person from childcare.'
    drop_off_from_childcare = 'Person can leave place of residence to drop off' \
                              ' a person to childcare.'
    attending_school_or_education = 'Person can leave place of residence to attend' \
                                    ' school or another educational institution,' \
                                    ' if they cannot reasonably learn from the' \
                                    ' place of residence.'
    obtaining_medical_care = 'Person can leave place of residence to obtain' \
                             ' medical care, including obtaining a ' \
                             ' COVID-19 test or vaccination.'
    obtaining_medical_supplies = 'Person can leave place of residence to obtain' \
                                 ' medical or health supplies.'
    donating_blood = 'Person can leave place of residence to donate blood.'
    provide_care = 'Person can leave place of residence to provide care or' \
                   ' assistance to a vulnerable person, or to fulfll carer\'s responsibilities.'
    compassionate_reasons = 'Person can leave place of residence for compassionate reasons.'
    family_contact_arrangements = 'Person can leave place of residence for family contact arrangements.'
    nominated_visitor_visiting = 'Person is a nominated visitor, visiting a person\'s place of residence.'
    nominated_visitor_exercise_or_recreation = 'Person is a nominated visitor,' \
                                               ' accompanying a person undertaking' \
                                               ' exercise or outdoor recreation.'
