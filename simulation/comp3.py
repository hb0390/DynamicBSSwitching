from simulation.initialize import *
from q_learning.q_learning_agent import *
from calculation.calculator_power import *
from simulation.mobility import move
from h_cran.RRH_switching import *
from simulation.algorithm import *


def compared_algorithm_3(episodes, transmission_list, num_of_ue, iteration):
    result_text = './result/c3_algorithm' + str(episodes) + '.txt'
    simulation_result = open(result_text, 'w')
    debug = open('./debug/c3_debug' + str(num_of_ue) + '.txt', 'w')

    bbu, ue_list = initialize_with_single_cell('no', num_of_ue, episodes)
    no_list = ''
    average_ue_capacity = 0
    ave_battery_consumption = 0
    ave_outage_probability = 0
    ave_sinr = 0
    avg_system_efficiency = 0
    avg_system_capacity = 0

    print("c3 applied start...")

    for episode in range(episodes):
        # print('no_applied >> ', episode)
        # mode_selection 진행
        transmission = transmission_list[episode * num_of_ue:(episode + 1) * num_of_ue + 1]
        # transmission = transmission_list[900 * num_of_ue:(900 + 1) * num_of_ue + 1]

        #print("episode ", episode, '>>>')
        cellular_list = make_cellular_list(ue_list)

        ua(cellular_list, ue_list, bbu, bbu.get_rrh_list())

        ue_capacity, average_sinr, sum_battery_consumption, system_efficiency, system_capacity, num_cellular = get_performance(
            ue_list, bbu, num_of_ue)
        #print("n_active : ", bbu.get_num_of_active_rrh(), ", sinr : ", average_sinr)
        outage_ue_num = 0
        for ue in ue_list:
            if ue.get_sinr() < bbu.sinr_constraint:
                outage_ue_num += 1

        outage_ue_num /= num_of_ue

        move(ue_list, episode)

        # debug 작성
        ue_sinr_string = str(episode) + ' ' + str(ue_capacity) + ' ' + str(num_cellular) + ' ' + str(
            num_of_ue - num_cellular) + ' '
        for ue in ue_list:
            ue_sinr_string += str(ue.get_sinr()) + ' '
        ue_sinr_string += '\n'
        debug.write(ue_sinr_string)

        if episode >= 400:
            system_string = str(episode) + ' ' + str(ue_capacity) + ' ' + str(average_sinr) + '\n'
            simulation_result.write(system_string)

            average_ue_capacity += ue_capacity
            ave_battery_consumption += sum_battery_consumption
            ave_outage_probability += outage_ue_num
            ave_sinr += average_sinr
            avg_system_efficiency += system_efficiency
            avg_system_capacity += system_capacity



    average_ue_capacity = average_ue_capacity / (episodes - 400)
    ave_outage_probability = ave_outage_probability / (episodes - 400)
    ave_sinr = ave_sinr / (episodes - 400)
    avg_system_efficiency /= (episodes - 400)
    avg_system_capacity /= (episodes - 400)

    debug.close()
    simulation_result.close()

    result = [no_list, ave_sinr, average_ue_capacity, ave_outage_probability, avg_system_capacity, avg_system_efficiency]

    print('...c3_end')
    return result