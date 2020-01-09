import numpy as np 
import matplotlib.pyplot as plt 
from skimage.measure import label, regionprops 
from skimage import measure
from scipy.ndimage import binary_dilation
from skimage.filters import threshold_otsu

def count_holes(symbol):
    if hasattr(symbol, "image"):    
        zero = symbol.image
    else:
        zero = symbol
    zero = ~zero
    zones = np.ones((zero.shape[0]+2,
                     zero.shape[1]+2))
    zones[1:-1, 1:-1] = zero
    z1 = label(zones)
    return np.max(z1)-1

def has_vline(symbol):
    image = symbol.image
    lines = np.sum(image, 0) // image.shape[0]
    return 1 in lines

def is_A(symbol):
    image = symbol.image
    zones = image[:].copy()
    zones[-1,:]  = 1
    holes = count_holes(zones)
    return holes == 2

def count_bays(symbol):
    zero=symbol.image
    holes = ~zero.copy()
    lb = label(holes)
    return np.max(lb)
    
    
    

def recognize(symbol):
    holes = count_holes(symbol)
    if holes == 2:
        if has_vline(symbol):
            return "B"
        else:
            return "8"
    elif holes == 1:
        if is_A(symbol):
            return "A"
        elif has_vline(symbol):
            lomme=symbol.convex_area/(symbol.image.shape[0]*symbol.image.shape[1])
            if lomme > 0.85:
                return "D"
            else:
                return "P"
        else:
            return "0"
    elif holes == 0:
        if np.all(symbol.image):
            return "-"
        elif has_vline(symbol):
            return "1"
        else:
            if count_bays(symbol) == 4:
                return "X"
            elif count_bays(symbol) == 5:
                return "W"
            else:
                arr = symbol.image
                ratio = arr.shape[0] / arr.shape[1]
                if 0.8 < ratio < 1.2:
                    return "*"
                elif 1.6 < ratio < 2.2:
                    return "/"
    return ""
def main_function_logic():
    my_image = plt.imread("symbols.png")
    gray = np.average(my_image, 2)
    gray[gray>0] = 1
    gray = gray.astype("uint8")
    my_label = label(gray)
    total = np.max(my_label)
    arr=np.zeros_like(my_label)
    symbols = regionprops(my_label)
    recon={"":0}
    for symbol in symbols:
        sym=recognize(symbol)
        if sym not in recon:
            recon[sym] = 1
        else:
            recon[sym] += 1
    print()
    print(recon)
    print()
    print("Recognizing rate: {}".format((total - recon[""]) / total))


main_function_logic()
