from simulation.initialize import *
from q_learning.q_learning_agent import *
from calculation.calculator_power import *
from simulation.mobility import move
from h_cran.RRH_switching import *
from h_cran.RRH_clustering import *

##################CODE###################


def my_algorithm(episodes, transmission_list, num_of_ue, iteration):
    bbu, ue_list = initialize_with_single_cell('my', num_of_ue, episodes)

    debug_txt = './debug/my_debug_'
    txt = '.txt'
    debug = open(debug_txt + str(num_of_ue) + txt, 'w')

    result_text = './result/my_algorithm_' + str(episodes) + '.txt'

    epoch_text = open('./performance/epoch_my_' + str(num_of_ue) + txt, 'w')

    simulation_result = open(result_text, 'w')
    print('my start...')

    my_list = ' '
    average_ue_capacity = 0
    ave_battery_consumption = 0
    ave_outage_probability = 0
    avg_sinr_for_performance = 0
    avg_system_efficiency = 0
    avg_system_capacity = 0

    epoch_ue_capacity = 0
    epoch_energy_consumption = 0
    epoch_battery_consumption = 0
    epoch_outage_probability = 0

    episode_avg_outage = 0

    # move(ue_list, 900)

    for episode in range(episodes):
        print("my : episode",episode, " >>>")
        # tx, rx 요청
        #transmission_string = do_communication(ue_list, bbu.get_rrh_list(), bbu,
        #                                       transmission_list[episode * num_of_ue:(episode + 1) * num_of_ue + 1],
        #                                       num_of_ue)

        outage = 0

        for rrh in bbu.get_rrh_list():
            avg_sinr = 0
            size = 0
            for ue in ue_list:
                if ue.get_rrh_pair() == rrh.get_key():
                    # print(ue.get_sinr())
                    avg_sinr += ue.get_sinr()
                    size += 1

                    if ue.get_sinr() < sinr_constraint:
                        outage += 1
            if size == 0:
                outage = 0
            else:
                outage /= size

            if size == 0:
                avg_sinr = 0
            else:
                avg_sinr /= size

            rrh.set_avg_sinr(avg_sinr)

        if episode % 10 == 0:
            bbu.old_states = bbu.env.get_state(bbu, ue_list)
            bbu_action = bbu.agent.get_action(bbu.old_states, iteration)
            bbu.set_n_group_rrh(bbu_action[0])
            bbu.set_n_sleep_rrh(bbu_action[1])

            for rrh in bbu.get_rrh_list():
                if rrh.get_state() :
                    rrh_states = rrh.env.get_state(rrh)
                    rrh.old_states = rrh_states
                    #print("rrh_state : ", rrh_states)
                    rrh_action = rrh.agent.get_action(rrh_states, iteration)
                    rrh.action = rrh_action


            RRH_clustering(bbu, bbu.get_rrh_list())

            sleep_mechanism(bbu, bbu.get_rrh_list())

        cellular_list = make_cellular_list(ue_list)
        ua(cellular_list, ue_list, bbu, bbu.get_rrh_list())


        sinr_for_minimum_sinr = 0
        outage_ue_num = 0

        for ue in ue_list:
            # 행동을 취한 후 다음 상태, 보상을 받아옴
            sinr_for_minimum_sinr += ue.get_sinr()
            if ue.get_sinr() < sinr_constraint:
                outage_ue_num += 1

        outage_ue_num /= num_of_ue
        episode_avg_outage += outage_ue_num
        if episode % 10 == 0:
            # time interval T 마다 rrh들이 각 interval의 평균 SINR, outage probability 가지고 min SINR 설정

            episode_avg_outage /= 10

            for rrh in bbu.get_rrh_list():
                if rrh.get_state() :
                    next_state, rrh_reward = rrh.env.get_next_state(rrh, ue_list)
                    # <s,a,r,s'>로 큐함수를 업데이트

                    rrh.agent.learn(rrh.old_states, rrh.action, rrh_reward, next_state)
                    # print(episode, " >>")


            next_state, bbu_reward = bbu.env.get_next_state(episode_avg_outage, bbu, ue_list)
            # <s,a,r,s'>로 큐함수를 업데이트
            bbu.agent.learn(bbu.old_states, bbu.get_n_sleep_rrh(), bbu_reward, next_state)

            episode_avg_outage = 0

        ue_capacity, average_sinr, sum_battery_consumption, system_efficiency, system_capacity, num_cellular = get_performance(
            ue_list, bbu, num_of_ue)
        #print('num_cellular',num_cellular, 'num_of_active :',bbu.get_num_of_active_rrh(),'|| ue_capacity : ', ue_capacity, 'sinr : ', average_sinr)

        move(ue_list, episode)


        # debug string 만드는 부분
        ue_sinr_string = str(episode) + ' ' + str(ue_capacity) + ' ' + str(num_cellular) + ' ' + str(
            num_of_ue - num_cellular) + ' '
        for ue in ue_list:
            ue_sinr_string += str(ue.get_sinr()) + ' '

        ue_sinr_string += '\n'

        # debug 작성
        debug.write(ue_sinr_string)

        if episode >= 400:
            system_string = str(episode) + ' ' + str(average_sinr) + '\n'

            simulation_result.write(system_string)
            average_ue_capacity += ue_capacity
            ave_battery_consumption += sum_battery_consumption
            ave_outage_probability += outage_ue_num
            avg_sinr_for_performance += average_sinr
            avg_system_efficiency += system_efficiency
            avg_system_capacity += system_capacity
            #print(average_sinr)

        # elif episode < 100:
        #    bbu.set_sinr_contraint(ue_list)

    average_ue_capacity /= (episodes - 400)
    ave_battery_consumption /= (episodes - 400)
    ave_outage_probability /= (episodes - 400)
    avg_sinr_for_performance /= (episodes - 400)
    avg_system_efficiency /= (episodes - 400)
    avg_system_capacity /= (episodes - 400)

    # print('[', episodes, ']', ave_count_for_recommendation)
    debug.close()
    simulation_result.close()
    epoch_text.close()
    #print(avg_sinr_for_performance)

    # print("!!!!!!!!!!!!!!!ave_count_for_recommendation : ", ave_count_for_recommendation)
    result = [my_list, avg_sinr_for_performance, average_ue_capacity, ave_outage_probability, avg_system_capacity,avg_system_efficiency ]

    print('...my_end')
    return result


