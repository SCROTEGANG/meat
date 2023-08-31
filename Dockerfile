FROM python:3.10.13

WORKDIR /bot

RUN pip install --no-cache-dir pipenv

COPY ./Pipfile ./Pipfile.lock ./

RUN pipenv install --system

COPY ./ ./

CMD ["python", "main.py"]