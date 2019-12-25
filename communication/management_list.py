from calculation.calculation import *
from communication.channel import *
from h_cran.params import *
import operator
import pprint


# make_sharing_rb_cellular_list : 같은 rb를 공유하고 있는 cellular 모드 리스트를 리턴해주는 함수
def make_sharing_rb_cellular_list(param_ue, ue_list):
    cellular_list = list()

    for ue in ue_list:
        if ue != param_ue:
            cellular_list.append(ue)

    return cellular_list


# get_rrh_list : 서비스 반경에 들어가있는 rrh 리스트를 리턴해주는 함수
def get_rrh_list(ue, all_rrh_list):
    """
    :type ue: ue class
    :type all_rrh_list: list of rrh
    """
    # ue가 반경안에 들어있는 rrh만 리스트화
    '''rrh_list = list()
    for x in all_rrh_list:
        if  min_distance_RRH < get_distance(ue.location_x, ue.location_y, x.location_x, x.location_y) <= max_distance_RRH * 2:
            rrh_list.append(x)
    return rrh_list'''
    return all_rrh_list


# d2d 단말 중 동일한 자원을 공유하고 있는 단말 리스트를 리턴
def make_sharing_ue_list(key, rb, ue_list):
    sharing_ue_list = list()

    for ue in ue_list:
        if ue.get_mode() == d2d_mode :
            if ue.get_usingRB() == rb and ue.get_key() != key:
                sharing_ue_list.append(ue)

    return sharing_ue_list


def make_cellular_list(ue_list):
    cellular_list = list()
    for ue in ue_list:
        if ue.get_preparedmode() == cellular_mode:
            cellular_list.append(ue)
    return cellular_list

def make_all_d2d(bbu, ue_list) :
    for ue in ue_list:
        new_link_key = make_d2dlink_key(ue.get_key(), ue.get_preparedpair())
        old_link_key = ue.link_key

        # 최초 통신
        if old_link_key == detection:
            if not new_link_key in bbu.get_D2D_list():
                bbu.get_D2D_list()[new_link_key] = [ue, ue_list[ue.get_preparedpair()]]

        # 새로 d2d 통신을 하거나(cellular모드) 다른 단말과 d2d 통신을 새로 하게 되었다면
        elif old_link_key != new_link_key:
            # 기존의 d2d list에서 link를 삭제함
            bbu.remove_d2dlink(old_link_key)

            # 그리고 생성한 링크키와 함께 d2d list에 삽입해준다
            if not new_link_key in bbu.get_D2D_list():
                bbu.get_D2D_list()[new_link_key] = [ue, ue_list[ue.get_preparedpair()]]

        # pprint.pprint(bbu.get_D2D_list())
    return bbu.get_D2D_list()

def make_d2dlink_list(bbu, ue_list):
    #pprint.pprint(bbu.get_D2D_list())
    for ue in ue_list:
        # preparedmode 가 D2D 모드인 단말들에 대해서만
        if ue.get_preparedmode() == d2d_mode :
            new_link_key = make_d2dlink_key(ue.get_key(), ue.get_preparedpair())
            old_link_key = ue.link_key

            #최초 통신
            if old_link_key == detection :
                if not new_link_key in bbu.get_D2D_list():
                    bbu.get_D2D_list()[new_link_key] = [ue, ue_list[ue.get_preparedpair()]]

            # 새로 d2d 통신을 하거나(cellular모드) 다른 단말과 d2d 통신을 새로 하게 되었다면
            elif ue.get_mode == cellular_power or old_link_key != new_link_key:
                # 기존의 d2d list에서 link를 삭제함
                bbu.remove_d2dlink(old_link_key)

                # 그리고 생성한 링크키와 함께 d2d list에 삽입해준다
                if not new_link_key in bbu.get_D2D_list() :
                    bbu.get_D2D_list()[new_link_key] = [ue, ue_list[ue.get_preparedpair()]]


    #pprint.pprint(bbu.get_D2D_list())
    return bbu.get_D2D_list()


def make_d2dlink_key(ue_key1, ue_key2):
    return 1000 + (ue_key1 + ue_key2) + (ue_key1 * ue_key2)


def find_close_rrh(ue, rrh_list):
    distance = list()

    for rrh in rrh_list:
        distance.append([rrh_list.index(rrh), get_distance(ue.location_x, ue.location_y, rrh.location_x, rrh.location_y)])
    sorted_list = sorted(distance, key=lambda x : x[1])
    for rrh_pair in sorted_list:
        #print(rrh_pair[0],len(rrh_list))
        return rrh_list[rrh_pair[0]]


def find_ue_by_key(key, ue_list):
    for ue in ue_list:
        if ue.get_key() == key:
            return key

    return False
