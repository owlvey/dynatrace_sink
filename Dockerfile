FROM python:3.9.2
WORKDIR /deployment
COPY ./app ./app
COPY ./requirements.txt .

RUN pip install -r  requirements.txt

ENV PYTHONPATH=/deployment
EXPOSE 5000/tcp
ENTRYPOINT ["python", "./app/startup.py"]