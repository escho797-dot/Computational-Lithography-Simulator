import matplotlib.pyplot as plt
import numpy as np
from lithography import (
    create_mask,
    simulate_lithography
)

from opc import (
    calculate_difference,
    calculate_error_metrics,
    calculate_cd,
    calculate_edges,
    calculate_signed_error,
    calculate_epe,
    check_resolution,
    modify_mask
)

def show_difference(target, resist, difference):
    # Figure 생성
    plt.figure(figsize=(12,5))
    # Target 출력
    plt.subplot(1,3,1)
    plt.imshow(target, cmap="gray")
    plt.title("Target")
    plt.axis("off")

    # Resist 출력
    plt.subplot(1,3,2)
    plt.imshow(resist, cmap="gray")
    plt.title("Resist")
    plt.axis("off")

    # Difference 출력
    plt.subplot(1,3,3)
    plt.tight_layout()
    plt.imshow(difference, cmap="gray")
    plt.title("Difference")
    plt.axis("off")

    # show()
    plt.show()
    return

def show_signed_error(error):
    plt.figure(figsize=(6,6))
    plt.imshow(error, cmap="bwr", vmin=-1, vmax=1)
    # 파랑(-1): over-print / 하양(0): correct / 빨강(1): under-print
    plt.title("Signed Error Map")
    plt.colorbar()
    plt.axis("off")
    plt.show()

"""
def compare_images(before, after, title1, title2):

    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.imshow(before, cmap="gray")
    plt.title(title1)
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(after, cmap="gray")
    plt.title(title2)
    plt.axis("off")

    plt.tight_layout()
    plt.show()
"""

"""
def compare_resist(before, after):
    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.imshow(before, cmap="gray")
    plt.title("Before OPC")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(after, cmap="gray")
    plt.title("After OPC")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

def compare_mask(before, after):
    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.imshow(before, cmap="gray")
    plt.title("Original Mask")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(after, cmap="gray")
    plt.title("Modified Mask")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
"""
    
def show_opc_result(original_mask, modified_mask,
                    original_resist, modified_resist):

    plt.figure(figsize=(10, 8))

    # Original Mask
    plt.subplot(2,2,1)
    plt.imshow(original_mask, cmap="gray")
    plt.title("Original Mask")
    plt.axis("off")

    # Modified Mask
    plt.subplot(2,2,2)
    plt.imshow(modified_mask, cmap="gray")
    plt.title("Modified Mask")
    plt.axis("off")

    # Before OPC
    plt.subplot(2,2,3)
    plt.imshow(original_resist, cmap="gray")
    plt.title("Before OPC")
    plt.axis("off")

    # After OPC
    plt.subplot(2,2,4)
    plt.imshow(modified_resist, cmap="gray")
    plt.title("After OPC")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

target = create_mask()
original_mask = create_mask()

_, intensity, resist = simulate_lithography(original_mask)

#mask = create_mask()
#mask, intensity, resist = simulate_lithography(mask)
difference = calculate_difference(target, resist)

show_difference(target, resist, difference)

#에러
error_pixels, error_rate = calculate_error_metrics(target, difference)
print("===== Before OPC =====")
print(f"Error Pixels : {error_pixels}")
print(f"Error Rate   : {error_rate:.2%}")

#edge & cd
left, right = calculate_edges(resist)
print(f"Left Edge  : {left}")
print(f"Right Edge : {right}")

cd = calculate_cd(resist)
print(f"CD Width   : {cd} pixels")

#signed_error
signed_error = calculate_signed_error(target, resist)
show_signed_error(signed_error)

#EPE
left_epe, right_epe = calculate_epe(target, resist)
print(f"Left EPE  : {left_epe} pixels")
print(f"Right EPE : {right_epe} pixels")

resolution = check_resolution(resist)
print(f"Resolution Status : {resolution}")

modified_mask = modify_mask(original_mask, left_epe, right_epe)

# Modified Mask로 다시 Lithography 수행
_, modified_intensity, modified_resist = simulate_lithography(modified_mask)

modified_difference = calculate_difference(target, modified_resist)
modified_error_pixels, modified_error_rate = calculate_error_metrics(target, modified_difference)

print("\n===== After OPC =====")

print(f"Error Pixels : {modified_error_pixels}")
print(f"Error Rate   : {modified_error_rate:.2%}")

modified_left, modified_right = calculate_edges(modified_resist)
print(f"Left Edge  : {modified_left}")
print(f"Right Edge : {modified_right}")

modified_cd = calculate_cd(modified_resist)
print(f"CD Width   : {modified_cd} pixels")

modified_left_epe, modified_right_epe = calculate_epe(target, modified_resist)
print(f"Left EPE   : {modified_left_epe}")
print(f"Right EPE  : {modified_right_epe}")

# 비교
show_opc_result(
    original_mask,
    modified_mask,
    resist,
    modified_resist
)
"""
compare_images(
    original_mask,
    modified_mask,
    "Original Mask",
    "Modified Mask"
)

compare_images(
    resist,
    modified_resist,
    "Before OPC",
    "After OPC"
)
"""

print("\n===== OPC Summary =====")
print(f"Error Rate : {error_rate:.2%} -> {modified_error_rate:.2%}")
print(f"Left EPE   : {left_epe} -> {modified_left_epe}")
print(f"Right EPE  : {right_epe} -> {modified_right_epe}")

# 추가/비교
changed_pixels = np.abs(modified_resist - resist)

plt.figure(figsize=(5,5))
plt.imshow(changed_pixels, cmap="hot")
plt.title("Changed Pixels")
plt.colorbar()
plt.axis("off")
plt.show()