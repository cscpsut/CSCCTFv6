## Solution Explanation

In this challenge, we exploit a cryptographic vulnerability that arises when the same random value `k` is reused during the signing of two different messages. This section explains the process and how the attack functions.

### Key Concept: The Danger of Reusing `k`

When signing a message, the user generates a random value `k` and uses it in the signature calculation. The following values are publicly shared as part of the signature:

1. `r = (k * G).x mod p`
2. `s = k^-1 * (z + r * dA)`

Where:
- `G` is the generator point.
- `z` is the hash of the message.
- `dA` is the private key.
- `p` is the prime order of the curve or group.

If the same `k` is used for two different signatures, the attacker can recover the private key `dA` using the following process.

### Exploiting the Reuse of `k`

1. **Obtain Two Signatures with the Same `k`**:
   - Let the two messages have hashes `z1` and `z2`, and the corresponding signatures are `(r, s1)` and `(r, s2)`.
   - Since the `k` value is the same for both signatures, we know:

     ```
     s1 = k^-1 * (z1 + r * dA)
     s2 = k^-1 * (z2 + r * dA)
     ```

2. **Calculate `k`**:
   - Subtract the two equations:

     ```
     s1 - s2 = k^-1 * (z1 - z2)
     ```
   - Rearrange to solve for `k`:

     ```
     k = (z1 - z2) / (s1 - s2)
     ```

3. **Recover the Private Key `dA`**:
   - Using one of the signatures, calculate:

     ```
     dA = r^-1 * (k * s - z)
     ```

   - This equation allows the attacker to compute the private key.

### Challenge-Specific Requirements

For the attack to work, you must:

1. Send `inp1`, which is added to the static random value `k`.
2. Send `inp2`, where:

   ```
   inp2 = inp1 + order_of_generator
   ```

By sending these inputs, the same `k` value is effectively reused in two signatures, enabling the attack as described above.

### Practical Implications

Once the attacker has recovered the private key `dA`, they can find the flag as it is the secret key.