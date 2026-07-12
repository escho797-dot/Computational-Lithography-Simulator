import matplotlib.pyplot as plt
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
    check_resolution
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

#signed_error
signed_error = calculate_signed_error(target, resist)
show_signed_error(signed_error)

#EPE
left_epe, right_epe = calculate_epe(target, resist)
print(f"Left EPE  : {left_epe} pixels")
print(f"Right EPE : {right_epe} pixels")

resolution = check_resolution(resist)
print(f"Resolution Status : {resolution}")