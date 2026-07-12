import matplotlib.pyplot as plt
from lithography import create_mask
from lithography import simulate_lithography
import opc
'''
from opc import (
    calculate_difference,
    calculate_error_metrics,
    calculate_cd,
    calculate_edges
)'''


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

target = create_mask()
mask = create_mask()

mask, intensity, resist = simulate_lithography(mask)
difference = calculate_difference(target, resist)

show_difference(target, resist, difference)

#에러
error_pixels, error_rate = calculate_error_metrics(target, difference)

print(f"Error Pixels : {error_pixels}")
print(f"Error Rate   : {error_rate:.2%}")

#edge & cd
left, right = calculate_edges(resist)
print(f"Left Edge  : {left}")
print(f"Right Edge : {right}")

cd = calculate_cd(resist)
print(f"CD Width   : {cd} pixels")