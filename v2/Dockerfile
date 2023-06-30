FROM python:3.10-alpine

WORKDIR /code

COPY ./requirement.txt /code/requirement.txt

COPY . /code/app

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 81

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "81"]