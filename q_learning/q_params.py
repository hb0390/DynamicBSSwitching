import pprint
from h_cran.params import *

power_actions = [10, 20]

n_m_actions = 2

learning_rate = 0.01
discount_factor = 0.9
epsilon = 0.99


def get_states_with_index(index):
    if '_' in index:
        states = index.split('_')
    else:
        states = [index]
    return states


def get_index_with_states(states):
    index = ''
    for state in states:
        if index == '':
            index = str(state)
        else:
            index += '_' + str(state)
    return index

def get_bbu_actions_with_index(actions, index):
    print("q_params>actions :", actions)
    print("q_params>index :", index)
    return actions[index]


def get_bbu_index_with_actions(actions, action):
    return actions.index(action)


def get_rrh_actions_with_index(index):
    actions = [0,1]

    return actions[index]


def get_rrh_index_with_actions(action):
    actions = [0,1]

    return actions.index(action)


def get_actions_with_index(index, group_action, sleep_action):
    # g 3
    # s 4
    # 7 -> 7 //4  -> 1
    # 7 - 4 * 1  = 3
    group_index = int(index // len(sleep_action))
    sleep_index = int(index - group_index * len(sleep_action))
    print("sleep_action :", sleep_action)
    print("index[",index,"]", "groupIndex : ",group_index,"sleepIndex :",sleep_index)


    actions = list()
    actions.append(group_action[group_index])
    actions.append(sleep_action[sleep_index])
    return actions


def get_index_with_actions(actions, group_action, sleep_action):
    group_index = group_action.index(actions)
    sleep_index = sleep_action.index(actions)

    index = group_index * len(sleep_action) + sleep_index
    return index
