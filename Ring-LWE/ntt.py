import numpy as np

# Function to obtain parameters for given N
# These values are pre-computed for q = 12289
def getParams(N):
    if N == 4:
        inv_N = 9217
        wn = 1479
        psin = 8246
        inv_wn = 10810
        inv_psin = 7143
        
    elif N == 8:
        inv_N = 10753
        wn = 8246
        psin = 4134
        inv_wn = 7143
        inv_psin = 10984
        
    elif N == 16:
        wn = 4134
        psin = 5860
        inv_wn = 10984
        inv_psin = 8747
        inv_N = 11521
        
    elif N == 32:
        wn = 5860
        psin = 7311
        inv_wn = 8747
        inv_psin = 9650
        inv_N = 11905
        
    elif N == 64:
        wn = 7311
        psin = 12149
        inv_wn = 9650
        inv_psin = 790
        inv_N = 12097
        
    elif N == 128:
        wn = 12149
        psin = 8340
        inv_wn = 790
        inv_psin = 1696
        inv_N = 12193
        
    elif N == 256:
        wn = 8340
        psin = 3400
        inv_wn = 1696
        inv_psin = 2859
        inv_N = 12241
        
    elif N == 512:
        wn = 3400
        psin = 10302
        inv_wn = 2859
        inv_psin = 8974
        inv_N = 12265
        
    elif N == 1024:
        wn = 10302
        psin = 1945
        inv_wn = 8974
        inv_psin = 4050
        inv_N = 12277
        
    else:
        wn, inv_wn, psin, inv_psin, inv_N = 0,0,0,0,0
        print("Screw it...")
        
    return wn, inv_wn, psin, inv_psin, inv_N

# Function to calculate (base^power) mod q  
def modExponent(base, power, q):
    result = 1
    for i in range(0, power):
        result = (result * base) % q
    return result
 
# Function to perform bit-reversal
def bitReverse(num, N):
    rev_num = 0
    for i in range(0, N):
        if (num >> i) & 1:
            rev_num |= 1 << (N - 1 - i)
    return rev_num

# Function to perform order-reversal
def orderReverse(poly, N_bit):
    for i, coeff in enumerate(poly):
        rev_i = bitReverse(i, N_bit)
        if rev_i > i:
            poly[i] = poly[rev_i]
            poly[rev_i] = coeff
    return poly

# Function to generate scaling factors (pre-scale and post-scale to perform negative wrapped convolution)  
def gen_sf(on, N, q):
    sf = []
    for i in range(N):
        sf.append(1)
        for j in range(0, bitReverse(i, int(np.log2(N)))):
            sf[i] = (sf[i] * on) % q
    sf = orderReverse(sf, int(np.log2(N)))
    return sf
  
# Function to generate twiddle factors
def gen_tf(wn, N, q):
    tf = []
    for i in range(N//2):
        tf.append(1)
        for j in range(0, bitReverse(i, int(np.log2(N//2)))):
            tf[i] = (tf[i] * wn) % q
    tf = orderReverse(tf, int(np.log2(N//2)))
    return tf

# Function to compute N-point Forward NTT using Decimation in Frequency
def dif_ntt(x, wl, q, N):
    ns = 1
    y = [0]*N
    for k in range(int(np.log2(N))):
        for j in range(ns):
            for i in range(N//(2*ns)):
                y[i + j*N//ns] = (x[i + j*N//ns] + x[i + N//(2*ns) + j*N//ns]) % q
                y[i + N//(2*ns) + j*N//ns] = (((x[i + j*N//ns] - x[i + N//(2*ns) + j*N//ns]) % q) * wl[(ns * i) % (N//2)]) % q
            x = y.copy()
        ns = ns*2
    yf = [0]*N
    for i in range(N):
        yf[i] = y[bitReverse(i,int(np.log2(N)))]
    return yf

# Function to compute N-point Inverse NTT using Decimation in Frequency
def dif_intt(x, inv_wl, q, N, inv_N):
    y = dif_ntt(x, inv_wl, q, N)
    for i in range(N):
        y[i] = (y[i] * inv_N) % q
    return y
