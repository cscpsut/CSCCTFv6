1. Register a dummy user
2. send password reset request for admin
3. Brute force the OTP, and reset the password
4. The OTP is a 4 digit number
5. The OTP is between 1000 and 10000
6. To make the brute force faster, we can use the rate limit bypass vulnerability
7. The rate limit is based on the IP address
9. The rate limit is 5 attempts
10. After 5 attempts, the user will be rate limited
11. But if the user (IP) makes a successful login, the rate limit will be reset to 0 attempts and the user can try again
