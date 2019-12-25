from h_cran.params import *
import random
import operator
import pprint
from UE.userequipment import *

def RRH_clustering(bbu, rrh_list):

    calculate_load_score(rrh_list)
    voting(rrh_list)

    rrh_head_list = select_rrh_head(bbu.get_n_group_rrh(), rrh_list)

    local_group_list = list()
    rrh_group_list = list()
    already_selected = list()
    voting_list = list()

    for head_key in rrh_head_list :

        rrh_list[head_key[0]].head = True
        local_group_list = list()
        local_group_list.append(rrh_list[head_key[0]])

        for neighbor in rrh_list[head_key[0]].neighbor_rrh_list:
            if not neighbor.get_key() in already_selected:
                voting_list.append([neighbor.get_key(), neighbor.voting_point])

        voting_list = sorted(voting_list, key=lambda x: x[1], reverse=True)

        for neighbor_pair in voting_list :
            if len(local_group_list) < bbu.get_n_group_rrh():
                local_group_list.append(rrh_list[neighbor_pair[0]])
            else :
                break

        rrh_group_list.append(local_group_list)

    bbu.rrh_group = rrh_group_list

def select_rrh_head(group_size, rrh_list):
    rrh_head_list = list()

    for rrh in rrh_list :
        rrh_head_list.append([rrh.get_key(), rrh.voting_point])

    rrh_head_list = sorted(rrh_head_list, key=lambda x: x[1])
    rrh_head_list = rrh_head_list[0:group_size]

    return rrh_head_list

def voting(rrh_list):
    for rrh in rrh_list :
        rrh.voting_point = 0
        for neighbor in rrh.neighbor_rrh_list:
            if rrh.load_score > neighbor.load_score:
                rrh.voting_point += 1

def calculate_load_score(rrh_list):
    for rrh in rrh_list :
        serving_ue = len(rrh.get_ue_list())

        rrh_power_consumption = 0

        if rrh.get_state :
            rrh_power_consumption += rrh_active_power
            rrh_power_consumption += rrh_slope * (serving_ue * dbmToWatt(transmission_power_rrh))

        else:
            rrh_power_consumption += rrh_sleep_power

        rrh.load_score = serving_ue * math.log10(rrh_power_consumption)

