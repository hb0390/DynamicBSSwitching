from h_cran.params import *
import random
import operator
import copy
import pprint
from q_learning.environment import *
from q_learning.q_learning_agent import *
from collections import defaultdict
from UE.userequipment import *


class BBU:
    def __init__(self, num_of_ue):
        self.rrh_list = list()
        self.using_RB_list = dict()
        self.D2D_list = dict()
        self.sinr_constraint = sinr_constraint
        self.outage_probability = 0
        self.n_active_rrh = num_of_RRH

        expected_cellular_ue = num_of_ue

        '''if min_distance_D2D == distance_150:
            expected_cellular_ue = int(num_of_ue * 0.9)

        elif min_distance_D2D == distance_250:
            expected_cellular_ue = int(num_of_ue * 0.7)

        elif min_distance_D2D == distance_350:
            expected_cellular_ue = int(num_of_ue * 0.5)'''

        for rrh in range(num_of_RRH):
            if size_RB * rrh > 4 * num_of_ue:
                self.max_sleep_rrh = num_of_RRH - rrh
                break

        self.old_states = list()
        self.env = BBU_Env()

        self.agent = BBU_QLearningAgent(self.max_sleep_rrh)
        self.n_sleep_rrh = 0
        self.n_group_rrh = 0
        self.rrh_group = list()

    def insert_RRH(self, key, x, y):
        self.rrh_list.append(RRH(key, x, y))

    def get_RRH(self, key):
        key = int(key)

        for rrh in self.rrh_list:
            if key == rrh.get_key():
                return rrh
        return False

    def get_rrh_list(self):
        return self.rrh_list

    def get_using_RB_list(self):
        return self.using_RB_list

    # cellular 단말에 자원을 할당, 할당한 rb를 리턴
    def allocate_rb(self, ue):
        # RB를 할당하기 위해 RB 넘버를 뽑는다
        # 이때, cellular 단말은 아무도 사용하지 않는 또는 d2d만 이용하고 있는 RB를 할당 받는다

        if len(self.using_RB_list) == totalRB:
            rb = self.find_possible_rb()
        else:
            for new in range(totalRB):
                if not new in self.using_RB_list:
                    rb = new
                    break

        using_ue = list()
        using_ue.append(ue)

        self.using_RB_list[rb] = using_ue

        # print("BBU>allocate_rb() : pprint")
        # pprint.pprint(self.using_RB_list)

        return rb

    def allocate_d2d_rb(self, ue, d2d_key, num_of_ue):
        if len(self.using_RB_list) == 0:
            rb = random.randint(0, totalRB - 1)
            using_ue = list()
        else:
            # rb = self.find_reusable_rb_minusage(num_of_ue)
            rb = self.find_reusable_rb_mindistance(ue, num_of_ue)
            using_ue = self.using_RB_list[rb]
            if rb == detection:
                print(detection, '뭐냐이거 ??')

        using_ue.append(d2d_key)

        self.using_RB_list[rb] = using_ue

        return rb

    def return_rb(self, rb, ue):
        # rb에서 올바른 키를 가진 단말(또는 d2d링크)를 삭제하고, rb를 사용하는 단말이 아예 없으면 list에서 삭제한다

        if rb in self.using_RB_list:
            if ue in self.using_RB_list[rb]:
                self.using_RB_list[rb].remove(ue)

                if len(self.using_RB_list[rb]) == 0:
                    del self.using_RB_list[rb]

    def find_usingrb_ue_list(self, rb):
        return self.using_RB_list[rb]

    # cellular ue가 없는 RB를 찾는다
    def find_possible_rb(self):
        possible_rb_list = list(self.using_RB_list.keys())
        # pprint.pprint(self.using_RB_list)
        # pprint.pprint(self.get_D2D_list())
        # print(possible_rb_list)
        for key, values in self.using_RB_list.items():
            for value in values:
                if isinstance(value, UE) and key in possible_rb_list:
                    possible_rb_list.remove(key)

        rb = random.choice(possible_rb_list)

        return rb

    # 사용자수가 가작 적은 cellular 할당된 RB를 리턴한다
    def find_reusable_rb_minusage(self, num_of_ue):
        rb_number_list = dict()
        ue_num = 0
        # print("BBU>fine_reusable_rb() : 아니대체 디텍션 어서 튀어나오는겨")
        # pprint.pprint(self.using_RB_list)
        for key, value in self.using_RB_list.items():
            if value is None or len(value) == 0:
                rb_number_list[key] = num_of_ue * num_of_ue
            else:
                ue_num = 0
                for ue in value:
                    if not isinstance(ue, int):
                        ue_num += 1
                rb_number_list[key] = ue_num
        rb = min(rb_number_list.items(), key=operator.itemgetter(1))[0]
        return rb

    # 사용자수가 가작 적은 cellular 할당된 RB를 리턴한다

    def find_reusable_rb_mindistance(self, d2d_ue, num_of_ue):
        rb_number_list = dict()
        # print("BBU>fine_reusable_rb() : 아니대체 디텍션 어서 튀어나오는겨")
        # pprint.pprint(self.using_RB_list)
        for key, value in self.using_RB_list.items():
            if value is None or len(value) == 0:
                rb_number_list[key] = 0
            else:
                ue_num = 0
                for ue in value:
                    if isinstance(ue, UE):
                        rb_number_list[key] = get_distance(d2d_ue.location_x, d2d_ue.location_y, ue.location_x,
                                                           ue.location_y)

        if len(rb_number_list) == 0:
            ue_num = 0
            for key, value in self.using_RB_list.items():
                for ue in value:
                    if not isinstance(ue, int):
                        ue_num += 1
                rb_number_list[key] = ue_num

        rb = min(rb_number_list.items(), key=operator.itemgetter(1))[0]
        return rb

    # bbu에서 d2dlink를 관리
    def get_D2D_list(self):
        return self.D2D_list

    def remove_d2dlink(self, link_key):
        if link_key in self.D2D_list:
            del self.D2D_list[link_key]

    # 인자로 넣은 key를 갖는 d2d링크를 리턴
    def get_d2dlink(self, key):
        if key in self.D2D_list:
            return self.D2D_list.get(key)

    # 인자로 넣은 key를 갖는 d2d링크의 존재여부를 리턴
    def find_d2dlink(self, key):
        if key in self.D2D_list:
            return True
        else:
            return False

    def get_num_of_active_rrh(self):
        num = 0
        for rrh in self.rrh_list:
            if rrh.get_state():
                num += 1
        return num

    def set_n_sleep_rrh(self, n_sleep_rrh):
        self.n_sleep_rrh = n_sleep_rrh

    def get_n_sleep_rrh(self):
        return self.n_sleep_rrh

    def set_n_group_rrh(self, n_group_rrh):
        self.n_group_rrh = n_group_rrh

    def get_n_group_rrh(self):
        return self.n_group_rrh

    def set_neighbor_rrhs(self):
        for x in self.rrh_list:
            neighbor_rrh_list = list()
            for neighbor in self.rrh_list:
                if neighbor != x :
                    if get_distance(x.location_x, x.location_y, neighbor.location_x,
                                                       neighbor.location_y) <= max_distance_RRH:
                        neighbor_rrh_list.append(neighbor)

            x.neighbor_rrh_list = neighbor_rrh_list

