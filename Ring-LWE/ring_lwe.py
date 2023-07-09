import ntt
import numpy as np
import math
import time

q = 12289   # Prime modulus (fixed for NewHope)
n = 512     # Length of polynomials (512 or 1024 for NewHope)

# Obtaining parameters
wn, inv_wn, psin, inv_psin, inv_n = ntt.getParams(n)

# Generating scaling factors and twiddle factors
wl = ntt.gen_tf(wn, n, q)
sl = ntt.gen_sf(psin, n, q)
inv_wl = ntt.gen_tf(inv_wn, n, q)
inv_sl = ntt.gen_sf(inv_psin, n, q)

# Polynomial multiplication under mod (x^n + 1) [i.e negative wrapped convolution] using NTT-INTT method 
def poly_mul_ntt(x1, x2):
	x1 = x1[::-1]
	x2 = x2[::-1]
	
	# Pre-scaling for negative wrapped convolution
	x1d = []
	x2d = []
	for i in range(n):
		x1d.append((x1[i]*sl[i])%q)
		x2d.append((x2[i]*sl[i])%q)

	# Forward NTT
	y1 = ntt.dif_ntt(x1d, wl, q, n)
	y2 = ntt.dif_ntt(x2d, wl, q, n)

	# Point-wise multiplication
	y3 = []
	for i in range(n):
		y3.append((y1[i]*y2[i])%q)

	# Inverse NTT
	x3d = ntt.dif_intt(y3, inv_wl, q, n, inv_n)

	# Post-scaling for negative wrapped convolution
	x3 = []
	for i in range(n):
		x3.append((x3d[i]*inv_sl[i])%q)
	
	x3 = x3[::-1]
	
	return x3

# Key generation function (to be performed by server)
def key_gen():
	a = np.random.randint(q, size=(n,))
	s = np.random.randint(-5,5, size=(n,))
	e = np.random.randint(-5,5, size=(n,))
	b = (poly_mul_ntt(a, s) + e) % q
	return s, a, b

# Encryption function (to be performed by client)
def encrypt(a, b, m):
	r = np.random.randint(-5,5, size=(n,))
	e1 = np.random.randint(-5,5, size=(n,))
	e2 = np.random.randint(-5,5, size=(n,))
	u = (poly_mul_ntt(a, r) + e1) % q
	v = (poly_mul_ntt(b, r) + e2 + math.floor(q/2)*m) % q
	return u, v

# Decryption function (to be performed by server)
def decrypt(s, u, v): 
	d = (v - poly_mul_ntt(s, u)) % q
	return d
	
# Randomly generated binary message, m	
m = np.random.randint(2, size=(n,))

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
