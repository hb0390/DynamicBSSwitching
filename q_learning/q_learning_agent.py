import numpy as np
import random
from q_learning.environment import *
from collections import defaultdict
from q_learning.q_params import *
from h_cran.params import *
import pprint


class BBU_QLearningAgent:
    def __init__(self,max_sleep_num):
        self.sleep_rrh_action = list()
        self.group_rrh_action = list()
        self.table = list()
        self.max_sleep_num = max_sleep_num
        self.max_group_num = int(math.floor(num_of_RRH / 2))
        self.min_group_num = 1
        for group in range(self.max_group_num):
            if group >= 1:
                # print("group > ", group)
                self.group_rrh_action.append(group)
        for num in range(self.max_sleep_num):
            self.sleep_rrh_action.append(num)

            for group in range(self.max_group_num):
                if group >= 1:
                    self.table.append(0.0)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        # 각각 모든 액션에 대해 m_actions, p_actions 순서
        self.q_table = defaultdict(lambda: self.table)

    # <s, a, r, s'> 샘플로부터 큐함수 업데이트
    def learn(self, states, action, reward, next_states):
        # state : list [interference_level, battery]
        print("state: ", states, ",action: ", action,  ",reward : ", reward)

        states = get_index_with_states(states)
        #print("BBU : learn >> ", action)
        action = get_bbu_index_with_actions(self.sleep_rrh_action, action)

        next_states = get_index_with_states(next_states)

        q_1 = self.q_table[states][action]
        q_2 = reward + self.discount_factor * max(self.q_table[next_states])

        '''try:
        except KeyError:
            self.q_table[next_states] = self.table
            q_2 = reward + self.discount_factor * max(self.q_table[next_states])'''

        self.q_table[states][action] += self.learning_rate * (q_2 - q_1)
        print(self.q_table)

    # 큐함수에 의거하여 입실론 탐욕 정책에 따라서 행동을 반환
    def get_action(self, states, iteration):
        # state : list [active_rrh, throughput]
        # i_state : interference level
        index_states = get_index_with_states(states)
        if len(self.q_table) is 0 :
            # 무작위 행동 반환
            group_action = np.random.choice(self.group_rrh_action)
            sleep_action = np.random.choice(self.sleep_rrh_action)

            action = [group_action, sleep_action]
        elif np.random.rand() > (self.epsilon * iteration):
            # 무작위 행동 반환
            group_action = np.random.choice(self.group_rrh_action)
            sleep_action = np.random.choice(self.sleep_rrh_action)

            action = [group_action, sleep_action]
            print("!!!!!!!!!!",self.group_rrh_action,"중에 group action : ", group_action)
        else:
            # 큐함수에 따른 행동 반환
            state_action = self.q_table[index_states]

            '''try:
            except KeyError:
                self.q_table[index_states] = self.table
                state_action = self.q_table[index_states]'''
            #print(state_action)
            action_index = self.arg_max(state_action)

            action = get_actions_with_index(action_index, self.group_rrh_action, self.sleep_rrh_action)
            # print('**BBU_Q**[', states,'] ->q_table[', index_states, '] : ',state_action)
        return action

    def arg_max(self, state_action):
        # state_action = [0.0, 0.0, ..., 0.0] 총 action의 개수
        # 먼저 mode중 큰 걸 선택, mode가 cellular일 경우 (인덱스0) power는 저절로 인덱스 -1
        max_value = state_action[0]

        action_list = []
        for index, value in enumerate(state_action):
            if value > max_value:
                action_list.clear()
                max_value = value
                action_list.append(index)
            elif value == max_value:
                action_list.append(index)
        # print(action_list, max_value, state_action)
        index = random.choice(action_list)

        return index

class RRH_QLearningAgent:
    def __init__(self):
        self.action = [0, 1] # 0 = sleep, 1 = active
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = 0.9
        # 각각 모든 액션에 대해 m_actions, p_actions 순서
        self.q_table = defaultdict(lambda: [0.0, 0.0])

    # <s, a, r, s'> 샘플로부터 큐함수 업데이트
    def learn(self, states, action, reward, next_states):
        # state : list [interference_level, battery]

        states = get_index_with_states(states)
        action = get_rrh_index_with_actions(action)

        next_states = get_index_with_states(next_states)
        q_1 = self.q_table[states][action]

        q_2 = reward + self.discount_factor * max(self.q_table[next_states])

        '''try:
        except KeyError:
            self.q_table[states] = [0.0, 0.0]
            q_1 = self.q_table[states][action]
        try:
        except KeyError:
            self.q_table[next_states] = [0.0, 0.0]
            q_2 = reward + self.discount_factor * max(self.q_table[next_states])
'''
        self.q_table[states][action] += self.learning_rate * (q_2 - q_1)

    # 큐함수에 의거하여 입실론 탐욕 정책에 따라서 행동을 반환
    def get_action(self, states, iteration):
        # state : list [active_rrh, throughput]
        # i_state : interference level
        index_states = get_index_with_states(states)

        if len(self.q_table) is 0 :
            action = np.random.choice(self.action)


        elif np.random.rand() > (self.epsilon * iteration):
            # 무작위 행동 반환
            action = np.random.choice(self.action)

        else:
            # 큐함수에 따른 행동 반환
            #print('state : ', index_states, self.q_table[index_states])
            state_action = self.q_table[index_states]

            '''try:
            except KeyError:
                self.q_table[index_states] = [0.0,0.0]
                state_action = self.q_table[index_states]'''
            #print('rrh_argmax : ', state_action)
            action = self.arg_max(state_action)
            # print('**BBU_Q**[', states,'] ->q_table[', index_states, '] : ',state_action)
        return action

    def arg_max(self, state_action):
        # state_action = [0.0, 0.0, ..., 0.0] 총 action의 개수
        # 먼저 mode중 큰 걸 선택, mode가 cellular일 경우 (인덱스0) power는 저절로 인덱스 -1
        max_value = state_action[0]

        action_list = []

        for index, value in enumerate(state_action):
            if value > max_value:
                action_list.clear()
                max_value = value
                action_list.append(index)
            elif value == max_value:
                action_list.append(index)
        # print(action_list, max_value, state_action)
        index = random.choice(action_list)

        return get_rrh_actions_with_index(index)

