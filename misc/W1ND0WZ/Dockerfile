FROM python:3.11-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat \
    && groupadd ctf \
    && useradd -r -g ctf ctf

WORKDIR /usr/src/app

COPY source/. .

RUN echo $FLAG > flag.txt

RUN chmod 500 server.py \
    && chown ctf:root server.py\ 
    && chmod 444 flag.txt

# USER ctf

EXPOSE 1337

CMD ["socat", "-T30", "TCP-L:1337,fork,reuseaddr", "EXEC:python3 server.py,pty,stderr,setsid,sane,raw,echo=0"]
