FROM python:3.9.16-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "bot.py" ]

EXPOSE 8080