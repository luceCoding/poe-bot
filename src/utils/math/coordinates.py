import math

def calc_coords(start_pt, distance, radians): #assumes x,y is (0,0)
    x, y = start_pt
    return (int(x + distance*math.cos(radians)), int(y + distance*math.sin(radians)))

def calc_angle(source, target):
    sx, sy = source
    tx, ty = target
    return math.atan2(ty-sy, tx-sx)

def calc_distance(source, target):
    sx, sy = source
    tx, ty = target
    return abs(math.hypot(tx - sx, ty - sy))

def get_centroid(positions):
    return positions.mean(axis=0)

def get_midpoint(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return int((x1 + x2)/2), int((y1 + y2)/2)

def inverse_pts_on_pivot(pivot, pt):
    pivotx, pivoty = pivot
    ptx, pty = pt
    x = pivotx - ptx
    y = pivoty - pty
    return (pivotx + x), (pivoty + y)

def degrees_to_radians(degrees):
    return math.radians(degrees)