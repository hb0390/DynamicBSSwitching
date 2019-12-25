from simulation.algorithm import *
from h_cran.params import *
from calculation.calculation import *
from simulation.comp1 import *
from simulation.comp2 import *
from simulation.comp3 import *


def make_seed(episode, num_of_ue):
    seed_list = list()
    for s in range(episode):
        for u in range(num_of_ue):
            seed_list.append(random.randint(0, 10000))
    print(seed_list)
    return seed_list


def make_communication_for_d2d(episode, num_of_ue):
    location_file = open('location_of_ue_gaussian.txt', mode='rt', encoding='utf-8')
    ue_location = location_file.readlines()
    ue_list = dict()
    for location in range(num_of_ue):
        location = ue_location[location].split(' ')
        ue_list[location[0]] = [float(location[1]), float(location[2])]
    location_file.close()

    choice_list = list()
    for ue, locations in ue_list.items():
        random_list = find_available_d2d_list(ue, locations[0], locations[1], ue_list)
        choice_list.append(random_list)

    transmission_list = list()
    for s in range(episode):

        for choices in choice_list:
            if len(choices) != 0:
                rx = int(random.choice(choices))
            else:
                rx = random.randint(num_of_ue + 10, num_of_ue + 1000)

            transmission_list.append(rx)

    print(transmission_list)
    return transmission_list


def find_available_d2d_list(key, x, y, ue_location_list):
    random_list = list()
    for ue, locations in ue_location_list.items():
        if key != ue:
            if get_distance(x, y, locations[0], locations[1]) < min_distance_D2D:
                random_list.append(ue)
    return random_list


if __name__ == '__main__':

    # 실험 모드 선택
    mode = 'load'

    num_list = []
    num_of_ue = 20

    # 돌리고 싶은 횟수
    num_iteration = 20 + 1
    for num in range(num_iteration):
        if num != 0 or num % 2 == 0:
            num_list.append(int((num) * 20))

    print(num_list)

    episode = 1000

    iteration_num = 1

    txt = '.txt'
    sinr_txt = './performance/performance_sinr_'
    ue_capacity_txt = './performance/performance_ue_capacity_'
    system_capacity_txt = './performance/performance_system_capacity_'
    outage_probability_txt = './performance/performance_outage_probability_'
    system_efficiency_txt = './performance/performance_system_efficiency_'

    compare = 4
    for iteration in range(iteration_num):
        performance_sinr = open(sinr_txt + str(iteration) + txt, 'w')
        performance_ue_capacity = open(ue_capacity_txt + str(iteration) + txt, 'w')
        performance_outage_probability = open(outage_probability_txt + str(iteration) + txt, 'w')
        performance_system_capacity = open(system_capacity_txt + str(iteration) + txt, 'w')
        performance_system_efficiency = open(system_efficiency_txt + str(iteration) + txt, 'w')

        performance_list = list()
        performance_list.append(performance_sinr)
        performance_list.append(performance_ue_capacity)
        performance_list.append(performance_outage_probability)
        performance_list.append(performance_system_capacity)

        # 4:9 돌리기
        for num in num_list[3:8]:
            print(num / 2)
            num_of_ue = num
            transmission_list = make_communication_for_d2d(episode, num_of_ue)
            my_result = my_algorithm(episode, transmission_list, num_of_ue, iteration)
            c1_result = compared_algorithm_1(episode, transmission_list, num_of_ue, iteration)

            # my_battery_result = my_algorithm(episode, transmission_list, num_of_ue,iteration)
            c2_result = compared_algorithm_2(episode, transmission_list, num_of_ue, iteration)
            c3_result = compared_algorithm_3(episode, transmission_list, num_of_ue, iteration)

            result_list = [my_result, c1_result, c2_result, c3_result]

            sinr_string = str(int(num / 2))
            ue_string = str(int(num / 2))
            bconsumption_string = str(int(num / 2))
            system_energy_consumption_string = str(int(num / 2))
            efficiency_string = str(int(num / 2))

            for c in range(compare):
                sinr_string += ' ' + str(result_list[c][1])
                ue_string += ' ' + str(result_list[c][2])
                bconsumption_string += ' ' + str(result_list[c][3])
                system_energy_consumption_string += ' ' + str(result_list[c][4])
                efficiency_string += ' ' + str(result_list[c][5])

            performance_ue_capacity.write(ue_string + '\n')
            performance_sinr.write(sinr_string + '\n')
            performance_outage_probability.write(bconsumption_string + '\n')
            performance_system_capacity.write(system_energy_consumption_string + '\n')
            performance_system_efficiency.write(efficiency_string + '\n')

        performance_ue_capacity.close()
        performance_sinr.close()
        performance_system_capacity.close()
        performance_outage_probability.close()
        performance_system_efficiency.close()
