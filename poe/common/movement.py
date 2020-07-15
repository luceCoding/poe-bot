from utils.math import coordinates as coord

def calc_mini_movement(masked_bgr_wall_minimap, start_pt, end_pt):
    distance = abs(coord.calc_distance(start_pt, end_pt))
    radians = coord.calc_angle(start_pt, end_pt)
    return distance, radians


# def calc_fog_movement(masked_bgr_wall_minimap, masked_bgr_fog_minimap):
#     zeros = np.zeros(3)
#     coords = np.column_stack(np.where(masked_bgr_fog_minimap != zeros))