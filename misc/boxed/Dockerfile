FROM ubuntu:latest

RUN mkdir /ctf

RUN apt update -y && apt install -y busybox socat

RUN mkdir /ctf/chal
WORKDIR /ctf/chal
COPY source/flag .

RUN chmod -x flag

EXPOSE 1337

RUN chmod -x /usr/bin/base64
RUN chmod -x /usr/bin/cat
RUN chmod -x /usr/bin/chmod

RUN groupadd -g 10001 user && useradd -u 10000 -g user user && chown -R user:user /ctf

USER user

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/bin/bash,stderr"]