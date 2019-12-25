from communication.channel import *
from h_cran.params import *
from communication.management_list import *
import operator
import random
from calculation.calculation import *


# Mode-selection 함수 : preparedmode {cellular_mode, d2d_mode}, preparedpair 를 설정
def do_communication_strong(ue_list, all_rrh_list, bbu, transmission_num, num_of_ue):
    '''
       통신을 위해 단말마다 난수를 발생 ( 0 ~ 2U 크기), 발생한 수가 ue key중 하나이면 d2d 검사,
       아니면 cellular 모드가 되는 mode selection을 한다
    '''
    transmission_string = ''
    d2d_list = list()
    d2d_list.clear()
    for ue in ue_list:
        transmission = transmission_num[ue.get_key()]

        transmission_string += str(transmission) + ' '
        # mode_flag 가 False인 단말에 대해서만 조사를 한다 (True는 정해졌거나, 통신요청을 받았다는 뜻)
        if not ue.get_mode_flag():
            if transmission >= num_of_ue or transmission == ue.get_key():
                ue.set_preparedmode(cellular_mode)
                ue.set_mode_flag(True)

            else:
                # 물리적 거리 조건이 안맞으면 cellular 통신
                if get_distance(ue.location_x, ue.location_y, ue_list[transmission].location_x,
                                ue_list[transmission].location_y) > (min_distance_D2D ):
                    ue.set_preparedmode(cellular_mode)
                    ue.set_mode_flag(True)
                    ue_list[transmission].set_preparedmode(cellular_mode)
                    ue_list[transmission].set_mode_flag(True)

                else:
                    ue.set_preparedmode(d2d_mode)
                    ue.set_prepairedpair(transmission)
                    ue.set_mode_flag(True)
                    ue_list[transmission].set_preparedmode(d2d_mode)
                    ue_list[transmission].set_prepairedpair(ue.get_key())
                    ue_list[transmission].set_mode_flag(True)
                    # print('do_communication >> Tx [', ue.get_key(), '] -> Rx [', ue_list[transmission].get_key(), ']')

    for ue in ue_list:
        ue.set_mode_flag(False)

    transmission_string += '\n'
    return transmission_string


# Mode-selection 함수 : preparedmode {cellular_mode, d2d_mode}, preparedpair 를 설정
def do_communication(ue_list, all_rrh_list, bbu, transmission_num, num_of_ue):
    '''
       통신을 위해 단말마다 난수를 발생 ( 0 ~ 2U 크기), 발생한 수가 ue key중 하나이면 d2d 검사,
       아니면 cellular 모드가 되는 mode selection을 한다
    '''
    transmission_string = ''
    d2d_list = list()
    d2d_list.clear()
    for ue in ue_list:
        transmission = transmission_num[ue.get_key()]

        transmission_string += str(transmission) + ' '
        # mode_flag 가 False인 단말에 대해서만 조사를 한다 (True는 정해졌거나, 통신요청을 받았다는 뜻)
        if not ue.get_mode_flag():
            if transmission >= num_of_ue or transmission == ue.get_key():
                ue.set_preparedmode(cellular_mode)
                ue.set_mode_flag(True)

            else:
                # 물리적 거리 조건이 안맞으면 cellular 통신
                if get_distance(ue.location_x, ue.location_y, ue_list[transmission].location_x,
                                ue_list[transmission].location_y) > (min_distance_D2D ):
                    ue.set_preparedmode(cellular_mode)
                    ue.set_mode_flag(True)
                    ue_list[transmission].set_preparedmode(cellular_mode)
                    ue_list[transmission].set_mode_flag(True)

                else:
                    ue.set_preparedmode(d2d_mode)
                    ue.set_prepairedpair(transmission)
                    ue.set_mode_flag(True)
                    ue_list[transmission].set_preparedmode(d2d_mode)
                    ue_list[transmission].set_prepairedpair(ue.get_key())
                    ue_list[transmission].set_mode_flag(True)
                    # print('do_communication >> Tx [', ue.get_key(), '] -> Rx [', ue_list[transmission].get_key(), ']')

                    d2d_list.append([ue, ue_list[transmission]])

    for link in d2d_list:
        sharing_ues = make_sharing_ue_list(link[0].get_key(), link[0].get_usingRB(), ue_list)
        cellular_list = make_sharing_rb_cellular_list(link[0], ue_list)
        mode = mode_selection_comparing_sinr(link[0], link[1], sharing_ues, cellular_list, all_rrh_list)
        #mode = mode_selection_basic(link[0], link[1], all_rrh_list)

        link[0].set_preparedmode(mode)
        link[0].set_tranceiver(tx)

        link[1].set_preparedmode(mode)
        link[1].set_tranceiver(rx)

        d2d_list.remove(link)

    for ue in ue_list:
        ue.set_mode_flag(False)

    transmission_string += '\n'
    return transmission_string


