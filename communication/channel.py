import math
from calculation.calculation import *
from h_cran.params import *
from communication.management_list import *


def get_rrh_channelgain(rrh, rx_ue):
    distance = get_distance(rrh.location_x, rrh.location_y, rx_ue.location_x, rx_ue.location_y)
    return 15.3 + 37.6 * math.log(distance, 10)


def get_ue_channelgain(tx_ue, rx_ue):
    if tx_ue == rx_ue:
        print('동일한 ue 오류')
    distance = get_distance(tx_ue.location_x, tx_ue.location_y, rx_ue.location_x, rx_ue.location_y)
    if distance == 0:
        return 28
    else:
        return 28 + 40 * math.log(distance, 10)


def calculate_system_capacity(bbu, ue_list):
    rb_capacity = 0

    for rb, using_ue_list in bbu.get_using_RB_list().items():
        d2d_links_sinr = 0
        cellular_sinr = 0
        for ue in using_ue_list:
            # d2d_link인 경우 : ue는 d2d_link의 키 값이 된다 (ue가 min_d2dlink_key보다 클때)

            if isinstance(ue, int) and ue >= min_d2dlink_key:
                if bbu.find_d2dlink(ue) is True:
                    d2d_link = bbu.get_d2dlink(ue)
                    try:
                        d2d_links_sinr += math.log(1 + d2d_link[0].get_sinr()+ d2d_link[1].get_sinr(), 2)

                    except ValueError as e:
                        d2d_links_sinr += math.log(1 + 0, 2)

                    #try:
                    #    d2d_links_sinr += math.log(1 + d2d_link[1].get_sinr(), 2)
                    #except ValueError as e:
                    #    d2d_links_sinr += math.log(1 + 0, 2)
            # cellular인 경우
            else:
                try:
                    cellular_sinr += math.log(1 + ue.get_sinr(), 2)
                except ValueError as e:
                    cellular_sinr += math.log(1 + 0, 2)

        rb_capacity += cellular_sinr + (d2d_links_sinr/2)



    system_capacity = bandwidth * (rb_capacity)
    return system_capacity


def calculate_rrh_capacity(rrh, ue_list):
    rrh_capacity = 0
    for ue in ue_list:
        if ue.get_rrh_pair() == rrh.get_key() and rrh.get_state():
            try:
                rrh_capacity += math.log(1 + ue.get_sinr(), 2)
            except ValueError as e:
                rrh_capacity += math.log(1 + 0, 2)

    rrh_capacity = rrh_capacity * bandwidth

    return rrh_capacity


def calculate_ue_capacity(sinr):
    try:
        capacity = math.log(1 + sinr, 2)
    except ValueError as e:
        capacity = math.log(1 + 0, 2)

    #    if capacity < 0:
    #       capacity = 0

    return single_bandwidth * capacity


def calc_cellular_sinr(ue, rrh, cellular_ues, sharing_ues, interference_rrh_list):
    interference_from_rrh = 0
    active_num = 0
    for x in interference_rrh_list:
        if rrh.key != x.key and x.get_state():
            active_num += 1
            interference_from_rrh += transmission_power_rrh - get_rrh_channelgain(x, ue)


    numerator = transmission_power_rrh - get_rrh_channelgain(rrh, ue)
    denorminator = (interference_from_rrh)
    #print("active : ",active_num," : ",numerator,"/", denorminator)
    if denorminator != 0:
        sinr = numerator / denorminator
    else:
        sinr = numerator

    ue.set_interference(denorminator)
    # print('cellular_sinr(', sinr, '),')
    # print('분자 (',cellular_power - get_rrh_channelgain(rrh, ue),') : ',cellular_power,' - ', get_rrh_channelgain(rrh, ue))
    # print('분모 (',interference_from_rrh + interference_from_sharing_ues + interference_from_cellular,') : ',interference_from_rrh,' + ', interference_from_sharing_ues ,' + ', interference_from_cellular)
    return sinr* 10


def calc_d2d_sinr(tx_ue, rx_ue, sharing_ues, cellular_ues, neighbor_rrh_list):
    interference_from_sharing_ues = 0
    for x in sharing_ues:
        if not x == rx_ue:
            interference_from_sharing_ues += x.power - get_ue_channelgain(x, rx_ue)

    interference_from_cellular = 0
    for cellular_ue in cellular_ues:
        if cellular_ue != rx_ue:
            interference_from_cellular += cellular_ue.power - get_ue_channelgain(rx_ue, cellular_ue)

    interference_from_rrh = 0
    for x in neighbor_rrh_list:
        interference_from_rrh += transmission_power_rrh - get_rrh_channelgain(x, rx_ue)

    numerator = rx_ue.power - get_ue_channelgain(tx_ue, rx_ue)
    denorminator = (interference_from_cellular + interference_from_sharing_ues + interference_from_rrh)

    if denorminator != 0:
        d2d_sinr = numerator / denorminator
    else:
        d2d_sinr = numerator

    tx_ue.set_interference(denorminator)

    # print('d2d_sinr(', d2d_sinr, '),')
    # print('분자 (',numerator,') : ',rx_ue.power,' - ', get_ue_channelgain(tx_ue, rx_ue))
    # print('분모 (',denorminator,') : ',interference_from_cellular,' + ', interference_from_sharing_ues)

    return d2d_sinr* 5

def calc_expected_d2d_sinr(tx_ue, rx_ue, power, sharing_ues, cellular_ues, rrh_list):
    interference_from_rrh = 0
    for x in rrh_list:
        interference_from_rrh += transmission_power_rrh - get_rrh_channelgain(x, rx_ue)

    interference_from_sharing_ues = 0
    for x in sharing_ues:
        if not x == rx_ue:
            interference_from_sharing_ues += x.power - get_ue_channelgain(x, rx_ue)

    interference_from_cellular = 0
    for cellular_ue in cellular_ues:
        if cellular_ue != rx_ue:
            interference_from_cellular += cellular_ue.power - get_ue_channelgain(rx_ue, cellular_ue)

    numerator = power - get_ue_channelgain(tx_ue, rx_ue)
    denorminator = (interference_from_cellular + interference_from_sharing_ues + interference_from_rrh)

    if denorminator != 0:
        d2d_sinr = numerator / denorminator
    else:
        d2d_sinr = numerator

    tx_ue.set_interference(denorminator)

    # print('expected d2d_sinr(', d2d_sinr, '),')
    # print('분자 (',numerator,') : ',rx_ue.power,' - ', get_ue_channelgain(tx_ue, rx_ue))
    # print('분모 (',denorminator,') : ',interference_from_cellular,' + ', interference_from_sharing_ues)
    return d2d_sinr * 5
