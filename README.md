# Post-Quantum-Cryptography
Python implementations of some popular Lattice based Post Quantum Cryptography schemes. 

1) PQC scheme based on Learning With Errors (LWE) problem [n = 128].
2) PQC scheme based on Ring Learning With Errors (R-LWE) problem [q = 12289, n = 512].
3) PQC scheme based on Module Learning With Errors (M-LWE) problem [q = 7681, n = 256, k = 2].
4) PQC scheme based on Module Learning With Errors (M-LWE) problem [q = 3329, n = 256, k = 2].
   
These codes are only to help understand the key-generation, encryption and decryption functions and the utility of Number Theoretic Transform to do fast integer polynomial multiplication. </br>
To understand NTT implementation for the 4th scheme (Module-LWE-v2) better, please refer to the following extremely well written article by Mr.Marjan Sterjev: https://www.linkedin.com/pulse/kyber-ntt-efficient-polynomial-multiplication-marjan-sterjev/ 
