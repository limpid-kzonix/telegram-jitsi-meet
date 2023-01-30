FROM python:3.11.1-bullseye

RUN addgroup --gid 1000 userapp
RUN adduser --home /home/userapp --gid 1000 --uid 1000 --disabled-password userapp
USER userapp

WORKDIR /home/userapp
COPY main.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir --user -r requirements.txt

RUN export PATH="$PATH:/home/userapp/.local/bin"

CMD [ "python", "./main.py" ]
