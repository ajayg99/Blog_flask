FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV EMAIL_USER=test@email.com EMAIL_PASS=password SECRET_KEY=secret_key SQLALCHEMY_DATABASE_URI=db_uri FLASK_APP=app.py

CMD ["flask","run","--host","0.0.0.0"]
