import ntt
import numpy as np
import math

# Kyber Parameters
n = 256    # number of points is always 256
q = 7681   # modulus is 7681 for Kyber v1
k = 2      # k can be 2 or 3 or 4, but only 2 is supported for now

# Constants derived from the parameters
wn = 219
inv_wn = 1438
inv_n = 7651        
psin = 1656
inv_psin = 218

# Generating scaling factors and twiddle factors
w1 = ntt.gen_tf(wn, n, q)
s1 = ntt.gen_sf(psin, n, q)
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
		x1d.append((x1[i]*s1[i])%q)
		x2d.append((x2[i]*s1[i])%q)

	# Forward NTT
	y1 = ntt.dif_ntt(x1d, w1, q, n)
	y2 = ntt.dif_ntt(x2d, w1, q, n)

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
	a = np.random.randint(q, size=(k,k,n))
	s = np.random.randint(0, 8, size=(k,n))
	e = np.random.randint(0, 8, size=(k,n))
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
	r = np.random.randint(0, 8, size=(k,n))
	e1 = np.random.randint(0, 8, size=(k,n))
	e2 = np.random.randint(0, 8, size=(n,))
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
