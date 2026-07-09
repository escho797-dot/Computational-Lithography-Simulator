# 더 얇게

import numpy as np
import matplotlib.pyplot as plt


# Mask 생성
mask = np.zeros((512,512))

mask[:,252:260] = 1

# FFT
mask_fft = np.fft.fft2(mask)

# 가운데로 이동
mask_fft_shift = np.fft.fftshift(mask_fft)

# 보기 쉽게 log scale
fft_image = np.log(np.abs(mask_fft_shift)+1)

# 출력
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.imshow(mask,cmap="gray")
plt.title("Mask")

plt.subplot(1,2,2)
plt.imshow(fft_image,cmap="gray")
plt.title("FFT")

plt.show()

# ---------------------
# Lens (OTF)
# ---------------------

N = 512

Y, X = np.ogrid[:N, :N]

center = N // 2

radius = np.sqrt((X-center)**2 + (Y-center)**2)

cutoff = 15

OTF = (radius < cutoff).astype(float)


plt.figure(figsize=(5,5))
plt.imshow(OTF, cmap="gray")
plt.title("OTF")
plt.show()

# ---------------------
# Lens 통과
# ---------------------

filtered_fft = mask_fft_shift * OTF

filtered_image = np.log(np.abs(filtered_fft)+1)

plt.figure(figsize=(5,5))
plt.imshow(filtered_image, cmap="gray")
plt.title("Filtered FFT")
plt.axis("off")
plt.show()

# ---------------------
# IFFT (Aerial Image)
# ---------------------

aerial = np.fft.ifft2(np.fft.ifftshift(filtered_fft))

intensity = np.abs(aerial)**2

plt.figure(figsize=(5,5))
plt.imshow(intensity, cmap="hot")
plt.title("Aerial Image")
plt.colorbar()
plt.axis("off")
plt.show()

print("min =", intensity.min())
print("max =", intensity.max())

# ---------------------
# Resist Pattern
# ---------------------

threshold = 0.5

resist = (intensity > threshold).astype(float)

print(intensity[256, 200:312])

plt.figure(figsize=(5,5))
plt.imshow(resist, cmap="gray")
plt.title("Resist Pattern")
plt.axis("off")
plt.show()