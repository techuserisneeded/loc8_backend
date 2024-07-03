def calculate_distance_to_center(distance_to_center, weightings):
    return ((100 - distance_to_center)*weightings)/100

def calculate_average_areas(average_areas, weightings):
    return (average_areas*weightings)/100

def calculate_average_speed(speed, weightings):
    return ((120-speed)*weightings)/120

def calculate_focal_vision_duration(focal_vision_duration, weightings):
    return (focal_vision_duration*weightings)/60 

def calculate_near_p_duration(near_p_duration, weightings):
    return (near_p_duration*weightings)/60

def calculate_mid_p_duration(mid_p_duration, weightings):
    return (mid_p_duration*weightings)/60

def calculate_far_p_duration(far_p_duration, weightings):
    return (far_p_duration*weightings)/60

def calculate_saliency(total):
    #return total / 100
    return total

def calculate_net_saliency(saliency_front, weight_front, saliency_rear, weight_rear):
    return ((saliency_front*weight_front) + (saliency_rear * weight_rear)) /100

def calculate_efficiency(saliency, rental_per_month):
    if rental_per_month == 0:
        return 0
    else:
       return (saliency * 100000/rental_per_month)