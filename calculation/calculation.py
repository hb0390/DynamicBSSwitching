import math
from h_cran.params import *

def get_bigger(a, b):
    if a >= b:
        return a
    else:
        return b

def get_distance(a_x, a_y, b_x, b_y):
    x = a_x - b_x
    y = a_y - b_y
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

def dbmToWatt(dbmPower):
    return math.pow(10, dbmPower / 10) / 1000


def regulate_q_table(rrh_list):
    for rrh in rrh_list:
        q_value_dict = dict()

        for state, actions in rrh.agent.q_table.items():
            q_value_dict[state] = actions  # [state : [actions]]

        for another_rrh in rrh_list:
            if rrh.get_key() != another_rrh.get_key():
                for state, actions in rrh.agent.q_table.items():
                    if state in q_value_dict :
                        for action in actions:
                            if rrh.agent.q_table[state][actions.index(action)] != 0:
                                q_value_dict[state][actions.index(action)] = action / rrh.agent.q_table[state][actions.index(action)]
                            else :
                                q_value_dict[state][actions.index(action)] = 0

        for state, actions in q_value_dict.items():
            for action in actions:
                action = action / rrh_group_size

        rrh.agent.q_table = q_value_dict




