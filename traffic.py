# ------------------------------------------------------------------------------
#
#                       Google Hash Code 2021
#
#                             Main code
#
# By: Kevin, Liam and Eda (25-2-2021)
# ------------------------------------------------------------------------------
# Import libraries
# ------------------------------------------------------------------------------
# import numpy as np
# import random
import math

# ------------------------------------------------------------------------------
# Kevin function library
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Liam function library <3 <3 <3
# ------------------------------------------------------------------------------


def update_cars_dict_with_time_per_street(cars_dict):

    car_duration = []
    for i in range(len(cars_dict)):
        car = 'car_' + str(i)
        counter = 0
        for name in (cars_dict[car]['names']):
            car_duration.append(streets_dict[name]['L_time_to_cross'])
        car_duration[0] = 0
        cars_dict[car]['time_to_cross'] = car_duration
        car_duration = []
    return cars_dict

def get_amount_of_starting_cars():
    street_list = []
    for i in range(len(cars_dict)):
        car = 'car_' + str(i)
        first_street = cars_dict[car]['names'][0]
        street_list.append(first_street)


    street_list.sort
    current_street = street_list[0]
    first_dict = {current_street : 1}
    first_dict[current_street] = 1
    counter = 0
    for i in range(1, len(street_list)):
        street= street_list[i]
        if current_street == street:
            first_dict[current_street] +=1
            current_street=street
        else:
            first_dict.update({street: 1})
            current_street = street
    return first_dict



def get_current_cars_in_street(cars_dict, street):
    #Returns car_list, a list of all cars currently in queue in given street (no order yet)
    car_list = []
    for i in range(len(cars_dict)):
        car = 'car_' + str(i)
        if street in cars_dict[car]['names']:
            if cars_dict[car]['names'][0] == street and cars_dict[car]['L_time_to_cross'][0]==0:
                car_list.append(car)
    return car_list


# ------------------------------------------------------------------------------
# Eda function library
# ------------------------------------------------------------------------------


def nbr_cars_to_pass(streets_dict, cars_dict):
    """
    Input: streets_dict, cars_dict
    Output: Dictionary with all street names as keys and an integer for the number of
            how many cars that will pass, ex: {'rue-de-londres': 2, 'rue-d-amsterdam': 1, 'rue-d-athenes': 1, 'rue-de-rome': 1, 'rue-de-moscou': 2}
    """
    dict_nbr_cars_to_pass = {key: 0 for key in streets_dict.keys()}
    for car in cars_dict.keys():
        route = cars_dict[car]['names']
        for name in route:
            dict_nbr_cars_to_pass[name] += 1
    return dict_nbr_cars_to_pass



def cars_on_street_init(street):
    nbr_cars_on_start_streets = {street : 0 for street in streets_dict.keys()}
    for car in cars_dict:
        nbr_cars_on_start_streets[cars_dict[car]['names'][0]] += 1
    return nbr_cars_on_start_streets[street]

# ------------------------------------------------------------------------------
# Input data from file
# ------------------------------------------------------------------------------
path = "/home/kevin/Desktop/Python/GHC_2021"
filesIn = ["/a", "/b", "/c", "/d", "/e", "/f"]

# Which file from "filesIn" to load
fileInNrb = 3

# Load input data in to list "dataIn"
with open(path+filesIn[fileInNrb]+".txt", "r") as file:
    # List structure
    dataIn = [line.strip().split() for line in file]
file.close()

# Sort into variables, dicts
Duration, nbr_intersections, nbr_streets, nbr_cars, F_bonus = [int(s) for s in dataIn[0]]

streets_dict = {}
cars_dict = {}

# Fill up streets_dict
for i_street in range(1,nbr_streets+1):
    street_info = dataIn[i_street]

    # Info on each street
    street = {}
    street['init_intersection'] = street_info[0]
    street['end_intersection'] = street_info[1]
    street['L_time_to_cross'] = street_info[3]

    # Store in dict
    streets_dict[street_info[2]] = street

# Fill up cars_dict
for i_car in range(nbr_cars):
    car_info = dataIn[i_car+1+nbr_streets]
    car = {}
    car['nbr_streets'] = car_info[0]
    car['names'] = car_info[1:]

    # Store in dict
    cars_dict['car_'+str(i_car)] = car

# Duration D: 6 , nbr_intersections I: 4 , nbr_streets: 5 , nbr_cars: 2 , F_bonus: 1000

