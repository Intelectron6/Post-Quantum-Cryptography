import numpy as np

# Function to perform bit-reversal (duh...)
def bitReverse(num, logn):
    rev_num = 0
    for i in range(logn):
        if (num >> i) & 1:
            rev_num |= 1 << (logn - 1 - i)
    return rev_num

# Function to generate twiddle factors (for both forward and inverse NTT)
def gen_tf(psin, inv_psin, n, q):
    positions = [bitReverse(x, int(np.log2(n))) for x in range(n)]
    tmp1, tmp2 = [], []
    psis, inv_psis = [], []
    psi = 1
    inv_psi = 1
    for x in range(n):
        tmp1.append(psi)
        tmp2.append(inv_psi)
        psi = psi * psin % q
        inv_psi = inv_psi * inv_psin % q
    for x in range(n):
        val = tmp1[positions[x]]
        inv_val = tmp2[positions[x]]
        psis.append(val)
        inv_psis.append(inv_val)
    return psis, inv_psis

# Function to generate scaling factors for point wise multiplication
def gen_pwmf(psin, n, q):
    pwmf = []
    for i in range(n):
        val = (psin**(2*bitReverse(i, int(np.log2(n))) + 1))%q
        pwmf.append(val)
    return pwmf

# Forward NTT using Cooley-Tukey (TC) algorithm
def ct_ntt(a, psis, q, n):
    t = n
    m = 1
    while m < n:
        t = t // 2
        for i in range(m):
            j1 = 2 * i * t
            j2 = j1 + t - 1
            S = psis[m + i]
            for j in range(j1, j2 + 1):
                U = a[j]
                V = a[j + t] * S
                a[j] = (U + V) % q
                a[j + t] = (U - V) % q
        m = 2 * m
    return a
  
# Inverse NTT using Gentleman-Sande (GS) algorithm
def gs_intt(a, inv_psis, q, n, inv_n):
    t = 1
    m = n
    while m > 1:
        j1 = 0
        h = m // 2
        for i in range(h):
            j2 = j1 + t - 1
            S = inv_psis[h + i]
            for j in range(j1, j2 + 1):
                U = a[j]
                V = a[j + t]
                a[j] = (U + V) % q
                a[j + t] = (U - V) * S % q
            j1 = j1 + 2 * t
        t = 2 * t
        m = m // 2
    for i in range(n):
        a[i] = a[i] * inv_n % q
    return a

# Function to compute 256 point NTT by splitting into even and odd terms and computing 128 point NTT for each 
def ntt_256(x, psis, q, n):
    xe, xo = [], []
    for i in range(n2):
        if i%2 == 0:
            xe.append(x[i])
        else:
            xo.append(x[i])
    ye = ct_ntt(xe, psis, q, n)
    yo = ct_ntt(xo, psis, q, n)
    return ye, yo

# Function to compute 256 point Inverse NTT by combining 128 point Inverse NTT of even and odd terms
def intt_256(ye, yo, inv_psis, q, n, inv_n):
    ze = gs_intt(ye, inv_psis, q, n, inv_n)
    zo = gs_intt(yo, inv_psis, q, n, inv_n)
    z = []
    for i in range(n):
        z.append(ze[i])
        z.append(zo[i])
    return z

# Function to perform point-wise multipication
def point_wise_mult(y1e, y1o, y2e, y2o, pwmf):
    y3e, y3o = [], []
    for i in range(n):
        y3e.append(((y1e[i] * y2e[i]) % q + (((y1o[i] * y2o[i]) % q) * pwmf[i]) % q) % q)
        y3o.append(((y1e[i] * y2o[i]) % q + (y1o[i] * y2e[i]) % q) % q)
    return y3e, y3o
