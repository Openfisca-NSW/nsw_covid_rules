from openfisca_core.indexed_enums import Enum

# details 1. eligibility and reasons to get a permit to leave Greater Sydney,
# 2. requirements to get such permit,
# 3. eligibility and reasons to get a permit to be a nominated visitor,
# 4. when gazetted, eligibility and reasons to get a permit to leave the area of concern.


class PermitReasonsGreaterSydney(Enum):
    leaving_Greater_Sydney = 'Person is leaving Greater Sydney.'
    relocating_new_place_of_residence = 'Person is relocating to a new place' \
                                        ' of residence outside Greater Sydney.'
    move_between_place_of_residence_for_work = 'Person moves between places of' \
                                               ' residence for work, where only' \
                                               ' the person moves to the other place of residence.'
    move_between_place_of_residence_for_repairs = 'Person moves between places of' \
                                                  ' residence for urgent maintenance or repairs.'
    move_between_place_of_residence_for_animal_welfare = 'Person moves between places of' \
                                                         ' residence for animal welfare.'
    inspect_new_place_of_residence = 'Person is inspecting residential property' \
                                     ' as potential place of residence, with the ' \
                                     ' intent to reside outside Greater Sydney as soon' \
                                     ' as is practicable.'
    carrying_out_work = 'Person is carrying out work more than 50 kilometres' \
                        ' from Greater Sydney.'
    carrying_out_emergency_work = 'Person is carrying out work involving the provision of an emergency service.'
    no_valid_reason = 'Person does not have a valid reason to leave Greater Sydney.'
