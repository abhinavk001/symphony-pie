FROM python:3.8.1-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt-get --no-install-recommends install -y ffmpeg

COPY . /app

CMD ["flask", "run", "--host=0.0.0.0"]