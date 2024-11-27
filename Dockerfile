FROM python:alpine

RUN apk update

WORKDIR /cs_uk


RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1


CMD exec sh -c "python manage.py collectstatic --dry-run && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"