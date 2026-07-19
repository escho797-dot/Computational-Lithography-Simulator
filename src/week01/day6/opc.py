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

""" 원래 이걸로 했는데, 
Left Edge: 250
Right Edge: 259
target: 248-261
>> 타겟 대비 좁게 출력된 거

이 상태로 끝나서 edge 기준으로 modify 하는 함수로 수정

    Signed Error Map을 이용하여
    Mask를 한 번 수정한다.
    +1 : mask 추가
    -1 : mask 제거

def modify_mask(mask, signed_error):
    modified_mask = mask.copy()

    # Under-print
    modified_mask[signed_error == 1] = 1

    # Over-print
    modified_mask[signed_error == -1] = 0

    return modified_mask
"""


#수정본
def modify_mask(mask, left_epe, right_epe):
    """
    EPE를 이용하여 Mask Edge를 수정한다.
    """
    left, right = calculate_edges(mask)

    if left is None:
        return mask.copy()

    new_left = left - left_epe
    new_right = right - right_epe

    new_left = max(0, new_left)
    new_right = min(mask.shape[1] - 1, new_right)

    if new_left >= new_right:
        return mask.copy()

    modified_mask = np.zeros_like(mask)
    modified_mask[:, new_left:new_right+1] = 1

    return modified_mask