from h_cran.params import *
from UE.userequipment import *
from h_cran.hcran import *
import operator


# single cell, 1 BBU pool,
def initialize_with_single_cell(sim_mode, num_of_ue, episode):
    # RRH의 위치를 읽어와 rrh 개수 대로 BBU에 rrh_list에 넣는다
    location_file = open('location_of_rrh_1x1_60.txt', mode='rt', encoding='utf-8')#open('location_of_rrh_1x1_'+str(num_of_RRH)+'.txt', mode='rt', encoding='utf-8')
    rrh_location = location_file.readlines()

    # ue list 생성
    ue_list = list()
    bbu = BBU(num_of_ue)

    for location in range(num_of_RRH):
        location = rrh_location[location].split(' ')
        bbu.insert_RRH(location[0], location[1], location[2])
    location_file.close()

    bbu.set_neighbor_rrhs()

    '''for group in group_list:
        for rrh in group:
            print(rrh.get_key(), end=",")
        print(" ")'''


    # UE의 위치를 읽어와 ue 개수 대로 ue list에 넣는다
    txt = '.txt'

    resource_file = open('resource_gaussian_1.txt', mode='rt', encoding='utf-8')
    # anwhere
    print("adfliasdjlifsadl")
    ue_resource = resource_file.readlines()
    for ue in range(num_of_ue):
        resource = ue_resource[ue].split(' ')

        mobility_list = read_mobility_list_from_file(ue, episode)
        # print(mobility_list)

        ue_list.append(UE(sim_mode, str(ue), resource[-1], mobility_list))

    # 모든 UE를 cellular 모드로 association한다
    cellular_list = make_cellular_list(ue_list)
    ua(cellular_list, ue_list, bbu, bbu.get_rrh_list())

    return bbu, ue_list


def read_mobility_list_from_file(ue, episode):
    mobility_file_header = './mobility_200/cityhall_mobility ('
    mobility_file_footer = ').txt'
    mobility_list = list()

    mobility_file = open(mobility_file_header + str(ue + 1) + mobility_file_footer, mode='rt', encoding='utf-8')
    mobilities = mobility_file.read().split('\n')
    for index in range(episode):
        locations = mobilities[index].split(' ')

        mobility_list.append(locations)

    mobility_file.close()
    return mobility_list