# q_learning 적용 위해 Tx, RX 함수만 만들어 preparedpair 를 설정한다
def make_communication_for_q(ue_list, transmission_num, num_of_ue):
    '''
       통신을 위해 단말마다 난수를 발생 ( 0 ~ 2U 크기), 발생한 수가 ue key중 하나이면 d2d 검사,
       아니면 cellular 모드가 되는 mode selection을 한다
    '''
    transmission_string = ''
    for ue in ue_list:
        transmission = transmission_num[ue.get_key()]
        transmission_string += str(transmission) + ' '
        # mode_flag 가 False인 단말에 대해서만 조사를 한다 (True는 정해졌거나, 통신요청을 받았다는 뜻)

        if not ue.get_mode_flag():
            if transmission >= num_of_ue or transmission == ue.get_key():
                ue.set_preparedmode(cellular_mode)
                ue.set_mode_flag(True)
            else:
                # 물리적 거리 조건이 안맞으면 cellular 통신
                if get_distance(ue.location_x, ue.location_y, ue_list[transmission].location_x,
                                ue_list[transmission].location_y) > min_distance_D2D:
                    ue.set_preparedmode(cellular_mode)
                    ue.set_mode_flag(True)
                    ue_list[transmission].set_preparedmode(cellular_mode)
                    ue_list[transmission].set_mode_flag(True)

                else:
                    ue.set_preparedmode(d2d_mode)
                    ue.set_prepairedpair(transmission)
                    ue.set_tranceiver(tx)
                    ue.set_mode_flag(True)

                    ue_list[transmission].set_preparedmode(d2d_mode)
                    ue_list[transmission].set_prepairedpair(ue.get_key())
                    ue_list[transmission].set_tranceiver(rx)
                    ue_list[transmission].set_mode_flag(True)
                    # print('Tx [', ue.get_key(), '] -> Rx [', ue_list[transmission].get_key(), ']')

    for ue in ue_list:
        ue.set_mode_flag(False)

    transmission_string += '\n'
    return transmission_string


def mode_selection_comparing_sinr(tx_ue, rx_ue, sharing_ues, cellular_ues, rrh_list):
    # 여기서 rrh list는 ue가 범위 내에 있는 rrh들이 속해있다
    # cellular 와 d2d 모드에서의 capacity를 계산하고 더 높은것을 선택하도록 한다
    # 이때, tx 단말과 rx 단말 거리가 d2d 서비스 거리가 되지 않으면 바로 cellular 모드가 선택된다

    close_rrh = find_close_rrh(tx_ue, rrh_list)
    neighbor_rrh_list = rrh_list #get_rrh_list(rx_ue, rrh_list)

    tx_sinr = calc_d2d_sinr(tx_ue, rx_ue, sharing_ues, cellular_ues, neighbor_rrh_list)
    rx_sinr = calc_d2d_sinr(rx_ue, tx_ue, sharing_ues, cellular_ues, neighbor_rrh_list)
    # cellular_sinr = calc_cellular_sinr(rx_ue, close_rrh, neighbor_rrh_list)

    cellular_sinr = calc_cellular_sinr(rx_ue, close_rrh, cellular_ues, sharing_ues, neighbor_rrh_list)

    if rx_sinr >= cellular_sinr:
        tx_ue.set_sinr(tx_sinr)
        rx_ue.set_sinr(rx_sinr)
        return d2d_mode
    else:
        tx_ue.set_sinr(cellular_sinr)
        return cellular_mode


