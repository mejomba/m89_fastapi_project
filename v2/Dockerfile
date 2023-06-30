FROM python:3.10-alpine
ENV PYTHONBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR .

COPY ./requirement.txt ./requirement.txt

COPY . .

RUN pip install -r requirement.txt

#EXPOSE 8001
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]