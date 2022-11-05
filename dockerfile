#--------- layer 1
FROM python:3.9 as silero-foundation

WORKDIR /usr/app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN apt-get update --fix-missing && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y sox libsox-fmt-mp3 sox
ADD requirements.txt .
RUN pip3 install -r requirements.txt


#--------- layer 2
FROM silero-foundation as silero-models
WORKDIR /usr/app
ADD download_models.py .
RUN python3 download_models.py


#--------- layer 3
FROM silero-models
WORKDIR /usr/app

ADD ./ ./

EXPOSE 80
# the second part of requiremets just not to rebuild all
ADD requirements_last.txt .
RUN pip3 install -r requirements_last.txt

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80" ]