def mode_selection_basic(tx_ue, rx_ue, rrh_list):
    # 여기서 rrh list는 ue가 범위 내에 있는 rrh들이 속해있다
    # 이때, tx 단말과 rx 단말 거리가 d2d 서비스 거리가 되지 않으면 바로 cellular 모드가 선택된다

    close_rrh = find_close_rrh(tx_ue, rrh_list)

    distance_d2d = get_distance(tx_ue.location_x, tx_ue.location_y, rx_ue.location_x, rx_ue.location_y)
    distance_rrh = get_distance(tx_ue.location_x, tx_ue.location_y, close_rrh.location_x, close_rrh.location_y)

    if distance_rrh >= distance_d2d:
        return d2d_mode
    else:
        return cellular_mode


# selected : bbu가 추천해준 action을 사용했는지 자체 action을 사용했는지 리턴 (str)
def mode_selection_with_action(tx_ue, rx_ue, sharing_ues, cellular_ues, rrh_list, recommended_actions, actions):
    # BBU 에서 추천 받은 action과 자체 action과 비교하여 선택한다
    # 추가적으로 BBU에 보내기 위해 selected (bool) 변수를 리턴한다
    selected_difference = 0
    close_rrh = find_close_rrh(tx_ue, rrh_list)
    neighbor_rrh_list = rrh_list#get_rrh_list(rx_ue, rrh_list)
    # cellular_sinr = calc_cellular_sinr(rx_ue, close_rrh, neighbor_rrh_list)
    cellular_sinr = calc_cellular_sinr(rx_ue, close_rrh, cellular_ues, sharing_ues, neighbor_rrh_list)

    # recommended_action
    # print(recommended_actions)
    if recommended_actions[0] == cellular_mode:
        recommended_sinr = cellular_sinr
    else:
        recommended_sinr = calc_expected_d2d_sinr(rx_ue, tx_ue, recommended_actions[1], sharing_ues, cellular_ues,
                                                  neighbor_rrh_list)

    # action
    if actions[0] == cellular_mode:
        self_sinr = cellular_sinr
    else:
        self_sinr = calc_expected_d2d_sinr(rx_ue, tx_ue, actions[1], sharing_ues, cellular_ues, neighbor_rrh_list)

    # 비교
    if recommended_sinr * 1.2 < self_sinr:
        rx_sinr = self_sinr
        tx_sinr = calc_expected_d2d_sinr(rx_ue, tx_ue, actions[1], sharing_ues, cellular_ues, neighbor_rrh_list)
        mode = actions[0]
        power = actions[1]
        selected_difference = recommended_sinr - self_sinr
        selected = False

    else:
        rx_sinr = recommended_sinr
        tx_sinr = calc_expected_d2d_sinr(rx_ue, tx_ue, recommended_actions[1], sharing_ues, cellular_ues,
                                         neighbor_rrh_list)
        mode = recommended_actions[0]
        power = recommended_actions[1]
        selected_difference = 0
        selected = True

    if mode == d2d_mode:
        tx_ue.set_sinr(tx_sinr)
        rx_ue.set_sinr(rx_sinr)
    else:
        tx_ue.set_sinr(cellular_sinr)

    return mode, power, selected, selected_difference


