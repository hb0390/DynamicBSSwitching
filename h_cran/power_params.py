import math
from calculation.calculation import *
#cellular
basic_power_cellular = 1288.04
scaling_factor_cellular_tx = 438.39


#d2d
scaling_factor_d2d_tx = 283.17
basic_tx_d2d = 132.86

#power model
peukert_constant = 1.038

#rrx : received data rate of rx
#srx : received power of rx

def calc_power_tx_cellular(rrx):
    # power = basic_power_cellular + baseband_tx_cellular + calc_rb_tx(stx) + basic_tx_cellular
    power = (scaling_factor_cellular_tx * rrx + basic_power_cellular) * 0.001 * 60
    return power

def calc_power_tx_d2d(rtx):
    return (scaling_factor_d2d_tx * rtx + basic_tx_d2d) * 0.001 * 60