#Streets {'rue-de-londres': {'init_intersection': '2', 'end_intersection': '0', 'L_time_to_cross': '1'},
#           'rue-d-amsterdam': {'init_intersection': '0', 'end_intersection': '1', 'L_time_to_cross': '1'},
#           'rue-d-athenes': {'init_intersection': '3', 'end_intersection': '1', 'L_time_to_cross': '1'},
            #'rue-de-rome': {'init_intersection': '2', 'end_intersection': '3', 'L_time_to_cross': '2'},
            #'rue-de-moscou': {'init_intersection': '1', 'end_intersection': '2', 'L_time_to_cross': '3'}}

#Cars {'car_0': {'nbr_streets': '4', 'names': ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou', 'rue-de-rome']},
# 'car_1': {'nbr_streets': '3', 'names': ['rue-d-athenes', 'rue-de-moscou', 'rue-de-londres']}}


# Dictionary of intersections (indexed by id, containing list of streets arriving at that intersection)
intersections_dict = {key: [] for key in [str(i) for i in range(nbr_intersections)]}
for street_name in streets_dict.keys():
    intersections_dict[streets_dict[street_name]['end_intersection']] += [street_name]

#intersections_dict {'0': ['rue-de-londres'], '1': ['rue-d-amsterdam', 'rue-d-athenes'], '2': ['rue-de-moscou'], '3': ['rue-de-rome']}

def dummy_solution(intersections_dict):
    """
    For all intersections, split even time over all incoming roads

    Input: dict of intersections with their incoming streets.
    Output: dict of intersections with their schedules, each on the format [(street_name, time),...(street_name,time)]
    """
    schedule_for_all_intersections = {}
    for intersection_id in range(nbr_intersections):
        roads_in = intersections_dict[str(intersection_id)]
        intersection_schedule = [(road, int(round(Duration/len(roads_in), 0))) for road in roads_in]
        schedule_for_all_intersections[str(intersection_id)] = intersection_schedule

    return schedule_for_all_intersections


def weighted_solution(intersections_dict):
    cars_to_pass = nbr_cars_to_pass(streets_dict, cars_dict)
    schedule_for_all_intersections = {}
    for intersection_id in range(nbr_intersections):
        # Order roads_in after number of starting cars at that road
        roads_in = intersections_dict[str(intersection_id)] # modifiera


        sum_cars_into_intersection = 0
        for road in roads_in:
            sum_cars_into_intersection += cars_to_pass[road]
        if sum_cars_into_intersection == 0:
            weights = {road : 1/len(roads_in) for road in roads_in}
        else:
            weights = {road : cars_on_street_init(road)/sum_cars_into_intersection for road in roads_in}
        intersection_schedule = [(road, min(Duration, max(1,int(round(weights[road]*Duration, 0))))) for road in roads_in]

        #intersection_schedule = [(road, int(round(Duration/len(roads_in), 0))) for road in roads_in]
        schedule_for_all_intersections[str(intersection_id)] = intersection_schedule

    return schedule_for_all_intersections


# Output {'0': [('rue-de-londres', 6)], '1': [('rue-d-amsterdam', 3), ('rue-d-athenes', 3)], '2': [('rue-de-moscou', 6)], '3': [('rue-de-rome', 6)]}

def schedule_to_string(schedule_for_all_intersections):
    """
    Transforms an intersection schedule to string format, ready to read to file
    """
    resultOut = str(nbr_intersections) + "\n"
    for intersection_id in schedule_for_all_intersections.keys():
        resultOut = resultOut + intersection_id + "\n"
        list_of_streets = schedule_for_all_intersections[intersection_id]
        resultOut += str(len(list_of_streets)) + "\n"
        for street, time in list_of_streets:
            resultOut += street + " " + str(time) + "\n"
    resultOut = resultOut.strip("\n")

    return resultOut


resultOut = schedule_to_string(weighted_solution(intersections_dict))
# ------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Update cars
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Update intersection
#
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Scorer
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Output to file
# ------------------------------------------------------------------------------
fileOut = ["/A", "/B", "/C", "/D", "/E", "/F"]
#with open(path+fileOut[fileInNrb]+".out", "w") as file:
    #for i in range(int(resultOut[0][0])):
        # Join string elemetns in "resultOut[i]" into one string
        # file.write(" ".join(resultOut)+"\n")
    # Last line should not include \n
    #file.write(" ".join(resultOut[i+1]))
    #file.write(resultOut)
file = open(path+fileOut[fileInNrb]+".out", "w")
file.write(resultOut)
file.close()
