FROM ubuntu:24.04


# install dependencies
RUN apt update -y && apt install g++ libssl-dev build-essential -y
RUN apt install  build-essential -y
# make a directory for the challenge
RUN mkdir /chal

WORKDIR /chal
# Copy binary file
COPY source/7aleeb .
COPY source/ynetd .
COPY source/entrypoint.sh .


 
 
EXPOSE 1337

RUN chmod +x ynetd
RUN chmod +x 7aleeb


# add non root user
# RUN groupadd -g 10001 user && \
#    useradd -u 10000 -g user user \
#    && chown -R user:user /chal




# switch to non root user and run the app

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/chal/entrypoint.sh"]

