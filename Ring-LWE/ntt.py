import numpy as np

# Function to obtain parameters for given N
# These values are pre-computed for q = 12289
def getParams(n):
    if n == 4:
        inv_n = 9217
        wn = 1479
        psin = 8246
        inv_wn = 10810
        inv_psin = 7143
        
    elif n == 8:
        inv_n = 10753
        wn = 8246
        psin = 4134
        inv_wn = 7143
        inv_psin = 10984
        
    elif n == 16:
        wn = 4134
        psin = 5860
        inv_wn = 10984
        inv_psin = 8747
        inv_n = 11521
        
    elif n == 32:
        wn = 5860
        psin = 7311
        inv_wn = 8747
        inv_psin = 9650
        inv_n = 11905
        
    elif n == 64:
        wn = 7311
        psin = 12149
        inv_wn = 9650
        inv_psin = 790
        inv_n = 12097
        
    elif n == 128:
        wn = 12149
        psin = 8340
        inv_wn = 790
        inv_psin = 1696
        inv_n = 12193
        
    elif n == 256:
        wn = 8340
        psin = 3400
        inv_wn = 1696
        inv_psin = 2859
        inv_n = 12241
        
    elif n == 512:
        wn = 3400
        psin = 10302
        inv_wn = 2859
        inv_psin = 8974
        inv_n = 12265
        
    elif n == 1024:
        wn = 10302
        psin = 1945
        inv_wn = 8974
        inv_psin = 4050
        inv_n = 12277
        
    else:
        wn, inv_wn, psin, inv_psin, inv_n = 0,0,0,0,0
        print("Screw it...")
        
    return wn, inv_wn, psin, inv_psin, inv_n

# Function to calculate (base^power) mod q  
def modExponent(base, power, q):
    result = 1
    for i in range(0, power):
        result = (result * base) % q
    return result
 
# Function to perform bit-reversal
def bitReverse(num, n):
    rev_num = 0
    for i in range(0, n):
        if (num >> i) & 1:
            rev_num |= 1 << (n - 1 - i)
    return rev_num

# Function to perform order-reversal
def orderReverse(poly, n_bit):
    for i, coeff in enumerate(poly):
        rev_i = bitReverse(i, n_bit)
        if rev_i > i:
            poly[i] = poly[rev_i]
            poly[rev_i] = coeff
    return poly

# Function to generate scaling factors (pre-scale and post-scale to perform negative wrapped convolution)  
def gen_sf(on, n, q):
    sf = []
    for i in range(n):
        sf.append(1)
        for j in range(0, bitReverse(i, int(np.log2(n)))):
            sf[i] = (sf[i] * on) % q
    sf = orderReverse(sf, int(np.log2(n)))
    return sf
  
# Function to generate twiddle factors
def gen_tf(wn, n, q):
    tf = []
    for i in range(n//2):
        tf.append(1)
        for j in range(0, bitReverse(i, int(np.log2(n//2)))):
            tf[i] = (tf[i] * wn) % q
    tf = orderReverse(tf, int(np.log2(n//2)))
    return tf

# Function to compute N-point Forward NTT using Decimation in Frequency
def dif_ntt(x, wl, q, n):
    ns = 1
    y = [0]*n
    for k in range(int(np.log2(n))):
        for j in range(ns):
            for i in range(n//(2*ns)):
                y[i + j*n//ns] = (x[i + j*n//ns] + x[i + n//(2*ns) + j*n//ns]) % q
                y[i + n//(2*ns) + j*n//ns] = (((x[i + j*n//ns] - x[i + n//(2*ns) + j*n//ns]) % q) * wl[(ns * i) % (n//2)]) % q
            x = y.copy()
        ns = ns*2
    yf = [0]*n
    for i in range(n):
        yf[i] = y[bitReverse(i,int(np.log2(n)))]
    return yf

# Function to compute N-point Inverse NTT using Decimation in Frequency
def dif_intt(x, inv_wl, q, n, inv_n):
    y = dif_ntt(x, inv_wl, q, n)
    for i in range(n):
        y[i] = (y[i] * inv_n) % q
    return y
