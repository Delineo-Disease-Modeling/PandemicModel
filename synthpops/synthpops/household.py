import sciris as sc
import numpy as np


def generate_household_dictionary(contacts):
    """
    Given a dictionary of contacts of a person derived from generate_synthetic_populaton, 
    generate a household_dict.

    Args:
        contacts(dict) : The contact dictionary

    Returns:
        a houehold dict of {household_index: [member_list]}
    """
    household_dict = {}

    for key in contacts.keys():
        hhid = contacts[key]['hhid']
        if hhid not in household_dict.keys():
            household_dict[hhid] = [key]
        else:
            household_dict[hhid].append(key)

    return household_dict
