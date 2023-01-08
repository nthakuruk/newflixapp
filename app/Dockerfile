FROM python:3.10.4

EXPOSE 9000

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app
CMD python main.py