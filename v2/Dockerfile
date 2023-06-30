FROM python:3.10-alpine
ENV PYTHONBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /code

COPY ./requirement.txt /code/requirement.txt

COPY . /code/app

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 81

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "81"]