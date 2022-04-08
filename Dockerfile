FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN wget 

COPY ..

CMD [ "python", "./" ]