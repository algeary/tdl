FROM python:3.11-slim-bookworm

workdir /app

env port 8000
copy ./ .

run pip3 install -r requirements.txt

arg SECRET_KEY
env SECRET_KEY=$SECRET_KEY

cmd ["python", "manage.py", "runserver"]


