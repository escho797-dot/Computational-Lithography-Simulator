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
    left, right = calculate_edges(resist, row)
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
    
def calculate_signed_error(target, resist):
    """
    +1 : target에는 있는데 출력이 안 된 상태 
     0 : Correct
    -1 : target에 없는데 출력된 상태
    """

    target = target.astype(np.int8)
    resist = resist.astype(np.int8)

    signed_error = target - resist
    return signed_error

#    Calculate Edge Placement Error (EPE).
def calculate_epe(target, resist):
    target_left, target_right = calculate_edges(target)
    resist_left, resist_right = calculate_edges(resist)

    if None in (
        target_left,
        target_right,
        resist_left,
        resist_right,
        ):
        return None, None

    left_epe = resist_left - target_left
    right_epe = resist_right - target_right
    return left_epe, right_epe

#Check whether the printed pattern is resolved.
def check_resolution(resist):
    left, right = calculate_edges(resist)
    if left is None or right is None:
        return "Not Resolved"
    return "Resolved"