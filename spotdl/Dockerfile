FROM python:3.12-slim-bookworm
RUN apt update
RUN apt install -y ffmpeg
COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt
CMD ["/bin/bash", "./run.sh"]


