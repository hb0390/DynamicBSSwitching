from simulation.initialize import *
from simulation.algorithm import *
from q_learning.q_learning_agent import *

#Sleep mode strategies for dense small cell 5G networks
def compared_algorithm_1(episodes, transmission_list, num_of_ue, iteration):
    bbu, ue_list = initialize_with_single_cell('c1', num_of_ue, episodes)

    debug_txt = './debug/c1_debug_'
    txt = '.txt'
    debug = open(debug_txt + str(num_of_ue) + txt, 'w')

    result_text = './result/c1_algorithm_' + str(episodes) + '.txt'
    simulation_result = open(result_text, 'w')

    print('comp1 start....')
    c1_list = ' '
    average_ue_capacity = 0
    ave_battery_consumption = 0
    ave_outage_probability = 0
    avg_sinr= 0
    avg_system_capacity= 0
    avg_system_efficiency = 0

    ###############simulation params###################

    min_power = 3
    max_target = 25
    min_target = -5
    target_sinr = 0
    ##################################################


    for episode in range(episodes):
        print("c1 : episode",episode, " >>>")

        if episode % 30 == 0:
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
            max_sleep= bbu.max_sleep_rrh
            for bs in bbu.get_rrh_list():

                # 내 pow(avg sinr,  1/servingue) - (1)
                if len(bs.get_ue_list()) is 0:
                    my_load = 0
                else:
                    my_load = pow(bs.get_avg_sinr() ,1/len(bs.get_ue_list()))

                # closest neighbor의 pow(avg sinr, 1/servingue) - (2)
                close_rrh = find_close_rrh(bs, bs.neighbor_rrh_list)
                if len(close_rrh.get_ue_list()) is 0:
                    neighbor_load = 0
                else:
                    neighbor_load = pow(close_rrh.get_avg_sinr(),1 / len(close_rrh.get_ue_list()))

                # (2) 가 더 크면 sleep

                if neighbor_load > my_load and sleep_num < max_sleep:
                    bs.sleep()
                    sleep_num += 1

                    if sleep_num >= max_sleep:
                        break

        cellular_list = make_cellular_list(ue_list)
        ua(cellular_list, ue_list, bbu, bbu.get_rrh_list())

        outage_ue_num = 0
        for ue in ue_list:
            if ue.get_sinr() < sinr_constraint:
                outage_ue_num += 1

        outage_ue_num /= num_of_ue
        ue_capacity, average_sinr, sum_battery_consumption, system_efficiency,system_capacity, num_cellular = get_performance(
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
            avg_system_capacity += system_capacity
            avg_system_efficiency += system_efficiency

    average_ue_capacity = average_ue_capacity / (episodes - 400)
    ave_battery_consumption = ave_battery_consumption / (episodes - 400)
    ave_outage_probability = ave_outage_probability / (episodes - 400)
    avg_sinr = avg_sinr / (episodes - 400)
    avg_system_capacity /= (episodes - 400)
    avg_system_efficiency /= (episodes - 400)

    debug.close()
    simulation_result.close()
    result = [c1_list, avg_sinr, average_ue_capacity, ave_outage_probability, avg_system_capacity, avg_system_efficiency]

    print('...c1_end')
    return result
