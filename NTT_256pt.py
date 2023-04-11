import numpy as np

# Function to perform (base^power) mod M
def modExponent(base, power, M):
    result = 1
    for i in range(0, power):
        result = (result * base) % M
    return result

# Function to perform bit reversal operation   
def bitReverse(num, N):
    rev_num = 0
    for i in range(0, N):
        if (num >> i) & 1:
            rev_num |= 1 << (N - 1 - i)
    return rev_num

# Function to generate Twiddle factors for DIF NTT
def gen_tf(wn, N, M):
    tf = []
    for i in range(N//2):
        tf.append(1)
        for j in range(0, bitReverse(i, int(np.log2(N//2)))):
            tf[i] = (tf[i] * wn) % M
    tf = orderReverse(tf, int(np.log2(N//2)))
    return tf

# Function to compute N-point DIF NTT
def dif_ntt(x, wl, M, N):
    ns = 1
    y = [0]*N
    for k in range(int(np.log2(N))):
        for j in range(ns):
            for i in range(N//(2*ns)):
                y[i + j*N//ns] = (x[i + j*N//ns] + x[i + N//(2*ns) + j*N//ns]) % M
                y[i + N//(2*ns) + j*N//ns] = (((x[i + j*N//ns] - x[i + N//(2*ns) + j*N//ns]) % M) * wl[(ns * i) % (N//2)]) % M
            x = y.copy()
        ns = ns*2
    yf = [0]*N
    for i in range(N):
        yf[i] = y[bitReverse(i,int(np.log2(N)))]
    return yf

# Input vector
x = [7614, 5147, 6806, 5503, 3750, 5037, 6683, 6413, 5928, 5539, 2072, 568,
    6380, 4622, 5550, 4861, 5394, 6289, 4969, 3453, 1607, 114,  1905, 2866,
    4444, 4926, 1883, 1965, 3796, 6324, 4687, 1913, 5969, 4412, 4313, 1289,
    7576, 6377, 5587, 6596, 4361, 4661, 3801, 4889, 6615, 4434, 1878, 3629,
    7063, 1558, 2234, 5887, 472,  6974, 3063, 4583, 845,  478,  7134, 789,
    2517, 1590, 1658, 3561, 2813, 7544, 7310, 5774, 916,  7205, 6138, 6568,
    6136, 5427, 3933, 359,  2222, 5585, 5315, 126,  5407, 7619, 3191, 1533,
    4843, 4083, 1034, 1509, 7089, 7591, 5536, 589,  1008, 3054, 5440, 5958,
    3857, 5713, 5093, 4133, 4957, 862,  4067, 3807, 2984, 6057, 3962, 6474,
    3426, 2790, 4539, 6434, 1157, 295,  4980, 6811, 6982, 6888, 5246, 4824,
    6772, 440,  712,  4887, 4963, 1187, 4371, 487,  5399, 1516, 778,  1999,
    2182, 2875, 3180, 7435, 4403, 1130, 6005, 2591, 2021, 1089, 2550, 1118,
    2237, 3535, 176,  397,  1379, 2120, 1237, 7208, 3589, 5668, 4404, 2843,
    272,  4583, 5092, 1696, 2280, 4284, 6562, 262,  390,  3209, 6979, 3873,
    4601, 4234, 6968, 1950, 5885, 2930, 2837, 7204, 5489, 3052, 4523, 1328,
    604,  262,  117,  3760, 7518, 7474, 6692, 2305, 2942, 3185, 2323, 4198,
    1889, 4697, 4289, 3387, 2475, 3757, 4771, 4392, 5306, 4471, 3052, 7609,
    1898, 6553, 2264, 2559, 6608, 2401, 6275, 6745, 790,  2641, 608,  2879,
    1717, 6404, 4287, 109,  6619, 6890, 3382, 2394, 3812, 5672, 458,  2916,
    5323, 619,  4881, 7048, 7285, 4475, 5161, 1174, 7469, 6205, 3671, 7626,
    6618, 3976, 2498, 3646, 3664, 3823, 643,  2771, 6419, 2474, 1358, 3415,
    4409, 5133, 7257, 1109]

# N is length of input, output and size of NTT
N = 256

# M is operating modulus
M = 7681

# wn is primitve Nth root of unity
wn = 2028


wl = gen_tf(wn, N, M)
y = dif_ntt(x, wl, M, N)

#print("Inputs:", x)
#print("Twiddle Factors:", wl)
#print("Outputs:", y)
print(N, "- point NTT for the given input under mod", M, "is:")
print(y)

