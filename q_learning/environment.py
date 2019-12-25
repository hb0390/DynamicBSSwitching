import time
from h_cran.params import *
from communication.communication import *
from communication.channel import *
from h_cran.power_params import *
from calculation.calculator_power import *
from calculation.calculation import *
from UE.userequipment import *

class BBU_Env():
    def __init__(self):
        a= 1

    # 현재 state 리턴
    def get_state(self, bbu, ue_list):
        avg_ue_capacity = 0
        for ue in ue_list:
            avg_ue_capacity += calculate_ue_capacity(ue.get_sinr())

        avg_ue_capacity /= len(ue_list)
        avg_ue_capacity = int(round(avg_ue_capacity))


        total_using_RB = len(bbu.get_using_RB_list())
        cellular_using_RB = 0
        for key, values in bbu.get_using_RB_list().items():
            for value in values:
                if not isinstance(value, int):  # d2dlink key가 int기 때문에 int가 아닌경우는 ue 객체인 경우
                    cellular_using_RB += 1

        # 가용 RB
        if total_using_RB != 0:
            cellular_using_RB = (1 - (cellular_using_RB / totalRB)) * 100
        else:
            cellular_using_RB = 100

        cellular_using_RB = cellular_using_RB // 10

        return [avg_ue_capacity, cellular_using_RB]

    def get_next_state(self, outage_probability, bbu, ue_list):
        # bbu_states : [active_rrh, throughput]
        # recommened-actions : [mode, power]
        # selected : True - 추천 받은 액션 사용, False - 추천 사용 X
        avg_sinr = 0
        for bs in bbu.get_rrh_list():
            avg_sinr += bs.get_avg_sinr()

        if avg_sinr >= sinr_constraint :
            system_ee = calculate_system_capacity(bbu, ue_list) / calculate_system_energy(ue_list, bbu)
        else :
            system_ee = -1 * calculate_system_capacity(bbu, ue_list) / calculate_system_energy(ue_list, bbu)

        reward = system_ee

        # 변화한 상태 받아오기기
        next_state = self.get_state(bbu, ue_list)

        # 보상 함수
        return next_state, reward

class RRH_Env():
    def __init__(self):
        a= 1

    # 현재 state 리턴
    def get_state(self,rrh):
        # 사용자수
        serving_rb = rrh.get_serving_RB()
        serving_ue = len(rrh.get_ue_list())

        sinr_of_neighbors = 0
        for neighbor in rrh.neighbor_rrh_list:
            sinr_of_neighbors += neighbor.get_avg_sinr()

        if serving_ue is 0 :
            serving_level = 0
        else :
            serving_level = serving_rb // serving_ue

        if len(rrh.neighbor_rrh_list) is 0:
            sinr_of_neighbors = 0
        else :
            sinr_of_neighbors /= len(rrh.neighbor_rrh_list)

        # time.sleep(0.03)
        avg_sinr = rrh.get_avg_sinr()

        if avg_sinr > sinr_of_neighbors :
            sinr_level = 1 * serving_level
        else :
            sinr_level = -1 * serving_level

        return [sinr_level]

    def get_next_state(self, rrh, ue_list):
        # bbu_states : [active_rrh, throughput]
        # recommened-actions : [mode, power]
        # selected : True - 추천 받은 액션 사용, False - 추천 사용 X

        if rrh.get_state() :

            rrh_power_consumption = rrh_active_power + rrh_slope * (
                            len(rrh.get_ue_list()) * dbmToWatt(transmission_power_rrh))
            fronthaul_power_consumption = fronthaul_constant_power + fronthaul_consumption_power_bit * \
                                               len(rrh.get_ue_list())
        else :
            rrh_power_consumption = rrh_sleep_power
            fronthaul_power_consumption = 0

        avg_neighbor_sinr = rrh.get_avg_sinr()

        for neighbor in rrh.neighbor_rrh_list :

            if neighbor.get_state():
                rrh_power_consumption += rrh_active_power
                rrh_power_consumption += rrh_slope * (
                            len(neighbor.get_ue_list()) * dbmToWatt(transmission_power_rrh))
                fronthaul_power_consumption += fronthaul_constant_power + fronthaul_consumption_power_bit * \
                                               len(neighbor.get_ue_list())

            else:
                rrh_power_consumption += rrh_sleep_power

            avg_neighbor_sinr += neighbor.get_avg_sinr()
        avg_ue_efficiency = avg_neighbor_sinr /(len(rrh.neighbor_rrh_list) + 1)

        #avg_ue_efficiency = calculate_ue_capacity(avg_ue_efficiency)
        reward = avg_ue_efficiency

        # 변화한 상태 받아오기기
        next_state = self.get_state(rrh)

        # 보상 함수
        return next_state, reward
