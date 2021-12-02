FROM python:3.8

COPY requirements.txt .

EXPOSE 8080

RUN pip3 install -r requirements.txt

COPY main.py .

CMD ["python3", "main.py"]