import numpy as np

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
