## **Digital Encryption League** Challenge Walkthrough

This challenge involves exploiting RSA encryption with hints provided through a custom modulus generation mechanism. The ultimate goal is to recover the `FLAG` using the provided ciphertext and modulus hints.

---

### **Challenge Details**

The challenge uses:
- An RSA public exponent \( e = 65537 \).
- A ciphertext \( c \) that encrypts the flag.
- Modulus hints provided through a menu option.

At the start of the game:
- You are given the ciphertext \( c \).
- You can request modulus hints in the form of congruence relations, allowing the recovery of the modulus.

The objective is to reconstruct the modulus \( p \), decrypt the ciphertext, and retrieve the `FLAG`.

---

### **The Cryptographic Vulnerability**

The modulus \( p \) is generated with properties that allow reconstruction through the **Chinese Remainder Theorem (CRT)**:
- Multiple congruences (\( a \mod m \)) are provided.
- Using CRT, the modulus \( p \) can be recovered.

---

### **Attack Steps**

#### **1. Collect Congruences**

Using the menu option, collect congruence relations (\( a \mod m \)). Ensure that the moduli \( m \) are pairwise coprime to use CRT.

#### **2. Reconstruct \( p \)**

Apply CRT to the collected congruences to reconstruct \( p \). The reconstructed value might require a brute-force adjustment due to a missing bit range.

#### **3. Decrypt the Ciphertext**
Since the Flag is smaller than P, we don't need Q to decrypt
#### Proof

We are given:

\[
c = m^e \mod (p \cdot q),
\]

and need to prove:

\[
c \mod p = m^e \mod p.
\]

---

##### Step 1: Express \( c \)

From \( c = m^e \mod (p \cdot q) \), there exists an integer \( k \) such that:

\[
c = m^e - k \cdot (p \cdot q).
\]

---

##### Step 2: Take modulo \( p \)

Taking \( \mod p \) on both sides:

\[
c \mod p = \big(m^e - k \cdot (p \cdot q)\big) \mod p.
\]

---

##### Step 3: Simplify

Since \( p \) divides \( p \cdot q \), the term \( k \cdot (p \cdot q) \mod p \) vanishes, leaving:

\[
c \mod p = m^e \mod p.
\]

---
With \( p \), compute:
\[
\phi = p - 1
\]
The private key \( d \) is calculated as:
\[
d = e^{-1} \mod \phi
\]
Finally, decrypt the ciphertext:
\[
\text{FLAG} = c^d \mod p
\]
