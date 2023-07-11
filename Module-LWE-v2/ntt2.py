import numpy as np

# Function to perform bit-reversal (duh...)
def bitReverse(num, logn):
    rev_num = 0
    for i in range(logn):
        if (num >> i) & 1:
            rev_num |= 1 << (logn - 1 - i)
    return rev_num

# Function to generate twiddle factors (for both forward and inverse NTT)
def gen_tf(psin, n, q):
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
