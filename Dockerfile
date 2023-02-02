FROM python:3.10.8-slim-buster

WORKDIR /api
ENV asgname asgname
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py", "asgname"]