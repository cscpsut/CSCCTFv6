## **Digital Encryption League** Challenge Walkthrough

This challenge leverages RSA encryption and exploits a cryptographic vulnerability known as the **common modulus attack**. Below is a detailed explanation of the challenge mechanics and how to solve it.

---

### **Challenge Details**

The challenge introduces the APT game, where:
1. RSA encryption is used to generate ciphertexts ("shots").
2. Each player is assigned a unique public exponent (`e`).
3. A common modulus `n` is used for all encryption operations.

At the start of the game:
- The list of public exponents (`Es`) and the modulus (`n`) is displayed.
- The goal is to recover the plaintext (`FLAG`) by collecting ciphertexts and exploiting the vulnerability.

---

### **The Cryptographic Vulnerability**

#### **Common Modulus Attack**

The RSA encryption formula is:
\[
c = m^e \mod n
\]
Where:
- \( c \): ciphertext
- \( m \): plaintext
- \( e \): public exponent
- \( n \): common modulus

If two ciphertexts are generated using the same modulus `n` but **different public exponents** `e1` and `e2`, and if `e1` and `e2` are coprime, the plaintext \( m \) can be recovered using the **common modulus attack**.

---

### **Attack Steps**

#### **1. Collect Ciphertexts**

You need two ciphertexts (\( c1, c2 \)) encrypted with different public exponents (\( e1, e2 \)). Ensure:
- The ciphertexts are valid (not distorted, indicated by the `huh?` message).
- \( e1 \) and \( e2 \) are coprime.

#### **2. Use the Extended Euclidean Algorithm**

Find integers \( s1 \) and \( s2 \) such that:
\[
s1 \cdot e1 + s2 \cdot e2 = 1
\]

#### **3. Recover the Plaintext**

The plaintext \( m \) can be computed as:
\[
m = (c1^{s1} \cdot c2^{-s2}) \mod n
\]
Where:
- \( c2^{-s2} \) is the modular inverse of \( c2 \) raised to \( -s2 \).
