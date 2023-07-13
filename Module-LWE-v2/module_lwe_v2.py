import ntt2
import numpy as np
import math

# Kyber-v2 parameters
q = 3329
n2 = 256
n = 128
inv_n = 3303
psin = 17
inv_psin = 1175

# Get pre-computed factors
psis, inv_psis = ntt2.gen_tf(psin, inv_psin, n, q)
pwmf = ntt2.gen_pwmf(psin, n, q)


# Polynomial multiplication under mod (x^n + 1) using NTT-INTT method
def poly_mul_ntt(x1, x2):
    x1e, x1o = [], []
    x2e, x2o = [], []
    for i in range(n2):
        if i%2 == 0:
            x1e.append(x1[i])
            x2e.append(x2[i])
        else:
            x1o.append(x1[i])
            x2o.append(x2[i])

    y1e = ntt2.ct_ntt(x1e, psis, q, n)
    y1o = ntt2.ct_ntt(x1o, psis, q, n)
    y2e = ntt2.ct_ntt(x2e, psis, q, n)
    y2o = ntt2.ct_ntt(x2o, psis, q, n)

    y3e, y3o = [], []
    for i in range(n):
        y3e.append(((y1e[i] * y2e[i]) % q + (((y1o[i] * y2o[i]) % q) * pwmf[i]) % q) % q)
        y3o.append(((y1e[i] * y2o[i]) % q + (y1o[i] * y2e[i]) % q) % q)

    ze = ntt2.gs_intt(y3e, inv_psis, q, n, inv_n)
    zo = ntt2.gs_intt(y3o, inv_psis, q, n, inv_n)

    z = []
    for i in range(n):
        z.append(ze[i])
        z.append(zo[i])

    return z


# Key generation function (to be performed by server)
def key_gen():
	a = np.random.randint(q, size=(k,k,n2))
	s = np.random.randint(-2, 2, size=(k,n2))
	e = np.random.randint(-2, 2, size=(k,n2))
	b0 = (poly_mul_ntt(a[0,0], s[0]) + e[0]) % q
	b1 = (poly_mul_ntt(a[0,1], s[1]) + e[1]) % q
	b2 = (poly_mul_ntt(a[1,0], s[0]) + e[0]) % q
	b3 = (poly_mul_ntt(a[1,1], s[1]) + e[1]) % q
	b01 = (b0 + b1) % q
	b23 = (b2 + b3) % q
	b = np.array([b01, b23])
	return s, a, b

# Encryption function (to be performed by client)
def encrypt(a, b, m):
	r = np.random.randint(-2, 2, size=(k,n2))
	e1 = np.random.randint(-2, 2, size=(k,n2))
	e2 = np.random.randint(-2, 2, size=(n2,))
	u0 = (poly_mul_ntt(a[0,0], r[0]) + e1[0]) % q
	u1 = (poly_mul_ntt(a[1,0], r[1]) + e1[1]) % q
	u2 = (poly_mul_ntt(a[0,1], r[0]) + e1[0]) % q
	u3 = (poly_mul_ntt(a[1,1], r[1]) + e1[1]) % q
	u01 = (u0 + u1) % q
	u23 = (u2 + u3) % q
	u = np.array([u01, u23])
	v0 = np.array(poly_mul_ntt(b[0], r[0]))
	v1 = np.array(poly_mul_ntt(b[1], r[1]))
	v = (v0 + v1 + e2 + math.floor(q/2)*m) % q
	return u, v

# Decryption function (to be performed by server)
def decrypt(s, u, v):
        p0 = np.array(poly_mul_ntt(s[0], u[0]))
        p1 = np.array(poly_mul_ntt(s[1], u[1]))
        p = (p0 + p1) % q
        d = (v - p) % q
        return d


# Randomly generated binary message, m
m = np.random.randint(2, size=(n2,))

# Generating private key (s) and publik keys (a,b)
s, a, b = key_gen()

# Encrypting the message using public keys to provide cipher texts (u,v)
u, v = encrypt(a, b, m)

# Decrypt the cipher using private key to obtain back the message (d)
d = decrypt(s, u, v)

# Decoding the decrypted message
md = []
for i in d:
	if i > math.floor(q/4) and i < math.floor(3*q/4):
		md.append(1)
	else:
		md.append(0)
md = np.array(md)

# Comparision and printing results
print("Actual message    :\n", m)
print("Decrypted message :\n", md)

if (list(m) == list(md)):
	print("Actual message and decrypted message are the same!")
else:
	print("There is mismatch between actual message and decrypted message....")

