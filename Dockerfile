FROM python:3.8.1-slim

RUN apt update
RUN apt-get --no-install-recommends install -y ffmpeg

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN chmod 755 ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]