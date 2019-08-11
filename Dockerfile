FROM python:3.7.4-buster

RUN pip install flask==0.12.2 \
    oauth2client==4.1.3 \
    gspread==3.0.1 \
    gunicorn==19.9.0 \
    pytest==3.4.2 \
    pandas==0.25.0 \
    xlrd==1.2.0

COPY . /app
WORKDIR /app

