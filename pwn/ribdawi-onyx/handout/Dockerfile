FROM ubuntu:24.04

# Install dependencies
RUN apt update -y && apt install g++ libssl-dev build-essential socat -y  && \
rm -rf /var/lib/apt/lists/*

# Make a directory for the challenge
RUN mkdir /app
WORKDIR /app

# Copy source code file
COPY source/ribdawi_onyx.c .
COPY source/ynetd .
COPY source/entrypoint.sh .


# compile binary (Include libc if required)
RUN gcc ribdawi_onyx.c -o ribdawi-onyx  -fstack-protector  -lcrypto

# Prefered not to edit the below lines
EXPOSE 1337

 

RUN chmod +x ynetd
RUN chmod +x ribdawi-onyx




# switch to non root user and run the app

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
