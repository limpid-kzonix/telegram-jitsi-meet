FROM python:slim

RUN addgroup --gid 1000 userapp
RUN adduser --home /home/userapp --gid 1000 --uid 1000 --disabled-password userapp
USER userapp

WORKDIR /home/userapp
COPY ./src/main.py ./
COPY requirements.txt ./

RUN export PATH="$PATH:/home/userapp/.local/bin"
RUN pip install --no-cache-dir --user -r requirements.txt

CMD [ "python", "./main.py" ]