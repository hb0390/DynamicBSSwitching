from h_cran.params import *
import random
import operator
import pprint
from UE.userequipment import *


def sleep_mechanism(bbu, rrh_list):
    rrh_group_index = 0

    voting_point_in_group = list()
    total_voting_point_in_group = list()

    # rrh action 대로 끄고,
    # 만약 숫자가 부족하면 추가적으로 voting point 가장 작은 애를 끈다
    sleep_number = bbu.max_sleep_rrh
    sleep = num_of_RRH - bbu.get_num_of_active_rrh()
    for rrh_members in bbu.rrh_group:
        for rrh in rrh_members:
            if rrh.action == 0:
                if sleep < sleep_number:

                    sleep += 1

                    if rrh.get_state():  # active 상태이면
                        rrh.sleep()
                else :
                    break
            else :
                if not rrh.get_state():
                    rrh.activate()

        voting_point_in_group = list()
        for rrh in rrh_members:
            voting_point_in_group.append([rrh.get_key(), rrh.voting_point])

        voting_point_in_group = sorted(voting_point_in_group, key=lambda x: x[1])
        total_voting_point_in_group.append(voting_point_in_group)
    print("sleep : ", sleep, "max_num : ", bbu.max_sleep_rrh, "active :", bbu.get_num_of_active_rrh())

    sleep_number = sleep_number - sleep
    count = 0
    while sleep_number > 0 :
        print("여기서 걸리나봐..")
        #print("sleep_number : ", sleep_number, "max_sleep_num : ", bbu.max_sleep_rrh)
        if count is 10:
            break
        for voting_points_in_group in total_voting_point_in_group :
            for pair in voting_points_in_group:
                #print(rrh_list[pair[0]].get_key(), '>>', rrh_list[pair[0]].get_state())
                if rrh_list[pair[0]].get_state(): # active 상태이면
                    rrh_list[pair[0]].sleep()
                    sleep_number = sleep_number - 1
                    break

            if sleep_number <= 0:
                break
        count +=1





