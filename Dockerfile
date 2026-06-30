FROM python:3.12

WORKDIR /code

COPY ./pip-requirement.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./dist /code/dist
COPY ./static /code/static
COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
