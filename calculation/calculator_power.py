from h_cran.params import *
from calculation.calculation import *
from communication.channel import *
from h_cran.power_params import *
import math
def calculate_system_energy(ue_list, bbu):
    rrh_transmission_list = list()
    for rrh in range(len(bbu.get_rrh_list())):
        rrh_transmission_list.append(0)# rrh의 개수대로

    total_transmission = 0
    fronthaul_power_consumption = 0

    for ue in ue_list:
        if ue.get_mode() == cellular_mode and ue.get_pair() < min_d2dlink_key :
            rrh_transmission_list[ue.get_pair()] = rrh_transmission_list[ue.get_pair()] + 1
            total_transmission = total_transmission + 1

    rrh_power_consumption = 0
    for rrh in bbu.get_rrh_list() :
        if rrh.get_state() :
            rrh_power_consumption += rrh_active_power
            rrh_power_consumption += rrh_slope * (rrh_transmission_list[rrh.get_key()] * dbmToWatt(transmission_power_rrh))
            fronthaul_power_consumption += fronthaul_constant_power + fronthaul_consumption_power_bit * rrh_transmission_list[rrh.get_key()]

        else :
            rrh_power_consumption += rrh_sleep_power
    #rrh_power_consumption = rrh_active_power + rrh_slope * (total_transmission * dbmToWatt(transmission_power_rrh))

    total_consumption = (rrh_power_consumption + fronthaul_power_consumption)
    return total_consumption


