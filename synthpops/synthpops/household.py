import sciris as sc
import numpy as np


def generate_household_dictionary(contacts):
    """
    Given a dictionary of contacts of a person derived from generate_synthetic_populaton, 
    generate a household_dict.

    Args:
        contacts(dict) : The contact dictionary

    Returns:
        a household dict of  {household_index: 
                                {'member_list': [member_list], 
                                'socio-econ': -1, 
                                location: '',
                                size: xxxx}
                            }
    """
    household_dict = {}

    for key in contacts.keys():
        hhid = contacts[key]['hhid']
        if hhid not in household_dict.keys():
			household_dict[hhid] = {}
            household_dict[hhid]['member_list'] = [key]
            household_dict[hhid]['socio-econ'] = -1
            household_dict[hhid]['location'] = ''
            household_dict[hhid]['size'] = 1
        else:
            household_dict[hhid]['member_list'].append(key)
            household_dict[hhid]['size'] += 1

    return household_dict


def make_socio_econ_status(hhdict, npop, lowest=.59, middle=.32, high=.08, highest=1-lowest-middle-high):  # to do find out US average
    """
    Given a dictionary of households index : hh info, and percentages of diff socio-econ class
    by hh income within the city, asign household and then its members of one socio econ status.

    0 - lowest:  hh income < 50k
    1 - middle:  hh income 50-100k
    2 - high:    hh income 100-200k
    3 - highest: hh income > 200k

    hhdict input: 
        a houehold dict of  {household_index: 
                                {'member_list': [member_list], 
                                'socio-econ': -1, 
                                location: '',
                                size: xxxx }
                            }

    Args:
        contacts(dict) : The contact dictionary

    Returns:
        a household dict of  {household_index: 
                                {'member_list': [member_list], 
                                'socio-econ': 0/1/2/3, 
                                location: ''}
                            }
    """
    # update according to Barnsdall data first
    lowest = .59
    middle = .32
    high = .08
    highest = 1 - lowest - middle - high

    num_lowest = int(npop * lowest)
    num_middle = int(npop * middle)
    num_higher = int(npop * high)
    num_highest = int(npop * highest)

    round_off_diff = npop - (num_lowest + num_middle + num_higher + num_highest)
    # naive way... need to change
    if round_off_diff == 1:
        num_lowest += 1
    elif round_off_diff == 2:
        num_lowest += 1
        num_middle += 1
    elif round_off_diff == 3:
        num_lowest += 1
        num_middle += 1
        num_higher += 1
    elif round_off_diff == 4:
        num_lowest += 1
        num_middle += 1
        num_higher += 1
        num_highest += 1

    print(num_lowest + num_middle + num_higher + num_highest)

    se_dict = {
        'se_lowest': [],
        'se_middle': [],
        'se_high': [],
        'se_highest': [],
    }

    remaining_dict = {
        'se_lowest': num_lowest,
        'se_middle': num_middle,
        'se_high': num_higher,
        'se_highest': num_highest
    }

    # put fams into dicts one by one first, fill in one se class as much as possible
    hhid = 0
    for se_class in se_dict.keys():
        while (remaining_dict[se_class] > 0):  # this makes each category slightly over
            se_dict[se_class].append(household_dict[hhid])
            remaining_dict[se_class] -= household_dict[hhid]['size']
            hhid += 1
            if hhid == len(household_dict):
                break

    # take out one household with size == the number of extra ppl in each class to put to last category
    found = False
    for se_class in ['se_lowest', 'se_middle', 'se_high']:
        num_extra = -1 * remaining_dict[se_class]
        if num_extra == 0:
            continue
        else:
            for hh in se_dict[se_class]:
                # remove first instance of the household with exactly the extra ppl and put into highest category
                if hh['size'] == num_extra:
                    se_dict[se_class].remove(hh)
                    se_dict['se_highest'].append(hh)
                    remaining_dict[se_class] += hh['size']
                    remaining_dict['se_highest'] -= hh['size']
                    break