# User-association 함수 : 성공적인 ua 는 1, 실패는 2를 반환한다
def ua(cellular_list, ue_list, bbu, rrh_list):
    sinr_list = dict()
    while len(cellular_list) > 0:
        for ue in cellular_list:
            sharing_ues = make_sharing_ue_list(ue.get_key(), ue.get_usingRB(), ue_list)
            for x in rrh_list:
                # sinr = calc_cellular_sinr(ue, x, neighbor_rrh_list)
                sinr = calc_cellular_sinr(ue, x, cellular_list, sharing_ues, rrh_list)
                sinr_list[x.key] = sinr

            sorted_sinr_list = sorted(sinr_list.items(), key=operator.itemgetter(1), reverse=True)
            # sorted_sinr_list (: list type) : [RRH_key, sinr]
            old_mode = ue.get_mode()
            old_pair = ue.get_pair()

            for x in sorted_sinr_list:
                if rrh_list[x[0]].active:
                    if old_mode == cellular_mode and x[0] == old_pair:
                        # 이전에 연결되어있는 RRH가 optimal sinr을 제공할 경우 -> 그대로 연결
                        cellular_list.remove(ue)
                        ue.set_sinr(x[1])
                        break
                    elif rrh_list[x[0]].available:
                        # optimal sinr을 제공하는 rrh가 다른 rrh라면 그 rrh가 available(즉 가용 자원이 있어야함)해야 한다
                        # 이전에 서비스 받던 애들 원래대로 돌리기 / 자원 할당처리
                        if old_mode == d2d_mode:
                            # d2d 모드였던 경우
                            bbu.return_rb(ue.get_usingRB(), ue.link_key)
                            allocated_RB = bbu.allocate_rb(ue)


                        elif old_mode == cellular_mode:
                            # 계속해서 cellular 통신을 하는 경우 RB 유지
                            allocated_RB = ue.get_usingRB()

                            if old_pair != ue.get_preparedpair():
                                # 핸드 오버의 경우
                                rrh_list[old_pair].unserve(ue)

                        elif old_mode == detection:
                            # 첫 통신 시작의 경우
                            allocated_RB = bbu.allocate_rb(ue)

                    rrh_list[x[0]].serve(ue, x[1], allocated_RB)

                    ue.set_mode(cellular_mode)
                    ue.set_pair(x[0])
                    ue.set_sinr(x[1])
                    ue.set_usingRB(allocated_RB)
                    ue.set_rrh_pair(x[0])

                    cellular_list.remove(ue)
                    break
    return 0
    # print(cellular_list)

def d2d_communication(bbu, num_of_ue, ue_list, cellular_ues):
    # d2dlink_list = [ [tx_ue, rx_ue], [tx_ue, rx_ue], ..., ]
    d2dlink_list = bbu.get_D2D_list()
    # pprint.pprint(bbu.get_using_RB_list())
    for link_key, pair in d2dlink_list.items():
        for ue in pair:
            # 이전과 동일한 단말과 D2D 통신을 이어서 하는 경우 RB 그대로 할당
            if ue.get_mode() == d2d_mode and ue.get_pair() == ue.get_preparedpair():
                rb = ue.get_usingRB()

            # 이전에 이용하던 자원을 삭제
            else:
                if ue.get_mode() == cellular_mode:
                    # 이전에 cellular 였던 경우
                    bbu.return_rb(ue.get_usingRB(), ue)
                elif ue.get_mode() == d2d_mode and ue.get_pair() != ue.get_preparedpair():
                    # 이전에 d2d 였던 경우 (상대 단말이 바뀐 경우에만)
                    bbu.return_rb(ue.get_usingRB(), ue.link_key)

                # 링크키 설정
                ue.link_key = link_key

        # 새롭게 D2D 자원 할당
        rb = bbu.allocate_d2d_rb(pair[0], link_key, num_of_ue)
        pair[0].set_usingRB(rb)

        rb = bbu.allocate_d2d_rb(pair[1], link_key, num_of_ue)
        pair[1].set_usingRB(rb)


        pair[0].set_mode(d2d_mode)
        pair[0].set_tranceiver(tx)
        pair[0].set_pair(pair[1].get_key())
        pair[1].set_mode(d2d_mode)
        pair[1].set_tranceiver(rx)
        pair[1].set_pair(pair[0].get_key())

        # 자원을 링크단위로 새로 할당 받는다

        sharing_ues = make_sharing_ue_list(pair[0], pair[0].get_usingRB(), ue_list)


        neighbor_rrh_list = get_rrh_list(pair[0], bbu.get_rrh_list())
        cellular_ue = make_sharing_rb_cellular_list(pair[0], cellular_ues)

        pair[0].set_sinr(calc_d2d_sinr(pair[0], pair[1], sharing_ues, cellular_ue, bbu.get_rrh_list()))

        cellular_ue = make_sharing_rb_cellular_list(pair[1], cellular_ues)
        neighbor_rrh_list = get_rrh_list(pair[1], bbu.get_rrh_list())
        pair[1].set_sinr(calc_d2d_sinr(pair[1], pair[0], sharing_ues, cellular_ue, bbu.get_rrh_list()))

        pair[0].set_rrh_pair(find_close_rrh(pair[0], bbu.get_rrh_list()).get_key())
        pair[1].set_rrh_pair(find_close_rrh(pair[1], bbu.get_rrh_list()).get_key())

