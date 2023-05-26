import ntt
import numpy as np
import math
import time

n = 512
q = 12289
wn, inv_wn, psin, inv_psin, inv_n = ntt.getParams(n)
w1 = ntt.gen_tf(wn, n, q)
s1 = ntt.gen_sf(psin, n, q)
inv_wl = ntt.gen_tf(inv_wn, n, q)
inv_sl = ntt.gen_sf(inv_psin, n, q)

def poly_mul_dir(a, b):
	pmod = np.array([0]*(n+1))
	pmod[0] = 1
	pmod[-1] = 1
	st = time.time()
	x = np.polymul(a, b)%q
	y = list(np.polydiv(x, pmod)[0])
	y = y[::-1]
	while True:
		if (len(y) < n):
			y.append(0)
		else:
			break
	y = y[::-1]
	et = time.time()
	print("Time for regular polymult:", (et-st)*1000, "ms")
	return y
	
def poly_mul_ntt(x1, x2):
	x1 = x1[::-1]
	x2 = x2[::-1]

	st = time.time()
	x1d = []
	x2d = []
	for i in range(n):
		x1d.append((x1[i]*s1[i])%q)
		x2d.append((x2[i]*s1[i])%q)

	y1 = ntt.dif_ntt(x1d, w1, q, n)
	y2 = ntt.dif_ntt(x2d, w1, q, n)

	y3 = []
	for i in range(n):
		y3.append((y1[i]*y2[i])%q)

	x3d = ntt.dif_intt(y3, inv_wl, q, n, inv_n)

	x3 = []
	for i in range(n):
		x3.append((x3d[i]*inv_sl[i])%q)
		
	et = time.time()
	print("Time for NTT-INTT polymult:", (et-st)*1000, "ms")
	
	x3 = x3[::-1]
	
	return x3
	
def key_gen():
	a = np.random.randint(q, size=(n,))
	s = np.random.randint(-5,5, size=(n,))
	e = np.random.randint(-5,5, size=(n,))
	#b = (poly_mul_dir(a, s) + e) % q
	b = (poly_mul_ntt(a, s) + e) % q
	return s, a, b
	
def encrypt(a, b, m):
	r = np.random.randint(-5,5, size=(n,))
	e1 = np.random.randint(-5,5, size=(n,))
	e2 = np.random.randint(-5,5, size=(n,))
	#u = (poly_mul_dir(a, r) + e1) % q
	u = (poly_mul_ntt(a, r) + e1) % q
	#v = (poly_mul_dir(b, r) + e2 + math.floor(q/2)*m) % q
	v = (poly_mul_ntt(b, r) + e2 + math.floor(q/2)*m) % q
	return u, v

def decrypt(s, u, v): 
	#d = (v - poly_mul_dir(s, u)) % q
	d = (v - poly_mul_ntt(s, u)) % q
	return d
	
m = np.random.randint(2, size=(n,))

s, a, b = key_gen()
u, v = encrypt(a, b, m)
d = decrypt(s, u, v)

md = []
for i in d:
	if i > math.floor(q/4) and i < math.floor(3*q/4):
		md.append(1)
	else:
		md.append(0)	
md = np.array(md)

print("Actual message    :\n", m)
print("Decrypted message :\n", md)
print(m == md)