class RRH:
    def __init__(self, key, x, y):
        self.key = int(key)
        self.active = True
        self.available = True
        self.location_x = float(x)
        self.location_y = float(y)
        self.remainRB = size_RB
        self.ue_list = list()
        self.minimum_sinr = 5
        self.avg_sinr = 0
        self.serving_RB = 0
        self.old_states = list()
        self.env = RRH_Env()
        self.agent = RRH_QLearningAgent()
        self.head = False
        self.load_score = 0
        self.neighbor_rrh_list = list()
        self.voting_point = 0
        self.action = 1
    def get_state(self):
        return self.active

    def get_info(self):
        print('key :', self.key)

    def get_key(self):
        return self.key

    def get_ue_list(self):
        return self.ue_list

    def serve(self, ue, sinr, rb):
        if not ue in self.ue_list:
            self.ue_list.append(ue)
            self.remainRB = self.remainRB - ue.get_usingRB()
            self.serving_RB += ue.get_usingRB()

    def unserve(self, ue):
        if ue in self.ue_list:
            self.ue_list.remove(ue)
            self.remainRB = self.remainRB  + ue.get_usingRB()
            self.serving_RB -= ue.get_usingRB()

    def set_avg_sinr(self, sinr):
        self.avg_sinr = sinr

    def get_avg_sinr(self):
        return self.avg_sinr

    def activate(self):
        self.active = True

    def sleep(self):
        self.active = False

    def get_serving_RB(self):
        return self.serving_RB