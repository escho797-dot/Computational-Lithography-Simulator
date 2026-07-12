import numpy as np

def calculate_difference(target, resist):
    """
    Target Pattern과 Resist Pattern을 비교하여
    Difference Map을 생성한다.
    """
    difference = np.abs(target - resist)
    return difference

def calculate_error_metrics(target, difference):
    """
    Difference Map으로부터 Error Metric 계산
    """
    error_pixels = np.sum(difference)
    total_pattern_pixels = np.sum(target)
    error_rate = error_pixels / total_pattern_pixels
    return error_pixels, error_rate  

def calculate_cd(resist, row=256): 
    left, right = calculate_edge(resist, row=256)
    if left is None:
        return 0
    return right - left + 1

def calculate_edges(resist, row=256):
    row_data = resist[row]
    indices = np.where(row_data == 1)[0]
    if len(indices) == 0:
        return None, None
    else:  
        return indices[0], indices[-1] #width, left egde, right edge