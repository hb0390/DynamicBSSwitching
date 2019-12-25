from simulation.initialize import *
from simulation.algorithm import *
from q_learning.q_learning_agent import *


# Optimized sleep strategy based on clustering in dense heterogeneous networks
def compared_algorithm_2(episodes, transmission_list, num_of_ue, iteration):
    bbu, ue_list = initialize_with_single_cell('c2', num_of_ue, episodes)

    debug_txt = './debug/c2_debug_'
    txt = '.txt'
    debug = open(debug_txt + str(num_of_ue) + txt, 'w')

    result_text = './result/c2_algorithm_' + str(episodes) + '.txt'
    simulation_result = open(result_text, 'w')

    print('comp2 start....')
    c2_list = ' '
    average_ue_capacity = 0
    ave_battery_consumption = 0
    ave_outage_probability = 0
    avg_system_efficiency = 0
    avg_sinr = 0
    avg_system_capacity = 0

    for episode in range(episodes):
        print("c2 : episode",episode, " >>>")

        if episode % 30 == 0:
            for bs in bbu.get_rrh_list():
                interference_between_neighbors = 0

                # 모든 ue에 대해 가장 power * channel gain이 큰 값을 찾는다
                max_interference_with_bs = 0
                for serving_ue in bs.get_ue_list():
                    max_interference_with_bs = max(max_interference_with_bs,
                                                   serving_ue.power * get_rrh_channelgain(bs, serving_ue))

                # 모든 neighboring bs와 연결된 ue에 대해 가장 power*channel gain이 큰 값을 찾는다
                max_interference_with_neighbor = 0
                for neighbor in bs.neighbor_rrh_list:
                    for serving_ue in neighbor.get_ue_list():
                        max_interference_with_neighbor = max(max_interference_with_neighbor,
                                                             serving_ue.power * get_rrh_channelgain(neighbor,
                                                                                                    serving_ue))
                    # 위에서 구한 값들중 큰 값을 선택한다
                    # 그값들을 합친다
                    interference_between_neighbors += max(max_interference_with_bs, max_interference_with_neighbor)

                bs.load_score = interference_between_neighbors

            maximum_interference = 0
            for bs in bbu.get_rrh_list():
                maximum_interference = max(maximum_interference, bs.load_score)

            maximum_interference = maximum_interference * 0.6

            rrh_groups = []
            group_index = 0
            for bs in bbu.get_rrh_list():
                if bs.load_score > maximum_interference:
                    if len(rrh_groups) is 0 or len(rrh_groups) <= group_index:
                        rrh_groups.append([bs])
                    else:
                        rrh_groups[group_index].append(bs)
                else:
                    group_index += 1
                    rrh_groups.append([bs])

            bbu.rrh_group = rrh_groups

            # SINR threshold보다 낮은 bs 끄기

            for bs in bbu.get_rrh_list():
                bs.activate()
                average_sinr = 0
                for serving_ue in bs.get_ue_list():
                    average_sinr += serving_ue.get_sinr()

                if len(bs.get_ue_list()) is 0:
                    average_sinr = 0
                else:
                    average_sinr /= len(bs.get_ue_list())

                bs.set_avg_sinr(average_sinr)

            sleep_num = 0
            max_num = bbu.max_sleep_rrh / 1.4
            for bs_group in bbu.rrh_group:
                for bs in bs_group:
                    if sleep_num < max_num and bs.get_avg_sinr() < sinr_constraint:
                        bs.sleep()
                        sleep_num += 1

                        if sleep_num >= max_num:
                            break
                    elif bs.get_state is False:
                        sleep_num += 1

        cellular_list = make_cellular_list(ue_list)
        ua(cellular_list, ue_list, bbu, bbu.get_rrh_list())

        outage_ue_num = 0
        for ue in ue_list:
            if ue.get_sinr() < sinr_constraint:
                outage_ue_num += 1

        outage_ue_num /= num_of_ue

        ue_capacity, average_sinr, sum_battery_consumption, system_efficiency, system_capacity, num_cellular = get_performance(
            ue_list, bbu, num_of_ue)

        move(ue_list, episode)

        # debug 작성
        ue_sinr_string = str(episode) + ' ' + str(ue_capacity) + ' ' + str(num_cellular) + ' ' + str(
            num_of_ue - num_cellular) + ' '
        for ue in ue_list:
            ue_sinr_string += str(ue.get_sinr()) + ' '
        ue_sinr_string += '\n'
        debug.write(ue_sinr_string)

        if episode >= 400:
            system_string = str(episode) + ' ' + str(ue_capacity) + ' ' + str(average_sinr / num_of_ue) + '\n'

            simulation_result.write(system_string)

            average_ue_capacity += ue_capacity
            avg_sinr += average_sinr
            ave_battery_consumption += sum_battery_consumption
            ave_outage_probability += outage_ue_num
            avg_system_efficiency += system_efficiency
            avg_system_capacity += system_capacity

    average_ue_capacity = average_ue_capacity / (episodes - 400)
    ave_outage_probability = ave_outage_probability / (episodes - 400)
    avg_sinr = avg_sinr / (episodes - 400)
    avg_system_efficiency /= (episodes - 400)
    avg_system_capacity /= (episodes - 400)

    debug.close()
    simulation_result.close()

    result = [c2_list, avg_sinr, average_ue_capacity, ave_outage_probability, avg_system_capacity,
              avg_system_efficiency]

    print('...c2_end')
    return result
