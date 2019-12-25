epoch = 10

#대기
detection = -7777

#ue 관련
circuit_power_ue = 0.01 #10mW, 10dbm

#cellular관련
cellular_mode = 'c'
cellular_power = 23
max_cellular_power = 23

# simulater_params
distance_150 = 0.15
distance_250 = 0.25
distance_350 = 0.35

#D2D 관련
d2d_mode = 'd'
min_distance_D2D = distance_150  # 0.25 #0.15
min_d2dlink_key = 1000
max_d2d_power = 23
tx = 'Tx'
rx = 'Rx'

#RRH 관련
num_of_RRH = 45
max_distance_RRH = 0.5
min_distance_RRHi = 0.015
transmission_power_rrh = 43


#system
bandwidth = 100
num_of_bbu = 4
size_RB = 80
totalRB = size_RB * num_of_RRH
single_bandwidth = 180

sinr_constraint = 2
system_outage_max = 1
system_outage_min = 0.01


rrh_group_size = 3

#energy consumption 관련
number_of_tranceiver = 6
rrh_active_power = 6.8 # W
rrh_sleep_power = 4.3
rrh_slope = 4.0
backhaul_power = 13.25
fronthaul_consumption_power_bit = 0.83
fronthaul_constant_power = 13


static_power_cue = 1288.04
static_power_due = 132.86
slope_cue = 51.97
slope_due = 137.01