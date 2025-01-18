FROM python:3.11-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat \
    && groupadd ctf \
    && useradd -r -g ctf ctf

WORKDIR /usr/src/app

COPY . .

RUN chmod 500 chall.py \
    && chmod 500 secret.py \
    && chown ctf:root chall.py \
    && chown ctf:root secret.py

USER ctf

EXPOSE 1337

CMD socat -T120 TCP-L:1337,fork,reuseaddr,nodelay EXEC:"stdbuf -i0 -o0 -e0 python3 chall.py",pty,stderr,setsid,sane,raw,echo=0,iexten=0
