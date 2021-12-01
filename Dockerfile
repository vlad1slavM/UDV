FROM python:3.8

COPY requirements.txt .

EXPOSE 8080

RUN pip3 install -r requirements.txt

COPY tests.py .

COPY main.py .

RUN python -m unittest tests.py

CMD ["python3", "main.py"]