def get_performance(ue_list, bbu, num_of_ue):
    sum_battery_consumption = 0
    average_d2d_efficiency = 0
    average_ue_capacity = 0
    average_sinr = 0
    num_cellular = 0
    # avr_battery_cycle = 0

    for ue in ue_list:
        #print("[",ue.get_key(), "]->",calculate_ue_capacity(ue.get_sinr()))

        average_sinr += ue.get_sinr()
        battery = ue.get_battery()

        ue_capa = calculate_ue_capacity(ue.get_sinr())
        if ue.get_mode() == cellular_mode:
            num_cellular += 1
            battery_comsumption = calc_power_tx_cellular(dbmToWatt(ue.get_power()))
            # print('cellular : ',battery_comsumption)
        else:
            battery_comsumption = calc_power_tx_d2d(dbmToWatt(ue.get_power()))
            # print('d2d : ', battery_comsumption)

        sum_battery_consumption += battery_comsumption
        average_ue_capacity += ue_capa

    sum_battery_consumption = sum_battery_consumption / (num_of_ue)

    average_d2d_efficiency = average_d2d_efficiency / (num_of_ue)
    average_sinr = average_sinr / num_of_ue
    average_ue_capacity = (average_ue_capacity / num_of_ue) / 100

    # print('capacity : ', calculate_system_capacity(bbu), end='/')
    # print('sm_battery : ', sum_battery_consumption)

    average_d2d_efficiency = sum_battery_consumption

    available_rb = 0

    for key, values in bbu.get_using_RB_list().items():
        # print(values)
        for value in values:
            if not isinstance(value, int):  # d2dlink key가 int기 때문에 int가 아닌경우는 ue 객체인 경우
                available_rb += 1

    # print((bbu_capacity / system_energy_consumption),' >> ', 'bbu_capacity : ', bbu_capacity, 'energy_consumption : ', system_energy_consumption )
    # system_energy_cunsumption = (bbu_capacity / system_energy_consumption) * 10
    # print('bbu_capacity : ', bbu_capacity, ' system_energy_consumption : ', system_energy_consumption,
    #      'min-sinr : ', bbu.get_minimum_sinr(),',sinr-contriant : ', bbu.get_sinr_constraint())

    system_capacity = calculate_system_capacity(bbu, ue_list)
    system_energy = calculate_system_energy(ue_list, bbu)
    system_efficiency = system_capacity / system_energy
    print(bbu.get_num_of_active_rrh(),">>",system_capacity,"/",system_energy)
    return average_ue_capacity, average_sinr, sum_battery_consumption,  system_efficiency, system_capacity, num_cellular
