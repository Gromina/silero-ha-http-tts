FROM python:3.9 as silero-ha-http-tts

WORKDIR /usr/app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN apt-get update --fix-missing && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y sox
ADD requirements.txt .
RUN pip3 install -r requirements.txt





FROM silero-ha-http-tts
WORKDIR /usr/app

ADD ./ ./

EXPOSE 80
ADD requirements_last.txt .
RUN pip3 install -r requirements_last.txt

# CMD [ "python3", "-u", "./server.py" ]
CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80" ]
