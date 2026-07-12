import numpy as np
import matplotlib.pyplot as plt

#생성
def create_mask():
    mask = np.zeros((512,512))
    #mask[:,252:260] = 1
    mask[:,248:262] = 1
    return mask

#계산만 할 때는 visualize=false 로 변경
def simulate_lithography(mask, visualize=False):
    # FFT
    mask_fft = np.fft.fft2(mask)

    # 가운데로 이동
    mask_fft_shift = np.fft.fftshift(mask_fft)

    # 보기 쉽게 log scale
    fft_image = np.log(np.abs(mask_fft_shift)+1)

    # 출력
    if visualize: 
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

    cutoff = 40

    OTF = (radius < cutoff).astype(float)

    if visualize: 
        plt.figure(figsize=(5,5))
        plt.imshow(OTF, cmap="gray")
        plt.title("OTF")
        plt.show()

    # ---------------------
    # Lens 통과
    # ---------------------

    filtered_fft = mask_fft_shift * OTF

    filtered_image = np.log(np.abs(filtered_fft)+1)

    if visualize: 
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
    
    if visualize:   
        plt.figure(figsize=(5,5))
        plt.imshow(intensity, cmap="hot")
        plt.title("Aerial Image")
        plt.colorbar()
        plt.axis("off")
        plt.show()

    if visualize: 
        print("min =", intensity.min())
        print("max =", intensity.max())

    # ---------------------
    # Resist Pattern
    # ---------------------

    threshold = 0.5

    resist = (intensity > threshold).astype(float)

    if visualize: 
        #print("Center line intensity:") 
        #print(intensity[256, 200:312])

        plt.figure(figsize=(5,5))
        plt.imshow(resist, cmap="gray")
        plt.title("Resist Pattern")
        plt.axis("off")
        plt.show()

    return mask, intensity, resist

# 이 파일을 직접 실행할 때만
if __name__ == "__main__":
    mask = create_mask()
    mask, intensity, resist = simulate_lithography(mask)