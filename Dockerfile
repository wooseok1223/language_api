FROM python:3.8

WORKDIR /language_api

ADD . .
RUN pip install -r requirements.txt

EXPOSE 5000
COPY ./run.py /app/

ENTRYPOINT ["python"]

CMD ["run.py", "--host", "0.0.0.0"]