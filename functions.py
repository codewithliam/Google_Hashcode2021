path = "./files2"
filesIn = ["/a", "/b", "/c", "/d", "/e"]

# Which file from "filesIn" to load
fileInNrb = 0

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

#Streets {'rue-de-londres': {'init_intersection': '2', 'end_intersection': '0', 'L_time_to_cross': '1'}, 
#           'rue-d-amsterdam': {'init_intersection': '0', 'end_intersection': '1', 'L_time_to_cross': '1'}, 
#           'rue-d-athenes': {'init_intersection': '3', 'end_intersection': '1', 'L_time_to_cross': '1'}, 
            #'rue-de-rome': {'init_intersection': '2', 'end_intersection': '3', 'L_time_to_cross': '2'}, 
            #'rue-de-moscou': {'init_intersection': '1', 'end_intersection': '2', 'L_time_to_cross': '3'}} 
            
#Cars {'car_0': {'nbr_streets': '4', 'names': ['rue-de-londres', 'rue-d-amsterdam', 'rue-de-moscou', 'rue-de-rome']}, 
# 'car_1': {'nbr_streets': '3', 'names': ['rue-d-athenes', 'rue-de-moscou', 'rue-de-londres']}}

resultOut = [["1"], ["2"]]


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

def get_current_cars_in_street(cars_dict, street):
    #Returns car_list, a list of all cars currently in queue in given street (no order yet)
    car_list = []
    for i in range(len(cars_dict)): 
        car = 'car_' + str(i)
        if street in cars_dict[car]['names']: 
            if cars_dict[car]['names'][0] == street and cars_dict[car]['L_time_to_cross'][0]==0: 
                car_list.append[car]
    return car_list




def cars_in_queue_for_street(intersection_dict):
    for i in range(len(intersection_dict)):
        for street in intersection_dict['street']: 


