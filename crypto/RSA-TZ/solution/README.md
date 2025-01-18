## Solution Explanation

In this challenge, we exploit the fact that the prime factors `p` and `q` of the modulus `n` are close in value (i.e., they have the same bit length), and `p` is slightly less than `q`. Here's a step-by-step breakdown of the solution:

### Key Observations and Reshaping the Problem

1. **Given Relationship**:
   - Since `q % p = TZ` (the remainder when `q` is divided by `p`), we can express `q` in terms of `p` and `TZ` as:
     
     ```
     q = k * p + TZ
     ```

     Where `k` is a small integer, and we can assume `k` is small.

2. **Rewriting TZ**:
   - Using the relation `TZ = p - q`, we can substitute and reshape the equation.

3. **Substituting Into n**:
   - The modulus `n` is the product of `p` and `q`, so:

     ```
     n = p * q
     n = (TZ + q) * q
     ```

4. **Quadratic Equation**:
   - Expanding and reshaping:

     ```
     n = q^2 + TZ * q
     q^2 + TZ * q - n = 0
     ```

   - This is a standard quadratic equation of the form:

     ```
     ax^2 + bx + c = 0
     ```

     Here, `a = 1`, `b = TZ`, and `c = -n`.

### Solving for `q`

Using the quadratic formula:

```
q = (-b \pm \sqrt{b^2 - 4ac}) / 2a
```

Substituting the values:

```
q = (-TZ \pm \sqrt{TZ^2 + 4n}) / 2
```

Select the positive root, as `q` must be positive.

### Finding `p`

Once `q` is found, compute `p` using:

```
p = n // q
```

### Computing `phi` and the Private Key `d`

1. **Compute `phi`**:
   - The Euler's totient function `phi` is given by:

     ```
     phi = (p - 1) * (q - 1)
     ```

2. **Find `d`**:
   - The private exponent `d` is the modular inverse of `e` modulo `phi`:

     ```
     d = e^-1 mod phi
     ```

### Decrypting the Ciphertext

Finally, use the private key `d` to decrypt the ciphertext `ct`:

```
flag = ct^d mod n
```

The decrypted value `flag` represents the plaintext or solution to the challenge.
