def ease_out_bezier(fraction):
    return 1 - (1 - fraction) ** 3

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))
