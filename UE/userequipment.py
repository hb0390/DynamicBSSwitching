from h_cran.params import *
from q_learning.environment import *
from q_learning.q_learning_agent import *


class UE:
    def __init__(self, sim_mode, key, resource, mobility_list):
        self.mobility_list = mobility_list
        self.key = int(key)
        self.location_x = float(mobility_list[0][0])
        self.location_y = float(mobility_list[0][1])
        self.battery = 26580  # mAh
        self.consumed_power = 0
        self.mode = detection
        self.tranceiver = detection
        self.prepared_mode = cellular_mode
        self.prepared_pair = cellular_power
        self.mode_flag = False
        self.pair = detection
        self.power = max_d2d_power

        self.rrh_pair = detection

        self.sinr = 0
        self.usingRB = detection
        self.link_key = detection
        self.old_states = ['']
        self.RB_usage = int(resource)
        self.interference = 0

    def get_ue(self):
        print(self.key, self.location_x, self.location_y, self.mode, self.usingRB)

    def get_key(self):
        return self.key

    def move(self, iteration):
        self.location_x = float(self.mobility_list[iteration][0]) * 0.5 + 0.25
        self.location_y = float(self.mobility_list[iteration][1]) * 0.5 + 0.25

    def get_location(self):
        return self.location_x, self.location_y

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode

    def get_preparedmode(self):
        return self.prepared_mode

    def set_preparedmode(self, mode):
        self.prepared_mode = mode

    def get_preparedpair(self):
        return self.prepared_pair

    def set_prepairedpair(self, pair):
        self.prepared_pair = pair

    def get_mode_flag(self):
        return self.mode_flag

    def set_mode_flag(self, bool_):
        if bool_ == True:
            self.mode_flag = True
        else:
            self.mode_flag = False

    def set_pair(self, pair):
        self.pair = pair

    def get_pair(self):
        return self.pair

    def set_usingRB(self, rb):
        self.usingRB = rb

    def get_usingRB(self):
        return self.usingRB

    def set_sinr(self, sinr):
        self.sinr = sinr

    def get_sinr(self):
        return self.sinr

    def set_power(self, power):
        self.power = power

    def get_power(self):
        return self.power

    def get_battery(self):
        return self.battery

    def set_interference(self, interference):
        self.interference = interference

    def get_interference(self):
        return self.interference

    def set_RB_usage(self, RB_usage):
        self.RB_usage = RB_usage

    def get_RB_usage(self):
        return self.RB_usage

    def set_tranceiver(self, tranceiver):
        self.tranceiver = tranceiver

    def get_tranceiver(self):
        return self.tranceiver

    def get_rrh_pair(self):
        return self.rrh_pair

    def set_rrh_pair(self, rrh_pair):
        self.rrh_pair = rrh_pair
