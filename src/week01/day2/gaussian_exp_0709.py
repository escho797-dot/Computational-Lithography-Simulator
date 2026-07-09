import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


# ---------------------
# Mask 생성
# ---------------------

N = 512

mask = np.zeros((N, N))

# Line pattern
mask[:,252:260] = 1


plt.figure(figsize=(5,5))
plt.imshow(mask, cmap="gray")
plt.title("Mask")
plt.axis("off")
plt.show()


# ---------------------
# Gaussian Exposure
# ---------------------

for sigma in [1, 5, 15]:

    aerial = gaussian_filter(mask, sigma=sigma)

    plt.figure(figsize=(5,5))
    plt.imshow(aerial, cmap="hot")
    plt.title(f"Aerial Image sigma={sigma}")
    plt.colorbar()
    plt.axis("off")
    plt.show()